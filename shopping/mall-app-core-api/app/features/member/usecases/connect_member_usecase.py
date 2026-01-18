"""회원 연결 UseCase."""

from uuid import UUID

from app.features.member.member_pdschema import MemberConnectRequest, MemberConnectResponse
from app.features.member.member_service import MemberService


class ConnectMemberUseCase:
    """소셜 로그인 후 회원 연결 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(
        self,
        user_id: UUID,
        email: str,
        data: MemberConnectRequest,
    ) -> MemberConnectResponse:
        """회원 연결 실행."""
        return await self._service.connect(user_id, email, data)
