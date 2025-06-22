from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from db.models import Location


# Получить все локации по user_id
async def get_location_by_user_id(session: AsyncSession, user_id: int) -> list[str]:
    result = await session.execute(
        select(Location.name).where(Location.user_id == user_id)
    )
    return [row[0] for row in result.all()]

# Добавить новую локацию
async def add_user_location(session: AsyncSession, user_id: int, location_name: str) -> bool:
    new_location = Location(user_id=user_id, name=location_name)
    session.add(new_location)
    try:
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False

# Удалить локацию по user_id и имени
async def delete_user_location(session: AsyncSession, user_id: int, location_name: str):
    await session.execute(
        delete(Location).where(
            Location.user_id == user_id,
            Location.name == location_name
        )
    )
    await session.commit()
