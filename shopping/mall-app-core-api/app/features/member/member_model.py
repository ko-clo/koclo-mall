"""회원 관련 SQLAlchemy 모델."""

from __future__ import annotations

import enum
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MemberStatus(str, enum.Enum):
    """회원 상태."""

    PENDING = "PENDING"  # 이메일 인증 대기
    ACTIVE = "ACTIVE"  # 활성
    DORMANT = "DORMANT"  # 휴면 (1년간 미로그인)
    SUSPENDED = "SUSPENDED"  # 정지
    WITHDRAWN = "WITHDRAWN"  # 탈퇴


class Member(Base):
    """회원 운영정보 테이블.

    Supabase auth.users와 1:1 관계.
    개인정보는 MemberProfile에 별도 저장.
    """

    __tablename__ = "members"

    # PK = Supabase auth.users.id
    id: Mapped[UUID] = mapped_column(primary_key=True)

    # 서비스 운영 정보 (개인정보 아님)
    status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus, native_enum=False),
        default=MemberStatus.ACTIVE,
    )
    marketing_agreed: Mapped[bool] = mapped_column(Boolean, default=False)
    terms_agreed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    privacy_agreed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 탈퇴 정보
    withdrawn_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    withdrawal_reason: Mapped[str | None] = mapped_column(String(20), nullable=True)
    personal_info_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # 메타데이터
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    profile: Mapped[MemberProfile | None] = relationship(
        back_populates="member",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )


class MemberProfile(Base):
    """회원 개인정보 테이블.

    탈퇴 시 5일 이내 삭제 대상.
    """

    __tablename__ = "member_profiles"

    member_id: Mapped[UUID] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # 개인정보 (탈퇴 시 삭제 대상)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    profile_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 메타데이터
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    member: Mapped[Member] = relationship(back_populates="profile")
