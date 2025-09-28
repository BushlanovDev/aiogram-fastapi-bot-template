import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, Update, User
from cachetools import TTLCache

logger = logging.getLogger('main')

CACHE = TTLCache(maxsize=10_000, ttl=2)


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
                text = 'Too many requests. Please slow down.'
                lexicon = data.get('lexicon')
                if lexicon is not None:
                    text = lexicon.get_text('throttled_message', data.get('user_lang'))
                await self._notify_throttled(event, text)
                return

            CACHE[user.id] = True

        return await handler(event, data)

    @staticmethod
    async def _notify_throttled(event: TelegramObject, text: str) -> None:
        if isinstance(event, Message):
            await event.answer(text)
            return

        if isinstance(event, CallbackQuery):
            if event.message is not None:
                await event.message.answer(text)
            await event.answer()
            return

        if isinstance(event, Update):
            if event.message is not None:
                await event.message.answer(text)
                return
            if event.callback_query is not None:
                if event.callback_query.message is not None:
                    await event.callback_query.message.answer(text)
                await event.callback_query.answer()
                return

        logger.debug('Throttling notification skipped: unsupported event type %s', type(event))
