from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import User

async def add_user(session: AsyncSession, user_id: int, username: str, first_name: str, last_name: str):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        new_user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        session.add(new_user)
        await session.commit()
