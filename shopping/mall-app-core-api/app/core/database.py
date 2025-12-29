from collections.abc import Callable
from contextvars import ContextVar
from functools import wraps
from typing import ParamSpec, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

_current_session: ContextVar[AsyncSession | None] = ContextVar("current_session", default=None)


def get_session() -> AsyncSession:
    """현재 컨텍스트의 DB 세션을 반환."""
    session = _current_session.get()
    if session is None:
        raise RuntimeError("세션이 없습니다. @with_session 데코레이터를 사용하세요.")
    return session


P = ParamSpec("P")
T = TypeVar("T")


def with_session(func: Callable[P, T]) -> Callable[P, T]:
    """Service 메서드에 트랜잭션 세션을 제공하는 데코레이터."""

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        async with async_session_maker() as session:
            token = _current_session.set(session)
            try:
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                _current_session.reset(token)

    return wrapper  # type: ignore
