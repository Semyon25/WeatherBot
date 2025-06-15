from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Location


async def get_location_by_user_id(session: AsyncSession,
                                       user_id: int) -> str | None:
    stmt = select(Location.name).where(Location.user_id == user_id)
    result = await session.execute(stmt)
    name = result.scalar_one_or_none()
    return name


async def upsert_location(session, user_id: int, location_name: str):
    stmt = select(Location).where(Location.user_id == user_id)
    result = await session.execute(stmt)
    location = result.scalar_one_or_none()

    if location:
        location.name = location_name
    else:
        location = Location(user_id=user_id, name=location_name)
        session.add(location)

    await session.commit()