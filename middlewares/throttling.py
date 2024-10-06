import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

logger = logging.getLogger(__name__)

CACHE = TTLCache(maxsize=10_000, ttl=2)  # Максимальный размер кэша - 10000 ключей, а время жизни ключа - 5 секунд


class ThrottlingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user')

        if user.id in CACHE:
            logger.debug(f'Throttling for user {user.id}')
            return

        CACHE[user.id] = True

        return await handler(event, data)