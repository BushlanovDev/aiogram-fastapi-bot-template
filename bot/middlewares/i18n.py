from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class I18nMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        data['user_lang'] = user.language_code

        return await handler(event, data)
