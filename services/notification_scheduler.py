from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from datetime import datetime
from services.weather import get_weather
from db.database import get_session
import db.notifications as db_notifications
import db.locations as db_locations

WEEKDAY_MODES = {
    "daily": lambda _: True,
    "weekdays": lambda dt: dt.weekday() < 5,
    "weekends": lambda dt: dt.weekday() >= 5,
}

scheduler = AsyncIOScheduler()

async def setup_scheduler(bot: Bot):
  scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))
  scheduler.add_job(send_scheduled_notifications, CronTrigger(minute="*"), args=[bot])
  scheduler.start()

async def send_scheduled_notifications(bot: Bot):
    moscow_tz = ZoneInfo("Europe/Moscow")
    now = datetime.now(moscow_tz)
    current_time = now.strftime("%H:%M")
    async with get_session() as session:
        notifications = await db_notifications.get_notifications(session)
        for notif in notifications:
            if notif.time != current_time:
                continue
            if not WEEKDAY_MODES.get(notif.mode, lambda _: False)(now):
                continue
            locations = await db_locations.get_location_by_user_id(session, notif.user_id)
            await send_weather(bot,notif.user_id, locations)

async def send_weather(bot: Bot, user_id: int, locations: list[str]):
    for loc in locations:
        weather = await get_weather(loc)
        await bot.send_message(user_id, weather, parse_mode="HTML")