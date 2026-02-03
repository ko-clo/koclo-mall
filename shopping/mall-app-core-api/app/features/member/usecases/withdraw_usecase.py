"""회원 탈퇴 UseCase."""

from uuid import UUID

from app.features.member.member_service import MemberService


class WithdrawUseCase:
    """회원 탈퇴 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(
        self,
        member_id: UUID,
        email: str,
        reason: str,
        password: str | None,
        withdraw_token: str,
    ) -> None:
        """회원 탈퇴 실행."""
        await self._service.withdraw(member_id, email, reason, password, withdraw_token)
