from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.callback import SaveCallbackFactory
from bot.services.context import HandlerContext
from bot.states.bot_state import BotState


class Handlers:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def start_command(self, message: Message, ctx: HandlerContext, user_lang: str | None):
        await message.answer(
            text=ctx.lexicon.get_text('start_message', user_lang),
            reply_markup=ctx.keyboards.get_start_button(ctx.lexicon, user_lang),
        )

    async def help_command(self, message: Message, ctx: HandlerContext, user_lang: str | None):
        await message.answer(text=ctx.lexicon.get_text('help_message', user_lang))

    async def webapp_command(self, message: Message, ctx: HandlerContext, user_lang: str | None):
        await message.answer(
            text=ctx.lexicon.get_text('webapp_message', user_lang),
            reply_markup=ctx.keyboards.get_webapp_button(ctx.lexicon, user_lang, ctx.web_app_url),
        )

    async def answer(self, message: Message, ctx: HandlerContext, user_lang: str | None):
        text = ctx.lexicon.get_text('default_answer', user_lang)
        await self.__send_message(message.chat.id, text, message.message_id)

    async def answer_fsm(self, message: Message, state: FSMContext, ctx: HandlerContext, user_lang: str | None):
        await message.answer(ctx.lexicon.get_text('fsm_wait_step_1', user_lang))
        await state.set_state(BotState.waiting_step_1)

    async def answer_fsm_state_1(self, message: Message, state: FSMContext, ctx: HandlerContext, user_lang: str | None):
        await state.update_data(step_1=message.text)
        await message.answer(ctx.lexicon.get_text('fsm_wait_step_2', user_lang))
        await state.set_state(BotState.waiting_step_2)

    async def answer_fsm_state_2(self, message: Message, state: FSMContext, ctx: HandlerContext, user_lang: str | None):
        await state.update_data(step_2=message.text)
        data = await state.get_data()
        await message.answer(
            ctx.lexicon.get_text('fsm_result', user_lang).format(
                step_1=data.get('step_1', ''),
                step_2=data.get('step_2', ''),
            )
        )
        await state.clear()

    async def answer_inline_button(self, message: Message, ctx: HandlerContext, user_lang: str | None):
        callback = SaveCallbackFactory(message_id=message.message_id).pack()
        await message.answer(
            text=ctx.lexicon.get_text('inline_prompt', user_lang),
            reply_markup=ctx.keyboards.get_inline_button(ctx.lexicon, user_lang, callback),
        )

    async def reply(self, message: Message, ctx: HandlerContext):
        text = message.text or ''
        await message.reply(text=ctx.bot_service.upper(text))

    async def process_any_inline_button_press(self, callback: CallbackQuery, callback_data: SaveCallbackFactory):
        text = f'Callback packed: {callback_data.pack()}'
        if callback.message:
            await callback.message.answer(text=text)
            await callback.answer()
        else:
            await callback.answer(text=text, show_alert=True)

    async def __send_message(self, chat_id: int, text: str, reply_to_message_id: int | None = None) -> int:
        await self.bot.send_chat_action(chat_id, ChatAction.TYPING)
        message = await self.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)

        return message.message_id
