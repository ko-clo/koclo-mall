"""Member Service 유닛 테스트."""

import os

# Ensure environment variables are set for testing
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-key-for-testing-purposes-only")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test"
)

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.core.exceptions import BadRequestException, ConflictException
from app.features.member.member_model import MemberStatus
from app.features.member.member_pdschema import (
    AgreementsSchema,
    MemberConnectRequest,
    SignupRequest,
)
from app.features.member.member_service import MemberService

from tests.conftest import (
    MockSupabaseAuthResponse,
    MockSupabaseUser,
    create_mock_member,
)


# ============================================================
# signup() 테스트
# ============================================================


class TestSignup:
    """signup() 메서드 테스트."""

    async def test_signup_success(
        self,
        member_service: MemberService,
        mock_supabase: MagicMock,
    ):
        """정상적인 회원가입."""
        # Given
        user_id = str(uuid4())
        mock_supabase.auth.sign_up.return_value = MockSupabaseAuthResponse(
            MockSupabaseUser(user_id=user_id, email="test@example.com")
        )

        request = SignupRequest(
            email="test@example.com",
            password="Test1234!",
            passwordConfirm="Test1234!",
        )

        # When
        result = await member_service.signup(request)

        # Then
        assert result.id == user_id
        assert result.email == "test@example.com"
        assert result.message == "인증 이메일을 확인하세요"
        mock_supabase.auth.sign_up.assert_called_once_with(
            {
                "email": "test@example.com",
                "password": "Test1234!",
            }
        )

    async def test_signup_password_mismatch(
        self,
        member_service: MemberService,
    ):
        """비밀번호 불일치."""
        request = SignupRequest(
            email="test@example.com",
            password="Test1234!",
            passwordConfirm="Test5678!",
        )

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.signup(request)

        assert exc_info.value.code == "PASSWORD_MISMATCH"
        assert "비밀번호가 일치하지 않습니다" in str(exc_info.value)

    async def test_signup_email_already_exists(
        self,
        member_service: MemberService,
        mock_supabase: MagicMock,
    ):
        """이미 가입된 이메일."""
        mock_supabase.auth.sign_up.side_effect = Exception("User already registered")

        request = SignupRequest(
            email="existing@example.com",
            password="Test1234!",
            passwordConfirm="Test1234!",
        )

        with pytest.raises(ConflictException) as exc_info:
            await member_service.signup(request)

        assert exc_info.value.code == "EMAIL_ALREADY_EXISTS"

    async def test_signup_supabase_error(
        self,
        member_service: MemberService,
        mock_supabase: MagicMock,
    ):
        """Supabase 오류."""
        mock_supabase.auth.sign_up.side_effect = Exception("Unknown error")

        request = SignupRequest(
            email="test@example.com",
            password="Test1234!",
            passwordConfirm="Test1234!",
        )

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.signup(request)

        assert "회원가입 실패" in str(exc_info.value)

    async def test_signup_no_user_returned(
        self,
        member_service: MemberService,
        mock_supabase: MagicMock,
    ):
        """Supabase가 user를 반환하지 않음."""
        mock_supabase.auth.sign_up.return_value = MockSupabaseAuthResponse(user=None)

        request = SignupRequest(
            email="test@example.com",
            password="Test1234!",
            passwordConfirm="Test1234!",
        )

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.signup(request)

        assert "회원가입 처리 중 오류가 발생했습니다" in str(exc_info.value)


# ============================================================
# connect() 테스트
# ============================================================


class TestConnect:
    """connect() 메서드 테스트."""

    @patch("app.core.database.get_session")
    async def test_connect_new_member(
        self,
        mock_get_session: MagicMock,
        mock_provider: MagicMock,
        mock_supabase: MagicMock,
    ):
        """신규 회원 연결."""
        # Given
        user_id = uuid4()
        email = "new@example.com"

        new_member = create_mock_member(
            member_id=user_id,
            email=email,
            status=MemberStatus.ACTIVE,
        )
        mock_provider.find_by_id.return_value = None  # 회원 없음
        mock_provider.create_member.return_value = new_member

        service = MemberService(mock_provider, mock_supabase)
        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True, marketing=True),
            name="홍길동",
            phone="+821012345678",
        )

        # When
        result = await service.connect(user_id, email, request)

        # Then
        assert result.id == str(user_id)
        assert result.email == email
        assert result.status == "ACTIVE"
        assert result.is_new is True
        mock_provider.create_member.assert_called_once()
        mock_provider.create_profile.assert_called_once()

    @patch("app.core.database.get_session")
    async def test_connect_existing_member(
        self,
        mock_get_session: MagicMock,
        member_service: MemberService,
        mock_provider: MagicMock,
    ):
        """기존 회원 연결 (로그인 기록 업데이트)."""
        # Given
        user_id = uuid4()
        email = "existing@example.com"
        existing_member = create_mock_member(
            member_id=user_id,
            email=email,
            status=MemberStatus.ACTIVE,
        )
        mock_provider.find_by_id.return_value = existing_member

        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
        )

        # When
        result = await member_service.connect(user_id, email, request)

        # Then
        assert result.id == str(user_id)
        assert result.status == "ACTIVE"
        assert result.is_new is False
        mock_provider.update_member.assert_called_once()
        mock_provider.create_member.assert_not_called()
        mock_provider.create_profile.assert_not_called()

    @patch("app.core.database.get_session")
    async def test_connect_dormant_member_reactivated(
        self,
        mock_get_session: MagicMock,
        member_service: MemberService,
        mock_provider: MagicMock,
    ):
        """휴면 회원 연결 시 활성화."""
        # Given
        user_id = uuid4()
        dormant_member = create_mock_member(
            member_id=user_id,
            status=MemberStatus.DORMANT,
        )
        mock_provider.find_by_id.return_value = dormant_member

        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
        )

        # When
        await member_service.connect(user_id, "dormant@example.com", request)

        # Then
        call_kwargs = mock_provider.update_member.call_args[1]
        assert call_kwargs["status"] == MemberStatus.ACTIVE

    @patch("app.core.database.get_session")
    async def test_connect_terms_not_agreed(
        self,
        mock_get_session: MagicMock,
        member_service: MemberService,
    ):
        """필수 약관 미동의."""
        user_id = uuid4()
        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=False, privacy=True),
        )

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.connect(user_id, "test@example.com", request)

        assert exc_info.value.code == "TERMS_NOT_AGREED"

    @patch("app.core.database.get_session")
    async def test_connect_privacy_not_agreed(
        self,
        mock_get_session: MagicMock,
        member_service: MemberService,
    ):
        """개인정보 약관 미동의."""
        user_id = uuid4()
        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=False),
        )

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.connect(user_id, "test@example.com", request)

        assert exc_info.value.code == "TERMS_NOT_AGREED"

    @patch("app.core.database.get_session")
    async def test_connect_default_name_from_email(
        self,
        mock_get_session: MagicMock,
        mock_provider: MagicMock,
        mock_supabase: MagicMock,
    ):
        """이름 미제공 시 이메일에서 추출."""
        # Given
        user_id = uuid4()
        email = "john.doe@example.com"

        new_member = create_mock_member(member_id=user_id, email=email)
        mock_provider.find_by_id.return_value = None
        mock_provider.create_member.return_value = new_member

        service = MemberService(mock_provider, mock_supabase)
        request = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
            # name 미제공
        )

        # When
        await service.connect(user_id, email, request)

        # Then
        profile_call_kwargs = mock_provider.create_profile.call_args[1]
        assert profile_call_kwargs["name"] == "john.doe"  # @앞 부분


# ============================================================
# change_password() 테스트
# ============================================================


class TestChangePassword:
    """change_password() 메서드 테스트."""

    async def test_change_password_mismatch(
        self,
        member_service: MemberService,
    ):
        """새 비밀번호 불일치."""
        from app.features.member.member_pdschema import PasswordChangeRequest

        data = MagicMock()
        data.new_password = "NewPass1!"
        data.new_password_confirm = "DifferentPass1!"
        data.current_password = "OldPass1!"

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.change_password(uuid4(), "test@example.com", data)

        assert exc_info.value.code == "PASSWORD_MISMATCH"

    async def test_change_password_wrong_current(
        self,
        member_service: MemberService,
        mock_supabase: MagicMock,
    ):
        """현재 비밀번호 틀림."""
        mock_supabase.auth.sign_in_with_password.side_effect = Exception(
            "Invalid credentials"
        )

        data = MagicMock()
        data.new_password = "NewPass1!"
        data.new_password_confirm = "NewPass1!"
        data.current_password = "WrongPass1!"

        with pytest.raises(BadRequestException) as exc_info:
            await member_service.change_password(uuid4(), "test@example.com", data)

        assert exc_info.value.code == "WRONG_PASSWORD"
