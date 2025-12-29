"""JWT 검증 및 보안 관련 유틸리티."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import BadRequestException, UnauthorizedException


@dataclass
class TokenPayload:
    """JWT 토큰 페이로드."""

    sub: UUID  # user_id
    email: str | None
    role: str  # authenticated, admin
    exp: datetime


def verify_supabase_jwt(token: str) -> TokenPayload:
    """Supabase JWT 토큰을 검증하고 페이로드를 반환합니다.

    Args:
        token: Bearer 토큰 (prefix 제외)

    Returns:
        TokenPayload: 검증된 토큰 페이로드

    Raises:
        UnauthorizedException: 토큰이 유효하지 않거나 만료됨
    """
    if not settings.supabase_jwt_secret:
        raise UnauthorizedException("JWT secret이 설정되지 않았습니다")

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
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
        raise BadRequestException("유효하지 않은 토큰입니다", code="INVALID_TOKEN") from e
