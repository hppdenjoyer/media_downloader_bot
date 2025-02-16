from aiogram import types
from aiogram.filters import Command

async def start_handler(message: types.Message):
    """Handle /start command"""
    welcome_text = """
Привет! 👋 Я бот для скачивания медиафайлов!

Я могу помочь тебе скачать медиа с:
• YouTube 🎥
• TikTok 📱
• Pinterest 🖼️

Просто отправь мне ссылку, и я сделаю всё остальное!

Используй /help для просмотра всех доступных команд.
    """
    await message.answer(welcome_text)

async def help_handler(message: types.Message):
    """Handle /help command"""
    help_text = """
Доступные команды:
/start - Запустить бота
/help - Показать это сообщение
/download [ссылка] - Скачать медиафайл по ссылке

Поддерживаемые платформы:
• YouTube: видео и аудио
• TikTok: видео
• Pinterest: фото и видео

Как использовать:
1. Отправь мне ссылку напрямую
2. Или используй команду /download со ссылкой

Примеры:
• /download https://youtube.com/watch?v=...
• https://tiktok.com/@user/video/...
    """
    await message.answer(help_text)