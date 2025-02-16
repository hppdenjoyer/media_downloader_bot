import aiohttp
from utils.logger import logger
from config import Config
import os
import re
from typing import Optional

class TikTokDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from TikTok URL."""
        patterns = [
            r'tiktok\.com/.*?/video/(\d+)',
            r'tiktok\.com/v/(\d+)',
            r'vm\.tiktok\.com/(\w+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Неверный формат ссылки на видео TikTok")

    async def download_video(self, url: str) -> str:
        try:
            video_id = self._extract_video_id(url)
            logger.info(f"Попытка загрузки видео TikTok с ID: {video_id}")

            # Используем yt-dlp для загрузки видео
            import yt_dlp

            output_path = os.path.join(Config.DOWNLOAD_PATH, 'tiktok')
            os.makedirs(output_path, exist_ok=True)
            
            file_path = os.path.join(output_path, f"video_{video_id}.mp4")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': file_path,
                'quiet': True,
                'no_warnings': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size > Config.MAX_FILE_SIZE:
                        os.remove(file_path)
                        raise ValueError("Размер файла превышает допустимый лимит (50 МБ)")
                    
                    logger.info(f"Видео TikTok успешно загружено: {file_path}")
                    return file_path
                else:
                    raise ValueError("Не удалось загрузить видео")

            except Exception as e:
                logger.error(f"Ошибка при загрузке видео через yt-dlp: {str(e)}")
                raise ValueError("Не удалось загрузить видео из TikTok")

        except ValueError as ve:
            logger.error(f"Ошибка в TikTok загрузчике: {str(ve)}")
            raise ValueError(str(ve))
        except Exception as e:
            logger.error(f"Неожиданная ошибка в TikTok загрузчике: {str(e)}")
            raise ValueError("Произошла ошибка при загрузке видео")
