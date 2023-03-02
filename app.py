from loader import bot, db_start, AuthMiddleware
import asyncio
from handlers.users.works import scheduler


async def on_shutdown(dp):
    await bot.close()

async def on_startup(_):
    await db_start()
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.middleware.setup(AuthMiddleware())
    executor.start_polling(dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)