from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import db.models as db
import models.notification as model

async def get_user_notifications(session: AsyncSession, user_id: int) -> list[model.Notification]:
    result = await session.execute(
        select(db.Notification).where(db.Notification.user_id == user_id)
    )
    rows = result.scalars().all()
    return [
        model.Notification(
            user_id=row.user_id,
            time=row.time,
            mode=row.mode
        )
        for row in rows
    ]

async def get_notifications(session: AsyncSession) -> list[model.Notification]:
    result = await session.execute(
        select(db.Notification)
    )
    rows = result.scalars().all()
    return [
        model.Notification(
            user_id=row.user_id,
            time=row.time,
            mode=row.mode
        )
        for row in rows
    ]

async def add_notification(session: AsyncSession, notif: model.Notification) -> bool:
    try:
        session.add(db.Notification(user_id=notif.user_id, time=notif.time, mode=notif.mode))
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False

async def delete_notification(session: AsyncSession, notif: model.Notification):
    await session.execute(
        delete(db.Notification).where(
            db.Notification.user_id == notif.user_id,
            db.Notification.time == notif.time,
            db.Notification.mode == notif.mode
        )
    )
    await session.commit()
