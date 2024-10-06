from typing import Any, Dict

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class App(BaseSettings):
    port: int = 8080
    url: str = 'https://my.domain'
    webhook_path: str = '/webhook/tg'


class TgBot(BaseSettings):
    token: SecretStr


class Settings(BaseSettings):
    app: App
    tg_bot: TgBot
    logging: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '%(levelname)-8s [%(asctime)s] [%(name)s] %(message)s',
            },
            'uvicorn_access': {
                'format': '%(levelname)-8s [%(asctime)s] [%(name)s] - %(client_addr)s - "%(request_line)s" %(status_code)s',
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
