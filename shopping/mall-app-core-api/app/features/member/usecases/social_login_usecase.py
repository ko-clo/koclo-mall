"""소셜 로그인 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import SocialLoginResponse, SocialMemberUpsertRequest
from app.features.member.member_service import MemberService


class SocialLoginUseCase:
    """소셜 로그인 시 회원 UPSERT UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(
        self,
        user_id: UUID,
        email: str,
        data: SocialMemberUpsertRequest,
    ) -> SocialLoginResponse:
        """소셜 회원 UPSERT 실행."""
        return await self._service.upsert_social_member(user_id, email, data)
