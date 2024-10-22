import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

logger = logging.getLogger(__name__)

CACHE = TTLCache(maxsize=10_000, ttl=2)  # Максимальный размер кэша - 10000 ключей, время жизни ключа - 2 секунды


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is not None:
            if user.id in CACHE:
                logger.debug(f'Throttling for user {user.id}')
                return

            CACHE[user.id] = True

        return await handler(event, data)
