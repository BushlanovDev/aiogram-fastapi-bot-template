from typing import Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class App(BaseSettings):
    debug: bool = True
    port: int = 8080
    url: str = 'https://my.domain'
    webhook_path: str = '/webhook/tg'
    default_language: str = 'en'


class TgBot(BaseSettings):
    token: SecretStr


class Settings(BaseSettings):
    app: App
    tg_bot: TgBot
    logging: dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(levelname)-8s [%(asctime)s] [%(name)s] %(message)s',
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'main': {
                'handlers': ['default'],
                'level': 'DEBUG',
            },
        },
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
