"""Member Service - Business Logic + TX 관리."""

from datetime import datetime, timezone
from uuid import UUID

from app.core.database import with_session
from app.core.exceptions import BadRequestException, ConflictException
from app.core.security import create_token, decode_token
from app.features.member.member_model import MemberStatus
from app.features.member.member_pdschema import (
    MemberProfileResponse,
    MemberProfileUpdate,
    PasswordChangeRequest,
    SignupRequest,
    SignupResponse,
    SocialLoginResponse,
    SocialMemberUpsertRequest,
    WithdrawCheckResponse,
)
from app.features.member.member_provider import MemberProvider
from supabase import Client as SupabaseClient

WITHDRAW_TOKEN_EXPIRE_MINUTES = 10


class MemberService:
    """회원 비즈니스 로직 (Singleton)."""

    def __init__(self, provider: MemberProvider, supabase: SupabaseClient):
        self._provider = provider
        self._supabase = supabase

    # ============================================================
    # MBR-001: 회원가입
    # ============================================================

    @with_session
    async def signup(self, data: SignupRequest) -> SignupResponse:
        """이메일 회원가입."""
        if not data.agreements.terms or not data.agreements.privacy:
            raise BadRequestException("필수 약관에 동의해야 합니다", code="TERMS_NOT_AGREED")

        if data.password != data.password_confirm:
            raise BadRequestException("비밀번호가 일치하지 않습니다", code="PASSWORD_MISMATCH")

        if await self._provider.exists_by_email(data.email):
            raise ConflictException("이미 가입된 이메일입니다", code="EMAIL_ALREADY_EXISTS")

        try:
            auth_response = self._supabase.auth.sign_up({
                "email": data.email,
                "password": data.password,
            })
        except Exception as e:
            if "already registered" in str(e).lower():
                raise ConflictException("이미 가입된 이메일입니다", code="EMAIL_ALREADY_EXISTS")
            raise BadRequestException(f"회원가입 실패: {e}")

        user = auth_response.user
        if not user:
            raise BadRequestException("회원가입 처리 중 오류가 발생했습니다")

        now = datetime.now(timezone.utc)
        user_id = UUID(user.id)

        await self._provider.create_member(
            member_id=user_id,
            status=MemberStatus.PENDING,
            marketing_agreed=data.agreements.marketing,
            terms_agreed_at=now,
            privacy_agreed_at=now,
        )

        await self._provider.create_profile(
            member_id=user_id,
            email=data.email,
            name=data.name,
            phone=data.phone,
        )

        return SignupResponse(id=str(user_id), email=data.email)

    @with_session
    async def upsert_social_member(
        self,
        user_id: UUID,
        email: str,
        data: SocialMemberUpsertRequest,
    ) -> SocialLoginResponse:
        """소셜 로그인 시 회원 UPSERT."""
        now = datetime.now(timezone.utc)
        member = await self._provider.find_by_id(user_id)

        if member:
            updates = {"last_login_at": now}
            if member.status == MemberStatus.DORMANT:
                updates["status"] = MemberStatus.ACTIVE
            member = await self._provider.update_member(member, **updates)
        else:
            member = await self._provider.create_member(
                member_id=user_id,
                status=MemberStatus.ACTIVE,
                marketing_agreed=data.marketing_agreed,
                terms_agreed_at=now,
                privacy_agreed_at=now,
            )
            await self._provider.create_profile(
                member_id=user_id,
                email=email,
                name=data.name or email.split("@")[0],
            )

        return SocialLoginResponse(id=str(member.id), status=member.status.value)

    # ============================================================
    # MBR-002: 로그인/로그아웃
    # ============================================================

    @with_session
    async def record_login(self, member_id: UUID) -> None:
        """로그인 기록 업데이트."""
        member = await self._provider.find_by_id(member_id)
        if not member:
            return

        updates = {"last_login_at": datetime.now(timezone.utc)}
        if member.status == MemberStatus.DORMANT:
            updates["status"] = MemberStatus.ACTIVE

        await self._provider.update_member(member, **updates)

    # ============================================================
    # MBR-003: 비밀번호 재설정
    # ============================================================

    async def request_password_reset(self, email: str) -> None:
        """비밀번호 재설정 요청."""
        try:
            self._supabase.auth.reset_password_email(email)
        except Exception:
            pass  # 보안: 이메일 존재 여부 노출 방지

    async def reset_password(self, user_id: UUID, new_password: str) -> None:
        """비밀번호 재설정."""
        try:
            self._supabase.auth.admin.update_user_by_id(
                str(user_id),
                {"password": new_password},
            )
        except Exception as e:
            raise BadRequestException(f"비밀번호 변경 실패: {e}")

    async def change_password(
        self,
        member_id: UUID,
        email: str,
        data: PasswordChangeRequest,
    ) -> None:
        """비밀번호 변경."""
        if data.new_password != data.new_password_confirm:
            raise BadRequestException("새 비밀번호가 일치하지 않습니다", code="PASSWORD_MISMATCH")

        try:
            self._supabase.auth.sign_in_with_password({
                "email": email,
                "password": data.current_password,
            })
        except Exception:
            raise BadRequestException("현재 비밀번호가 일치하지 않습니다", code="WRONG_PASSWORD")

        try:
            self._supabase.auth.admin.update_user_by_id(
                str(member_id),
                {"password": data.new_password},
            )
        except Exception as e:
            raise BadRequestException(f"비밀번호 변경 실패: {e}")

    # ============================================================
    # MBR-004: 회원정보 수정
    # ============================================================

    @with_session
    async def get_profile(self, member_id: UUID) -> MemberProfileResponse | None:
        """회원 프로필 조회."""
        member = await self._provider.find_by_id(member_id)
        if not member or not member.profile:
            return None

        return MemberProfileResponse(
            id=member.id,
            email=member.profile.email,
            name=member.profile.name,
            phone=member.profile.phone,
            profile_image=member.profile.profile_image,
            status=member.status.value,
            marketing_agreed=member.marketing_agreed,
            created_at=member.created_at,
        )

    @with_session
    async def update_profile(
        self,
        member_id: UUID,
        data: MemberProfileUpdate,
    ) -> MemberProfileResponse:
        """프로필 수정."""
        member = await self._provider.find_by_id(member_id)
        if not member or not member.profile:
            raise BadRequestException("회원 정보를 찾을 수 없습니다")

        profile_updates = {}
        if data.name is not None:
            profile_updates["name"] = data.name
        if data.phone is not None:
            profile_updates["phone"] = data.phone

        if profile_updates:
            await self._provider.update_profile(member.profile, **profile_updates)

        if data.marketing_agreed is not None:
            await self._provider.update_member(member, marketing_agreed=data.marketing_agreed)

        return MemberProfileResponse(
            id=member.id,
            email=member.profile.email,
            name=member.profile.name,
            phone=member.profile.phone,
            profile_image=member.profile.profile_image,
            status=member.status.value,
            marketing_agreed=member.marketing_agreed,
            created_at=member.created_at,
        )

    # ============================================================
    # MBR-005: 회원 탈퇴
    # ============================================================

    async def check_withdraw(self, member_id: UUID) -> WithdrawCheckResponse:
        """탈퇴 가능 여부 확인."""
        blockers: list[str] = []
        warnings: list[str] = []

        # TODO: 진행 중 주문 확인 (Order feature 구현 후)
        # TODO: 환불 진행 중 확인
        # TODO: 미사용 포인트/쿠폰 확인

        can_withdraw = len(blockers) == 0
        withdraw_token = None
        if can_withdraw:
            withdraw_token = create_token(
                {"sub": str(member_id), "purpose": "withdraw"},
                WITHDRAW_TOKEN_EXPIRE_MINUTES,
            )

        return WithdrawCheckResponse(
            can_withdraw=can_withdraw,
            blockers=blockers,
            warnings=warnings,
            withdraw_token=withdraw_token,
        )

    @with_session
    async def withdraw(
        self,
        member_id: UUID,
        email: str,
        reason: str,
        password: str | None,
        withdraw_token: str,
    ) -> None:
        """회원 탈퇴."""
        payload = decode_token(withdraw_token)
        if payload.get("purpose") != "withdraw":
            raise BadRequestException("유효하지 않은 탈퇴 토큰입니다", code="INVALID_WITHDRAW_TOKEN")
        if payload.get("sub") != str(member_id):
            raise BadRequestException("유효하지 않은 탈퇴 토큰입니다", code="INVALID_WITHDRAW_TOKEN")

        if password:
            try:
                self._supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password,
                })
            except Exception:
                raise BadRequestException("비밀번호가 일치하지 않습니다", code="WRONG_PASSWORD")

        member = await self._provider.find_by_id(member_id)
        if not member:
            raise BadRequestException("회원 정보를 찾을 수 없습니다")

        now = datetime.now(timezone.utc)
        await self._provider.update_member(
            member,
            status=MemberStatus.WITHDRAWN,
            withdrawn_at=now,
            withdrawal_reason=reason,
        )
