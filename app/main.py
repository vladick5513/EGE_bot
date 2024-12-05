import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.handlers.scores import router as scores_handlers
from app.handlers.auth import router as auth_handlers

# Создание бота
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Функция для запуска бота
async def main():
    dp.include_routers(scores_handlers, auth_handlers)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

