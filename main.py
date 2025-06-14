import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers import start, weather
from scheduler.job import start_scheduler


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем хендлеры
    dp.include_routers(start.router, weather.router)

    # Запускаем планировщик
    asyncio.create_task(start_scheduler(bot))

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
