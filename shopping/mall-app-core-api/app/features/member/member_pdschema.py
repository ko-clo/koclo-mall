"""Member feature Pydantic 스키마 (API req/res DTO)."""

import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

__all__ = [
    # 회원가입
    "AgreementsSchema",
    "SignupRequest",
    "SignupResponse",
    # 회원 연결
    "MemberConnectRequest",
    "MemberConnectResponse",
    # 소셜 로그인
    "SocialMemberUpsertRequest",
    "SocialLoginResponse",
    # 비밀번호
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChangeRequest",
    # 프로필
    "MemberProfileResponse",
    "MemberProfileUpdate",
    # 탈퇴
    "WithdrawCheckResponse",
    "WithdrawRequest",
]


# ============================================================
# 회원가입 (MBR-001)
# ============================================================


class AgreementsSchema(BaseModel):
    """약관 동의 정보."""

    terms: bool  # 이용약관 (필수)
    privacy: bool  # 개인정보처리방침 (필수)
    marketing: bool = False  # 마케팅 수신 (선택)


class SignupRequest(BaseModel):
    """이메일 회원가입 요청 (Supabase 계정 생성만)."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=20)
    password_confirm: str = Field(..., alias="passwordConfirm")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """영문+숫자+특수문자 조합 필수."""
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("영문자를 포함해야 합니다")
        if not re.search(r"\d", v):
            raise ValueError("숫자를 포함해야 합니다")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("특수문자를 포함해야 합니다")
        return v


class SignupResponse(BaseModel):
    """회원가입 응답."""

    id: str
    email: str
    message: str = "인증 이메일을 확인하세요"


# ============================================================
# 회원 연결 (MBR-001)
# ============================================================


class MemberConnectRequest(BaseModel):
    """이메일 인증 후 또는 소셜 로그인 후 회원 연결 요청."""

    agreements: AgreementsSchema
    name: str | None = Field(None, min_length=2, max_length=50)
    phone: str | None = Field(None, pattern=r"^\+82\d{9,10}$")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """한글 또는 영문만."""
        if v and not re.match(r"^[가-힣a-zA-Z\s]+$", v):
            raise ValueError("이름은 한글 또는 영문만 가능합니다")
        return v


class MemberConnectResponse(BaseModel):
    """회원 연결 응답."""

    id: str
    email: str
    status: str
    is_new: bool = Field(..., serialization_alias="isNew")


# ============================================================
# 소셜 로그인 (MBR-001)
# ============================================================


class SocialMemberUpsertRequest(BaseModel):
    """소셜 로그인 시 회원 UPSERT 요청."""

    name: str | None = None
    marketing_agreed: bool = False


class SocialLoginResponse(BaseModel):
    """소셜 로그인 응답."""

    id: str
    status: str


# ============================================================
# 비밀번호 (MBR-002, MBR-003)
# ============================================================


class PasswordResetRequest(BaseModel):
    """비밀번호 재설정 요청."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """비밀번호 재설정 확인."""

    password: str = Field(..., min_length=8, max_length=20)
    password_confirm: str = Field(..., alias="passwordConfirm")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """영문+숫자+특수문자 조합 필수."""
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("영문자를 포함해야 합니다")
        if not re.search(r"\d", v):
            raise ValueError("숫자를 포함해야 합니다")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("특수문자를 포함해야 합니다")
        return v


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청."""

    current_password: str = Field(..., alias="currentPassword")
    new_password: str = Field(..., min_length=8, max_length=20, alias="newPassword")
    new_password_confirm: str = Field(..., alias="newPasswordConfirm")


# ============================================================
# 프로필 (MBR-004)
# ============================================================


class MemberProfileResponse(BaseModel):
    """회원 프로필 응답."""

    id: UUID
    email: EmailStr
    name: str
    phone: str | None
    profile_image: str | None
    status: str
    marketing_agreed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MemberProfileUpdate(BaseModel):
    """회원 프로필 수정 요청."""

    name: str | None = Field(None, min_length=2, max_length=50)
    phone: str | None = Field(None, pattern=r"^\+82\d{9,10}$")
    marketing_agreed: bool | None = None


# ============================================================
# 탈퇴 (MBR-005)
# ============================================================


class WithdrawCheckResponse(BaseModel):
    """탈퇴 가능 여부 응답."""

    can_withdraw: bool = Field(..., serialization_alias="canWithdraw")
    warnings: list[str] = []
    blockers: list[str] = []
    withdraw_token: str | None = Field(
        None,
        serialization_alias="withdrawToken",
        description="탈퇴 가능 시 발급되는 토큰 (10분 유효)",
    )


class WithdrawRequest(BaseModel):
    """회원 탈퇴 요청."""

    reason: str = Field(
        ...,
        pattern=r"^(SERVICE_UNSATISFIED|RARELY_USED|FOUND_ALTERNATIVE|PRIVACY_CONCERN|OTHER)$",
    )
    password: str | None = None  # 이메일 가입자만
    withdraw_token: str = Field(..., alias="withdrawToken")
