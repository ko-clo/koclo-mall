"""공통 테스트 fixture."""

import os

# Mock settings before importing app modules
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "test-service-role-key")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-key-for-testing-purposes-only")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test"
)

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

# Mock supabase client before importing member modules
with patch("supabase.create_client") as mock_create_client:
    mock_create_client.return_value = MagicMock()
    from app.features.member.member_model import Member, MemberProfile, MemberStatus
    from app.features.member.member_provider import MemberProvider
    from app.features.member.member_service import MemberService


# ============================================================
# Mock Supabase
# ============================================================


class MockSupabaseUser:
    """Mock Supabase User."""

    def __init__(self, user_id: str | None = None, email: str = "test@example.com"):
        self.id = user_id or str(uuid4())
        self.email = email


class MockSupabaseAuthResponse:
    """Mock Supabase Auth Response."""

    def __init__(self, user: MockSupabaseUser | None = None):
        self.user = user


class MockSupabaseAuth:
    """Mock Supabase Auth."""

    def __init__(self):
        self.sign_up = MagicMock(
            return_value=MockSupabaseAuthResponse(MockSupabaseUser())
        )
        self.sign_in_with_password = MagicMock()
        self.reset_password_email = MagicMock()
        self.admin = MagicMock()
        self.admin.update_user_by_id = MagicMock()


class MockSupabaseClient:
    """Mock Supabase Client."""

    def __init__(self):
        self.auth = MockSupabaseAuth()


@pytest.fixture
def mock_supabase() -> MockSupabaseClient:
    """Mock Supabase Client fixture."""
    return MockSupabaseClient()


# ============================================================
# Mock Provider
# ============================================================


def create_mock_member(
    member_id: UUID | None = None,
    status: MemberStatus = MemberStatus.ACTIVE,
    email: str = "test@example.com",
    name: str = "테스트",
    phone: str | None = None,
    marketing_agreed: bool = False,
) -> Member:
    """테스트용 Member 객체 생성."""
    now = datetime.now(timezone.utc)
    member = MagicMock(spec=Member)
    member.id = member_id or uuid4()
    member.status = status
    member.marketing_agreed = marketing_agreed
    member.terms_agreed_at = now
    member.privacy_agreed_at = now
    member.last_login_at = None
    member.created_at = now
    member.updated_at = now

    profile = MagicMock(spec=MemberProfile)
    profile.member_id = member.id
    profile.email = email
    profile.name = name
    profile.phone = phone
    profile.profile_image = None
    profile.created_at = now
    profile.updated_at = now

    member.profile = profile
    return member


@pytest.fixture
def mock_provider() -> MagicMock:
    """Mock MemberProvider fixture."""
    provider = MagicMock(spec=MemberProvider)
    provider.find_by_id = AsyncMock(return_value=None)
    provider.find_by_email = AsyncMock(return_value=None)
    provider.exists_by_email = AsyncMock(return_value=False)
    # create_member will return a default mock member
    # Tests should override this with specific return values when needed
    provider.create_member = AsyncMock(return_value=create_mock_member())
    provider.create_profile = AsyncMock()
    provider.update_member = AsyncMock()
    provider.update_profile = AsyncMock()
    return provider


# ============================================================
# Member Service
# ============================================================


@pytest.fixture
def member_service(
    mock_provider: MagicMock, mock_supabase: MockSupabaseClient
) -> MemberService:
    """MemberService fixture with mocked dependencies."""
    return MemberService(mock_provider, mock_supabase)
