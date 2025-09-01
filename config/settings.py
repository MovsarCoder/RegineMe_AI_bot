import os
from dotenv import load_dotenv

load_dotenv()


class GetTokenBot:
    BOT_TOKEN: str
    BOT_TOKEN = os.getenv("BOT_TOKEN")


class GetTechSupport:
    TECH_SUPPORT: str
    TECH_SUPPORT = os.getenv("TECH_SUPPORT")


class GetBotName:
    BOT_NAME: str
    BOT_USERNAME: str

    BOT_NAME = os.getenv("BOT_NAME")
    BOT_USERNAME = os.getenv("BOT_USERNAME")


class YooKassaInfo:
    PAY_TOKEN: str
    SHOP_ID: int

    PAY_TOKEN = os.getenv("PAYMENT_TOKEN")
    SHOP_ID = os.getenv("SHOP_ID")


class RedisConfig:
    """Конфигурация Redis для кеширования"""
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "")

    # Настройки кеширования
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # Время жизни кеша в секундах (по умолчанию 1 час)
    CACHE_PREFIX: str = os.getenv("CACHE_PREFIX", "bot_cache:")

    @classmethod
    def get_redis_url(cls) -> str:
        """Получить URL для подключения к Redis"""
        if cls.REDIS_URL:
            return cls.REDIS_URL

        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"

        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
