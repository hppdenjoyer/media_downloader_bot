import os
from dataclasses import dataclass

@dataclass
class Config:
    # Telegram Bot Token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "bot.log"

    # Download settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB in bytes
    DOWNLOAD_PATH: str = "downloads"

    # Request timeout
    TIMEOUT: int = 10  # seconds

    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # Webhook settings
    WEBHOOK_ENABLED: bool = os.getenv("WEBHOOK_ENABLED", "false").lower() == "true"
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8443"))
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")