"""프로필 조회 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import MemberProfileResponse
from app.features.member.member_service import MemberService


class GetProfileUseCase:
    """회원 프로필 조회 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, member_id: UUID) -> MemberProfileResponse | None:
        """프로필 조회 실행."""
        return await self._service.get_profile(member_id)
