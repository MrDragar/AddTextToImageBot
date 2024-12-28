import asyncio
import logging
from aiogram import Bot, Dispatcher

from src.handlers import router
from src import config
from src.services import init_cloudinary


async def main():
    logging.basicConfig(
        level=config.log_level,
        format=config.log_format,
        filename=config.log_file,
        filemode="a"
    )
    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await init_cloudinary(
        cloud_name=config.CLOUD_NAME, api_key=config.CLOUDINARY_API_SECRET,
        api_secret=config.CLOUDINARY_API_SECRET
    )
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
