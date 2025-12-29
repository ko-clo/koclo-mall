"""로그인 기록 UseCase."""

from uuid import UUID

from app.features.member.member_service import MemberService


class RecordLoginUseCase:
    """로그인 기록 업데이트 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, member_id: UUID) -> None:
        """로그인 기록 실행."""
        await self._service.record_login(member_id)
