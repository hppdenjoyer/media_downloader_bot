import yt_dlp
from utils.logger import logger
from config import Config
import os
from typing import Optional
import re


class YouTubeDownloader:
    @staticmethod
    def _extract_video_id(url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:be\/)([0-9A-Za-z_-]{11}).*'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Неверный формат ссылки на YouTube видео")

    @staticmethod
    async def download_video(url: str) -> str:
        try:
            video_id = YouTubeDownloader._extract_video_id(url)
            logger.info(f"Попытка загрузки YouTube видео с ID: {video_id}")

            output_path = os.path.join(Config.DOWNLOAD_PATH, 'youtube')
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, f"{video_id}.mp4")

            ydl_opts = {
                'format': 'best[filesize<50M]/best',
                'outtmpl': output_file,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'no_color': True,
                'geo_bypass': True,
                'noprogress': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                if "Video unavailable" in str(e):
                    raise ValueError("Видео недоступно или было удалено")
                elif "Private video" in str(e):
                    raise ValueError("Это приватное видео")
                elif "Sign in" in str(e):
                    raise ValueError("Видео требует авторизации")
                elif "exceeds maximum length" in str(e) or "larger than max-filesize" in str(e):
                    raise ValueError("Видео слишком большое (максимум 50 МБ)")
                else:
                    raise ValueError(f"Ошибка при загрузке видео: {str(e)}")

            if not os.path.exists(output_file):
                raise ValueError("Не удалось загрузить видео")

            if os.path.getsize(output_file) > Config.MAX_FILE_SIZE:
                os.remove(output_file)
                raise ValueError("Размер видео превышает допустимый лимит (50 МБ)")

            logger.info(f"Видео с YouTube успешно загружено: {output_file}")
            return output_file

        except ValueError as ve:
            logger.error(f"Ошибка в YouTube загрузчике: {str(ve)}")
            raise ve
        except Exception as e:
            logger.error(f"Неожиданная ошибка в YouTube загрузчике: {str(e)}")
            raise ValueError("Произошла ошибка при загрузке видео")

    @staticmethod
    async def download_audio(url: str) -> str:
        try:
            video_id = YouTubeDownloader._extract_video_id(url)
            logger.info(f"Попытка загрузки аудио с YouTube видео ID: {video_id}")

            output_path = os.path.join(Config.DOWNLOAD_PATH, 'youtube')
            os.makedirs(output_path, exist_ok=True)
            output_file = os.path.join(output_path, f"{video_id}.mp3")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_file,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'no_color': True,
                'geo_bypass': True,
                'noprogress': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                if "Video unavailable" in str(e):
                    raise ValueError("Видео недоступно или было удалено")
                elif "Private video" in str(e):
                    raise ValueError("Это приватное видео")
                elif "Sign in" in str(e):
                    raise ValueError("Видео требует авторизации")
                else:
                    raise ValueError(f"Ошибка при загрузке аудио: {str(e)}")

            if not os.path.exists(output_file):
                raise ValueError("Не удалось загрузить аудио")

            if os.path.getsize(output_file) > Config.MAX_FILE_SIZE:
                os.remove(output_file)
                raise ValueError("Размер аудио превышает допустимый лимит (50 МБ)")

            logger.info(f"Аудио с YouTube успешно загружено: {output_file}")
            return output_file

        except ValueError as ve:
            logger.error(f"Ошибка в YouTube загрузчике: {str(ve)}")
            raise ve
        except Exception as e:
            logger.error(f"Неожиданная ошибка в YouTube загрузчике: {str(e)}")
            raise ValueError("Произошла ошибка при загрузке аудио")
