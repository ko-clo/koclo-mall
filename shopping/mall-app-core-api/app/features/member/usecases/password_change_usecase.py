"""비밀번호 변경 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import PasswordChangeRequest
from app.features.member.member_service import MemberService


class PasswordChangeUseCase:
    """비밀번호 변경 UseCase (로그인 상태에서)."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(
        self,
        member_id: UUID,
        email: str,
        data: PasswordChangeRequest,
    ) -> None:
        """비밀번호 변경 실행."""
        await self._service.change_password(member_id, email, data)
