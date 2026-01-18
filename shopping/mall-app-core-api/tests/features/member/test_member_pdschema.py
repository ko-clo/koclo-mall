"""Member Pydantic 스키마 유닛 테스트."""

import pytest
from pydantic import ValidationError

from app.features.member.member_pdschema import (
    AgreementsSchema,
    MemberConnectRequest,
    MemberConnectResponse,
    PasswordChangeRequest,
    PasswordResetConfirm,
    SignupRequest,
    SignupResponse,
)


# ============================================================
# SignupRequest 테스트
# ============================================================


class TestSignupRequest:
    """SignupRequest DTO 테스트."""

    def test_valid_signup_request(self):
        """정상적인 회원가입 요청."""
        data = SignupRequest(
            email="test@example.com",
            password="Test1234!",
            passwordConfirm="Test1234!",
        )
        assert data.email == "test@example.com"
        assert data.password == "Test1234!"
        assert data.password_confirm == "Test1234!"

    def test_invalid_email_format(self):
        """잘못된 이메일 형식."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="invalid-email",
                password="Test1234!",
                passwordConfirm="Test1234!",
            )
        assert "email" in str(exc_info.value)

    def test_password_too_short(self):
        """비밀번호 최소 길이 미달."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="test@example.com",
                password="Test1!",  # 7자
                passwordConfirm="Test1!",
            )
        assert "String should have at least 8 characters" in str(exc_info.value)

    def test_password_too_long(self):
        """비밀번호 최대 길이 초과."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="test@example.com",
                password="Test1234567890123456!",  # 21자
                passwordConfirm="Test1234567890123456!",
            )
        assert "String should have at most 20 characters" in str(exc_info.value)

    def test_password_missing_letter(self):
        """비밀번호에 영문자 누락."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="test@example.com",
                password="12345678!",
                passwordConfirm="12345678!",
            )
        assert "영문자를 포함해야 합니다" in str(exc_info.value)

    def test_password_missing_number(self):
        """비밀번호에 숫자 누락."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="test@example.com",
                password="TestTest!",
                passwordConfirm="TestTest!",
            )
        assert "숫자를 포함해야 합니다" in str(exc_info.value)

    def test_password_missing_special_char(self):
        """비밀번호에 특수문자 누락."""
        with pytest.raises(ValidationError) as exc_info:
            SignupRequest(
                email="test@example.com",
                password="Test1234",
                passwordConfirm="Test1234",
            )
        assert "특수문자를 포함해야 합니다" in str(exc_info.value)


# ============================================================
# MemberConnectRequest 테스트
# ============================================================


class TestMemberConnectRequest:
    """MemberConnectRequest DTO 테스트."""

    def test_valid_connect_request_minimal(self):
        """최소 필수 필드만으로 연결 요청."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
        )
        assert data.agreements.terms is True
        assert data.agreements.privacy is True
        assert data.agreements.marketing is False
        assert data.name is None
        assert data.phone is None

    def test_valid_connect_request_full(self):
        """모든 필드 포함 연결 요청."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True, marketing=True),
            name="홍길동",
            phone="+821012345678",
        )
        assert data.name == "홍길동"
        assert data.phone == "+821012345678"
        assert data.agreements.marketing is True

    def test_valid_name_korean(self):
        """한글 이름 유효."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
            name="홍길동",
        )
        assert data.name == "홍길동"

    def test_valid_name_english(self):
        """영문 이름 유효."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
            name="John Doe",
        )
        assert data.name == "John Doe"

    def test_invalid_name_with_numbers(self):
        """숫자 포함 이름 무효."""
        with pytest.raises(ValidationError) as exc_info:
            MemberConnectRequest(
                agreements=AgreementsSchema(terms=True, privacy=True),
                name="홍길동123",
            )
        assert "이름은 한글 또는 영문만 가능합니다" in str(exc_info.value)

    def test_invalid_name_with_special_chars(self):
        """특수문자 포함 이름 무효."""
        with pytest.raises(ValidationError) as exc_info:
            MemberConnectRequest(
                agreements=AgreementsSchema(terms=True, privacy=True),
                name="홍길동!@#",
            )
        assert "이름은 한글 또는 영문만 가능합니다" in str(exc_info.value)

    def test_name_too_short(self):
        """이름 최소 길이 미달."""
        with pytest.raises(ValidationError) as exc_info:
            MemberConnectRequest(
                agreements=AgreementsSchema(terms=True, privacy=True),
                name="홍",  # 1자
            )
        assert "String should have at least 2 characters" in str(exc_info.value)

    def test_valid_phone_10_digits(self):
        """010 핸드폰 번호 (10자리)."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
            phone="+82101234567",  # 9자리
        )
        assert data.phone == "+82101234567"

    def test_valid_phone_11_digits(self):
        """010 핸드폰 번호 (11자리)."""
        data = MemberConnectRequest(
            agreements=AgreementsSchema(terms=True, privacy=True),
            phone="+821012345678",  # 10자리
        )
        assert data.phone == "+821012345678"

    def test_invalid_phone_format(self):
        """잘못된 전화번호 형식."""
        with pytest.raises(ValidationError) as exc_info:
            MemberConnectRequest(
                agreements=AgreementsSchema(terms=True, privacy=True),
                phone="010-1234-5678",  # 하이픈 포함
            )
        assert "phone" in str(exc_info.value)


# ============================================================
# MemberConnectResponse 테스트
# ============================================================


class TestMemberConnectResponse:
    """MemberConnectResponse DTO 테스트."""

    def test_is_new_serialization(self):
        """is_new 필드가 isNew로 직렬화되는지 확인."""
        response = MemberConnectResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            status="ACTIVE",
            is_new=True,
        )
        json_data = response.model_dump(by_alias=True)
        assert "isNew" in json_data
        assert json_data["isNew"] is True


# ============================================================
# PasswordResetConfirm 테스트
# ============================================================


class TestPasswordResetConfirm:
    """PasswordResetConfirm DTO 테스트."""

    def test_valid_password_reset(self):
        """정상적인 비밀번호 재설정."""
        data = PasswordResetConfirm(
            password="NewPass1!",
            passwordConfirm="NewPass1!",
        )
        assert data.password == "NewPass1!"
        assert data.password_confirm == "NewPass1!"

    def test_password_validation_same_as_signup(self):
        """비밀번호 유효성 검사가 SignupRequest와 동일."""
        with pytest.raises(ValidationError) as exc_info:
            PasswordResetConfirm(
                password="nospecial1",  # 특수문자 누락
                passwordConfirm="nospecial1",
            )
        assert "특수문자를 포함해야 합니다" in str(exc_info.value)


# ============================================================
# AgreementsSchema 테스트
# ============================================================


class TestAgreementsSchema:
    """AgreementsSchema DTO 테스트."""

    def test_required_agreements(self):
        """필수 약관 동의."""
        data = AgreementsSchema(terms=True, privacy=True)
        assert data.terms is True
        assert data.privacy is True
        assert data.marketing is False  # 기본값

    def test_marketing_optional(self):
        """마케팅 동의 선택."""
        data = AgreementsSchema(terms=True, privacy=True, marketing=True)
        assert data.marketing is True

    def test_missing_required_field(self):
        """필수 필드 누락."""
        with pytest.raises(ValidationError):
            AgreementsSchema(terms=True)  # privacy 누락
