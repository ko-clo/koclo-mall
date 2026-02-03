"""JWT 검증 및 보안 관련 유틸리티."""

import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import httpx
from jose import JWTError, jwt
from jose.exceptions import JWKError

from app.core.config import settings
from app.core.exceptions import BadRequestException, UnauthorizedException


@dataclass
class TokenPayload:
    """JWT 토큰 페이로드."""

    sub: UUID  # user_id
    email: str | None
    role: str  # authenticated, admin
    exp: datetime


# JWKS 캐시 (1시간)
_jwks_cache: dict[str, Any] = {}
_jwks_cache_time: float = 0
_JWKS_CACHE_TTL = 3600  # 1시간


def _get_jwks() -> dict[str, Any]:
    """Supabase JWKS를 가져옵니다 (캐시 사용)."""
    global _jwks_cache, _jwks_cache_time

    now = time.time()
    if _jwks_cache and (now - _jwks_cache_time) < _JWKS_CACHE_TTL:
        return _jwks_cache

    if not settings.supabase_url:
        raise UnauthorizedException("Supabase URL이 설정되지 않았습니다")

    jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"

    try:
        response = httpx.get(jwks_url, timeout=10)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_cache_time = now
        return _jwks_cache
    except httpx.HTTPError as e:
        raise UnauthorizedException(f"JWKS를 가져올 수 없습니다: {e}") from e


def _get_signing_key(token: str) -> dict[str, Any]:
    """토큰의 kid에 맞는 signing key를 찾습니다."""
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise UnauthorizedException(f"토큰 헤더를 파싱할 수 없습니다: {e}") from e

    kid = unverified_header.get("kid")
    if not kid:
        raise UnauthorizedException("토큰에 kid가 없습니다")

    jwks = _get_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key

    raise UnauthorizedException(f"일치하는 signing key를 찾을 수 없습니다: {kid}")


def verify_supabase_jwt(token: str) -> TokenPayload:
    """Supabase JWT 토큰을 검증하고 페이로드를 반환합니다 (JWKS 사용).

    Args:
        token: Bearer 토큰 (prefix 제외)

    Returns:
        TokenPayload: 검증된 토큰 페이로드

    Raises:
        UnauthorizedException: 토큰이 유효하지 않거나 만료됨
    """
    signing_key = _get_signing_key(token)

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256", "ES256"],
            audience="authenticated",
        )
    except JWTError as e:
        raise UnauthorizedException(f"유효하지 않은 토큰입니다: {e}") from e

    # 필수 필드 확인
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedException("토큰에 사용자 ID가 없습니다")

    # 만료 시간 확인
    exp = payload.get("exp")
    if not exp:
        raise UnauthorizedException("토큰에 만료 시간이 없습니다")

    exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
    if exp_datetime < datetime.now(timezone.utc):
        raise UnauthorizedException("토큰이 만료되었습니다")

    return TokenPayload(
        sub=UUID(sub),
        email=payload.get("email"),
        role=payload.get("role", "authenticated"),
        exp=exp_datetime,
    )


def create_token(payload: dict, expire_minutes: int) -> str:
    """JWT 토큰 생성.

    Args:
        payload: 토큰에 담을 데이터
        expire_minutes: 만료 시간 (분)

    Returns:
        JWT 토큰 문자열
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = {**payload, "exp": expire}
    return jwt.encode(to_encode, settings.supabase_jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    """JWT 토큰 디코딩.

    Args:
        token: JWT 토큰 문자열

    Returns:
        토큰 페이로드

    Raises:
        BadRequestException: 토큰이 유효하지 않거나 만료됨
    """
    try:
        return jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
        )
    except JWTError as e:
        raise BadRequestException(
            "유효하지 않은 토큰입니다", code="INVALID_TOKEN"
        ) from e
