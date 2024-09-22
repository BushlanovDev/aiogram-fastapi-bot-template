from pydantic import SecretStr
from pydantic_settings import BaseSettings


class App(BaseSettings):
    port: int = 80
    url: str = 'https://my.domain'
    webhook_path: str = '/webhook/tg'


class TgBot(BaseSettings):
    token: SecretStr


class Settings(BaseSettings):
    app: App
    tg_bot: TgBot

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
