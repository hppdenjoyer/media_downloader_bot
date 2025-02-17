import asyncio
import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.client.bot import DefaultBotProperties
from aiohttp import web
from config import Config
from handlers import start_handler, help_handler, download_handler
from utils.logger import logger
import os

# Initialize bot
bot = Bot(
    token=Config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Initialize Redis
redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

# Register handlers
dp.message.register(start_handler, Command(commands=['start']))
dp.message.register(help_handler, Command(commands=['help']))
dp.message.register(download_handler, Command(commands=['download']))
dp.message.register(download_handler)  # Handle all messages as potential URLs


async def on_startup():
    """Setup actions on startup"""
    logger.info("Bot started")
    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)

    # Set webhook if enabled
    if Config.WEBHOOK_ENABLED:
        await bot.set_webhook(
            url=Config.WEBHOOK_URL + Config.WEBHOOK_PATH,
            drop_pending_updates=True
        )
        logger.info(f"Webhook set to {Config.WEBHOOK_URL + Config.WEBHOOK_PATH}")


async def on_shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
    if Config.WEBHOOK_ENABLED:
        await bot.delete_webhook()
    await redis_client.close()
    await bot.session.close()


async def main():
    logger.info("Starting bot...")

    if Config.WEBHOOK_ENABLED:
        # Setup webhook
        app = web.Application()
        handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )
        handler.register(app, path=Config.WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)

        # Setup startup and shutdown handlers
        app.on_startup.append(lambda _: on_startup())
        app.on_shutdown.append(lambda _: on_shutdown())

        # Start webhook
        logger.info(f"Starting webhook on {Config.WEBHOOK_HOST}:{Config.WEBHOOK_PORT}")
        return await web._run_app(
            app,
            host=Config.WEBHOOK_HOST,
            port=Config.WEBHOOK_PORT
        )
    else:
        # Start polling
        logger.info("Starting polling...")
        await dp.start_polling(
            bot,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )


if __name__ == '__main__':
    asyncio.run(main())
