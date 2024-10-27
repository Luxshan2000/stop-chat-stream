from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from be.db.models import AbortSignal


async def get_by_id(session: AsyncSession, id: str) -> AbortSignal:
    """Retrieve an AbortSignal record by ID."""
    result = await session.execute(select(AbortSignal).filter_by(id=id))
    abort_signal = result.scalars().first()
    return abort_signal


async def delete_by_id(session: AsyncSession, id: str) -> bool:
    """Delete an AbortSignal record by ID."""
    abort_signal = await get_by_id(session, id)
    if not abort_signal:
        return False
    await session.delete(abort_signal)
    await session.commit()
    return True


async def insert(session: AsyncSession, id: str, flag: bool = False) -> AbortSignal:
    """Insert a new AbortSignal record."""
    new_abort_signal = AbortSignal(id=id, flag=flag)
    session.add(new_abort_signal)
    await session.commit()
    await session.refresh(new_abort_signal)
    return new_abort_signal


async def update_flag_by_id(session: AsyncSession, id: str, new_flag: bool) -> bool:
    """Update the flag of an AbortSignal record by ID."""
    abort_signal = await get_by_id(session, id)
    if not abort_signal:
        return False
    abort_signal.flag = new_flag
    await session.commit()
    await session.flush()
    return True
