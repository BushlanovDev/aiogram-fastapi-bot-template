from aiogram import BaseMiddleware

from bot.services.context import HandlerContext


class ContextMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['ctx'] = HandlerContext(
            lexicon=data['lexicon'],
            keyboards=data['keyboards'],
            bot_service=data['bot_service'],
        )

        return await handler(event, data)
