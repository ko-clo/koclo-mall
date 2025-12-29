"""탈퇴 가능 여부 조회 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import WithdrawCheckResponse
from app.features.member.member_service import MemberService


class GetWithdrawCheckUseCase:
    """탈퇴 가능 여부 조회 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, member_id: UUID) -> WithdrawCheckResponse:
        """탈퇴 가능 여부 조회 실행."""
        return await self._service.check_withdraw(member_id)
