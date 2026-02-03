"""Member Controller - HTTP Layer."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import BadRequestException
from app.core.security import TokenPayload, verify_supabase_jwt
from app.features.member.member_pdschema import (
    MemberProfileResponse,
    MemberProfileUpdate,
    PasswordChangeRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    SignupRequest,
    SignupResponse,
    MemberConnectResponse,
    MemberConnectRequest,
    WithdrawCheckResponse,
    WithdrawRequest,
)
from app.features.member.member_singleton import (
    confirm_password_reset_usecase,
    get_profile_usecase,
    get_withdraw_check_usecase,
    password_change_usecase,
    record_login_usecase,
    request_password_reset_usecase,
    signup_usecase,
    connect_member_usecase,
    update_profile_usecase,
    withdraw_usecase,
)

router = APIRouter(tags=["member"])
security = HTTPBearer(auto_error=False)


# ============================================================
# Dependencies - Auth
# ============================================================


async def get_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> TokenPayload:
    """JWT 토큰 검증."""
    if not credentials:
        raise BadRequestException("인증 토큰이 필요합니다")
    return verify_supabase_jwt(credentials.credentials)


async def get_current_profile(
    token: Annotated[TokenPayload, Depends(get_token)],
) -> MemberProfileResponse:
    """현재 로그인된 회원 프로필."""
    profile = await get_profile_usecase.execute(token.sub)
    if not profile:
        raise BadRequestException("회원 연결이 필요합니다", code="MEMBER_NOT_CONNECTED")
    return profile


async def get_active_profile(
    profile: Annotated[MemberProfileResponse, Depends(get_current_profile)],
) -> MemberProfileResponse:
    """활성 상태 회원만."""
    if profile.status == "PENDING":
        raise BadRequestException("이메일 인증을 완료해주세요")
    if profile.status == "SUSPENDED":
        raise BadRequestException("정지된 계정입니다")
    if profile.status == "WITHDRAWN":
        raise BadRequestException("탈퇴한 계정입니다")
    return profile


# ============================================================
# MBR-001: 회원가입
# ============================================================


@router.post("/auth/signup", response_model=SignupResponse, status_code=201)
async def signup(data: SignupRequest) -> SignupResponse:
    """이메일 회원가입."""
    return await signup_usecase.execute(data)


@router.post("/members/connect", response_model=MemberConnectResponse, status_code=201)
async def connect_member(
    data: MemberConnectRequest,
    token: Annotated[TokenPayload, Depends(get_token)],
) -> MemberConnectResponse:
    """소셜 로그인 후 회원 연결."""
    return await connect_member_usecase.execute(
        user_id=token.sub,
        email=token.email or "",
        data=data,
    )


# ============================================================
# MBR-002: 로그인/로그아웃
# ============================================================


@router.post("/members/login-record")
async def record_login(
    profile: Annotated[MemberProfileResponse, Depends(get_current_profile)],
) -> dict:
    """로그인 기록 업데이트."""
    await record_login_usecase.execute(profile.id)
    return {"message": "ok"}


# ============================================================
# MBR-003: 비밀번호 재설정
# ============================================================


@router.post("/auth/password/reset-request")
async def request_password_reset(data: PasswordResetRequest) -> dict:
    """비밀번호 재설정 요청."""
    await request_password_reset_usecase.execute(data.email)
    return {"message": "이메일을 확인하세요"}


@router.post("/auth/password/reset")
async def reset_password(
    data: PasswordResetConfirm,
    token: Annotated[TokenPayload, Depends(get_token)],
) -> dict:
    """비밀번호 재설정."""
    if data.password != data.password_confirm:
        raise BadRequestException(
            "비밀번호가 일치하지 않습니다", code="PASSWORD_MISMATCH"
        )
    await confirm_password_reset_usecase.execute(token.sub, data.password)
    return {"message": "비밀번호가 변경되었습니다"}


# ============================================================
# MBR-004: 회원정보 수정
# ============================================================


@router.get("/members/me", response_model=MemberProfileResponse)
async def get_my_profile(
    profile: Annotated[MemberProfileResponse, Depends(get_active_profile)],
) -> MemberProfileResponse:
    """내 프로필 조회."""
    return profile


@router.patch("/members/me", response_model=MemberProfileResponse)
async def update_my_profile(
    data: MemberProfileUpdate,
    profile: Annotated[MemberProfileResponse, Depends(get_active_profile)],
) -> MemberProfileResponse:
    """내 프로필 수정."""
    return await update_profile_usecase.execute(profile.id, data)


@router.post("/members/me/password")
async def change_password(
    data: PasswordChangeRequest,
    profile: Annotated[MemberProfileResponse, Depends(get_active_profile)],
) -> dict:
    """비밀번호 변경."""
    await password_change_usecase.execute(profile.id, profile.email, data)
    return {"message": "비밀번호가 변경되었습니다"}


# ============================================================
# MBR-005: 회원 탈퇴
# ============================================================


@router.get("/members/me/withdraw-check", response_model=WithdrawCheckResponse)
async def check_withdraw(
    profile: Annotated[MemberProfileResponse, Depends(get_active_profile)],
) -> WithdrawCheckResponse:
    """탈퇴 가능 여부 확인."""
    return await get_withdraw_check_usecase.execute(profile.id)


@router.delete("/members/me")
async def withdraw(
    data: WithdrawRequest,
    profile: Annotated[MemberProfileResponse, Depends(get_active_profile)],
) -> dict:
    """회원 탈퇴."""
    await withdraw_usecase.execute(
        profile.id,
        profile.email,
        data.reason,
        data.password,
        data.withdraw_token,
    )
    return {"message": "탈퇴가 완료되었습니다"}
