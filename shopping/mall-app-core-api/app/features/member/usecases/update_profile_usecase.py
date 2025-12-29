"""프로필 수정 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import MemberProfileResponse, MemberProfileUpdate
from app.features.member.member_service import MemberService


class UpdateProfileUseCase:
    """회원 프로필 수정 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, member_id: UUID, data: MemberProfileUpdate) -> MemberProfileResponse:
        """프로필 수정 실행."""
        return await self._service.update_profile(member_id, data)
