import logging
from typing import Callable, Optional

import uvicorn
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Update
from fastapi import FastAPI
from fastapi.requests import Request

from bot.callbacks.callback import SaveCallbackFactory
from bot.configs.config import App, Settings, TgBot
from bot.handlers.handlers import Handlers
from bot.keyboards.keyboards import Keyboards
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.services.bot_service import BotService
from bot.states.bot_state import BotState

logger = logging.getLogger('main')


def create_startup_handler(bot: Bot, dp: Dispatcher, url: str) -> Callable:
    async def startup_handler() -> None:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != url:
            await bot.set_webhook(
                url=url,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True,
            )

        await bot.set_my_commands(
            [
                BotCommand(command='/help', description='Help'),
            ]
        )

        logger.debug('startup_handler')

    return startup_handler


def create_shutdown_handler(bot: Bot, debug: bool) -> Callable:
    async def shutdown_handler() -> None:
        if debug:
            await bot.delete_webhook()
        logger.debug('shutdown_handler')

    return shutdown_handler


def create_webhook_handler(bot: Bot, dp: Dispatcher) -> Callable:
    async def webhook_handler(request: Request) -> None:
        try:
            update = Update.model_validate(await request.json(), context={'bot': bot})
            logger.info(f'Received update: {update.update_id}')
            await dp.feed_update(bot, update)
            logger.debug(f'Successfully processed update: {update.update_id}')
        except Exception as e:
            logger.error(f'Failed to process update: {str(e)}')
            raise

    return webhook_handler


def create_bot(settings: TgBot) -> Bot:
    return Bot(token=settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def create_dispatcher(storage: Optional[BaseStorage] = None) -> Dispatcher:
    return Dispatcher(storage=storage)


def register_handlers(dp: Dispatcher, hd: Handlers) -> None:
    dp.message.register(hd.start_command, CommandStart())
    dp.message.register(hd.help_command, Command(commands='help'))
    dp.message.register(hd.answer, F.text == 'hi')
    dp.message.register(hd.answer_inline_button, F.text == 'inline button')
    dp.message.register(hd.answer_fsm, F.text == 'fsm')
    dp.message.register(hd.answer_fsm_state_1, BotState.waiting_step_1)
    dp.message.register(hd.answer_fsm_state_2, BotState.waiting_step_2)
    dp.message.register(hd.reply)
    dp.callback_query.register(hd.process_any_inline_button_press, SaveCallbackFactory.filter())


def register_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(ThrottlingMiddleware())


def register_workflow_data(dp: Dispatcher) -> None:
    dp.workflow_data.update({'answer': 'Hello'})


def create_app(bot: Bot, dp: Dispatcher, settings: App) -> FastAPI:
    app = FastAPI()
    app.add_event_handler('startup', create_startup_handler(bot, dp, settings.url + settings.webhook_path))
    app.add_event_handler('shutdown', create_shutdown_handler(bot, settings.debug))
    app.add_api_route(settings.webhook_path, create_webhook_handler(bot, dp), methods=['POST'])

    return app


def main() -> None:
    settings = Settings()

    logging.config.dictConfig(settings.logging)

    bot = create_bot(settings.tg_bot)
    dp = create_dispatcher(MemoryStorage())
    app = create_app(bot, dp, settings.app)
    register_handlers(dp, Handlers(bot, Keyboards(), BotService()))
    register_middlewares(dp)
    register_workflow_data(dp)

    logger.debug('Application is running')

    uvicorn.run(app, host='0.0.0.0', port=settings.app.port)


if __name__ == '__main__':
    main()
