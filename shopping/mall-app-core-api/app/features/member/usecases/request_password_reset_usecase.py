"""비밀번호 재설정 요청 UseCase."""

from app.features.member.member_service import MemberService


class RequestPasswordResetUseCase:
    """비밀번호 재설정 이메일 발송 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, email: str) -> None:
        """비밀번호 재설정 요청 실행."""
        await self._service.request_password_reset(email)
