import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers import start, weather
from scheduler.job import start_scheduler
from db.database import create_tables
from routers import setup_routers

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await create_tables()

    # Регистрируем хендлеры
    dp.include_router(setup_routers())

    # Запускаем планировщик
    asyncio.create_task(start_scheduler(bot))

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
