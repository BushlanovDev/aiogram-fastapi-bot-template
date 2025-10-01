from aiogram import BaseMiddleware

from bot.services.context import HandlerContext


class ContextMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['ctx'] = HandlerContext(
            lexicon=data['lexicon'],
            keyboards=data['keyboards'],
            bot_service=data['bot_service'],
            web_app_url=data['web_app_url'],
        )

        return await handler(event, data)
