import aiohttp
from bs4 import BeautifulSoup
from utils.logger import logger
from config import Config
import os
from typing import Optional
import re

class PinterestDownloader:
    @staticmethod
    async def download_pin(url: str) -> str:
        try:
            # Проверяем формат URL
            if not re.search(r'pinterest\.com/pin/[\w-]+', url):
                raise ValueError("Неверный формат ссылки на пин Pinterest")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            logger.info(f"Начинаем загрузку пина Pinterest: {url}")

            async with aiohttp.ClientSession(headers=headers) as session:
                # Получаем HTML страницы
                try:
                    async with session.get(url, timeout=Config.TIMEOUT) as response:
                        if response.status == 404:
                            raise ValueError("Пин не найден или был удален")
                        response.raise_for_status()
                        html = await response.text()
                except aiohttp.ClientError as e:
                    logger.error(f"Ошибка при получении страницы Pinterest: {str(e)}")
                    raise ValueError("Не удалось загрузить страницу пина")

                soup = BeautifulSoup(html, 'html.parser')
                meta_tag = soup.find('meta', {'property': 'og:image'})

                if not meta_tag or not meta_tag.get('content'):
                    logger.error("Не найдено изображение в мета-тегах")
                    raise ValueError("Не удалось найти изображение на странице Pinterest")

                image_url = meta_tag['content']
                logger.info(f"Найден URL изображения: {image_url}")

                # Скачиваем изображение
                try:
                    async with session.get(image_url, timeout=Config.TIMEOUT) as image_response:
                        if image_response.status == 404:
                            raise ValueError("Изображение не найдено или было удалено")
                        image_response.raise_for_status()
                        content = await image_response.read()

                        if len(content) > Config.MAX_FILE_SIZE:
                            raise ValueError("Размер файла превышает допустимый лимит (50 МБ)")

                        # Сохраняем изображение
                        output_path = os.path.join(Config.DOWNLOAD_PATH, 'pinterest')
                        os.makedirs(output_path, exist_ok=True)

                        pin_id = re.search(r'pin/([\w-]+)', url).group(1)
                        file_path = os.path.join(output_path, f"pin_{pin_id}.jpg")

                        with open(file_path, 'wb') as f:
                            f.write(content)

                        logger.info(f"Pinterest изображение успешно загружено: {file_path}")
                        return file_path

                except aiohttp.ClientError as e:
                    logger.error(f"Ошибка при скачивании изображения: {str(e)}")
                    raise ValueError("Не удалось скачать изображение")

        except ValueError as ve:
            logger.error(f"Ошибка в Pinterest загрузчике: {str(ve)}")
            raise ValueError(str(ve))
        except Exception as e:
            logger.error(f"Неожиданная ошибка в Pinterest загрузчике: {str(e)}")
            raise ValueError("Произошла ошибка при загрузке изображения")