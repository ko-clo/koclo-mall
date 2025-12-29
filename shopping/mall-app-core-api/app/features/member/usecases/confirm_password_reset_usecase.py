"""비밀번호 재설정 확인 UseCase."""

from uuid import UUID

from app.features.member.member_service import MemberService


class ConfirmPasswordResetUseCase:
    """비밀번호 재설정 확인 UseCase (토큰 검증 후 비밀번호 변경)."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, user_id: UUID, new_password: str) -> None:
        """비밀번호 재설정 실행."""
        await self._service.reset_password(user_id, new_password)
