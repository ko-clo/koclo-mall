"""회원가입 UseCase."""

from app.features.member.member_pdschema import SignupRequest, SignupResponse
from app.features.member.member_service import MemberService


class SignupUseCase:
    """이메일 회원가입 UseCase."""

    def __init__(self, service: MemberService):
        self._service = service

    async def execute(self, data: SignupRequest) -> SignupResponse:
        """회원가입 실행."""
        return await self._service.signup(data)
