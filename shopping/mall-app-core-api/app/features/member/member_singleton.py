"""Member feature - Singleton instances."""

from supabase import create_client

from app.core.config import settings
from app.features.member.member_provider import MemberProvider
from app.features.member.member_service import MemberService
from app.features.member.usecases import (
    ConfirmPasswordResetUseCase,
    ConnectMemberUseCase,
    GetProfileUseCase,
    GetWithdrawCheckUseCase,
    PasswordChangeUseCase,
    RecordLoginUseCase,
    RequestPasswordResetUseCase,
    SignupUseCase,
    UpdateProfileUseCase,
    WithdrawUseCase,
)

# Singletons
supabase_client = create_client(settings.supabase_url, settings.supabase_service_role_key)
member_provider = MemberProvider()
member_service = MemberService(member_provider, supabase_client)

# UseCases
signup_usecase = SignupUseCase(member_service)
connect_member_usecase = ConnectMemberUseCase(member_service)
record_login_usecase = RecordLoginUseCase(member_service)
request_password_reset_usecase = RequestPasswordResetUseCase(member_service)
confirm_password_reset_usecase = ConfirmPasswordResetUseCase(member_service)
get_profile_usecase = GetProfileUseCase(member_service)
update_profile_usecase = UpdateProfileUseCase(member_service)
password_change_usecase = PasswordChangeUseCase(member_service)
get_withdraw_check_usecase = GetWithdrawCheckUseCase(member_service)
withdraw_usecase = WithdrawUseCase(member_service)
