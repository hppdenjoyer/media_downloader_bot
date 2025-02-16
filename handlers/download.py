from aiogram import types
from aiogram.types import FSInputFile
from utils.helpers import get_platform, is_valid_url
from utils.logger import logger
from services.youtube import YouTubeDownloader
from services.tiktok import TikTokDownloader
from services.pinterest import PinterestDownloader
import os

async def download_handler(message: types.Message):
    """Handle media download requests"""
    try:
        # Extract URL from message
        url = message.text
        if message.text.startswith('/download'):
            # Remove command from text
            url = message.text.replace('/download', '').strip()

        if not url:
            await message.answer("Пожалуйста, отправьте ссылку на медиафайл или используйте команду /download <ссылка>")
            return

        if not is_valid_url(url):
            await message.answer("Пожалуйста, предоставьте действительную ссылку")
            return

        # Send processing message
        processing_msg = await message.answer("⏳ Обрабатываю ваш запрос...")
        logger.info(f"Processing download request for URL: {url}")

        # Determine platform and download
        platform = get_platform(url)
        logger.info(f"Detected platform: {platform}")
        file_path = None

        try:
            if platform == 'youtube':
                downloader = YouTubeDownloader()
                file_path = await downloader.download_video(url)
            elif platform == 'tiktok':
                downloader = TikTokDownloader()
                file_path = await downloader.download_video(url)
            elif platform == 'pinterest':
                downloader = PinterestDownloader()
                file_path = await downloader.download_pin(url)
            else:
                await message.answer("⚠️ Извините, эта платформа не поддерживается")
                return

            # Send the file
            if file_path and os.path.exists(file_path):
                try:
                    if file_path.endswith(('.mp4', '.mov')):
                        await message.answer_video(
                            FSInputFile(file_path),
                            caption="🎥 Вот ваше видео!"
                        )
                    elif file_path.endswith(('.mp3', '.m4a')):
                        await message.answer_audio(
                            FSInputFile(file_path),
                            caption="🎵 Вот ваше аудио!"
                        )
                    else:
                        await message.answer_photo(
                            FSInputFile(file_path),
                            caption="📸 Вот ваше фото!"
                        )
                    logger.info(f"Successfully sent file to user: {file_path}")
                except Exception as e:
                    logger.error(f"Error sending file to user: {str(e)}")
                    await message.answer("⚠️ Произошла ошибка при отправке файла. Возможно, файл слишком большой.")
                finally:
                    # Clean up
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"Cleaned up file: {file_path}")

            await processing_msg.delete()

        except ValueError as ve:
            error_message = str(ve)
            await message.answer(f"⚠️ {error_message}")
        except Exception as e:
            logger.error(f"Error downloading media: {str(e)}")
            await message.answer("⚠️ Произошла ошибка при загрузке. Пожалуйста, попробуйте позже.")

    except Exception as e:
        logger.error(f"Error in download handler: {str(e)}")
        await message.answer("⚠️ Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")

    finally:
        try:
            if 'processing_msg' in locals():
                await processing_msg.delete()
        except:
            pass