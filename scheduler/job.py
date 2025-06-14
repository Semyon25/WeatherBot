from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from config import USER_ID
from services.weather import get_weather
from datetime import time
import pytz


async def send_weather(bot: Bot):
  weather = await get_weather()
  await bot.send_message(USER_ID, weather)


async def start_scheduler(bot: Bot):
  scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))
  scheduler.add_job(send_weather, "cron", hour=10, minute=00, args=[bot])
  scheduler.start()
