from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from config import ADMIN_ID
from services.weather import get_weather
from datetime import time
import pytz


async def send_weather(bot: Bot):
  weather = await get_weather('Москва')
  await bot.send_message(ADMIN_ID, weather, parse_mode="HTML")


async def start_scheduler(bot: Bot):
  scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))
  scheduler.add_job(send_weather, "cron", hour=10, minute=00, args=[bot])
  scheduler.start()
