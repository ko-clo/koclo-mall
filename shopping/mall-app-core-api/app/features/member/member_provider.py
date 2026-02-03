"""Member Provider - DB CRUD only."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from app.core.database import get_session
from app.features.member.member_model import Member, MemberProfile, MemberStatus


class MemberProvider:
    """회원 DB 접근 Provider (Singleton)."""

    async def find_by_id(self, member_id: UUID) -> Member | None:
        """ID로 회원 조회."""
        session = get_session()
        result = await session.execute(select(Member).where(Member.id == member_id))
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> MemberProfile | None:
        """이메일로 프로필 조회."""
        session = get_session()
        result = await session.execute(
            select(MemberProfile).where(MemberProfile.email == email)
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        """이메일 존재 여부 확인."""
        result = await self.find_by_email(email)
        return result is not None

    async def create_member(
        self,
        member_id: UUID,
        status: MemberStatus,
        marketing_agreed: bool,
        terms_agreed_at: datetime,
        privacy_agreed_at: datetime,
    ) -> Member:
        """회원 생성."""
        session = get_session()
        member = Member(
            id=member_id,
            status=status,
            marketing_agreed=marketing_agreed,
            terms_agreed_at=terms_agreed_at,
            privacy_agreed_at=privacy_agreed_at,
        )
        session.add(member)
        await session.flush()
        return member

    async def create_profile(
        self,
        member_id: UUID,
        email: str,
        name: str,
        phone: str | None = None,
    ) -> MemberProfile:
        """프로필 생성."""
        session = get_session()
        profile = MemberProfile(
            member_id=member_id,
            email=email,
            name=name,
            phone=phone,
        )
        session.add(profile)
        await session.flush()
        return profile

    async def update_member(
        self,
        member: Member,
        **kwargs,
    ) -> Member:
        """회원 정보 업데이트."""
        session = get_session()
        for key, value in kwargs.items():
            if hasattr(member, key) and value is not None:
                setattr(member, key, value)
        await session.flush()
        return member

    async def update_profile(
        self,
        profile: MemberProfile,
        **kwargs,
    ) -> MemberProfile:
        """프로필 업데이트."""
        session = get_session()
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        await session.flush()
        return profile
