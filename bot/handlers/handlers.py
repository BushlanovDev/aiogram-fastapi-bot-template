from typing import Optional

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.callbacks.callback import SaveCallbackFactory
from bot.keyboards.keyboards import Keyboards
from bot.services.bot_service import BotService
from bot.states.bot_state import BotState


class Handlers:

    def __init__(self, bot: Bot, kb: Keyboards, bot_service: BotService):
        self.bot = bot
        self.kb = kb
        self.bot_service = bot_service

    async def start_command(self, message: Message):
        await message.answer(text='Hi user! This start message.', reply_markup=self.kb.get_start_button())

    async def help_command(self, message: Message):
        await message.answer(text='This help message.')

    async def answer(self, message: Message, answer: str):
        await self.__send_message(message.chat.id, answer, message.message_id)

    async def answer_fsm(self, message: Message, state: FSMContext):
        await message.answer('Waiting Step 1')
        await state.set_state(BotState.waiting_step_1)

    async def answer_fsm_state_1(self, message: Message, state: FSMContext):
        await state.update_data(step_1=message.text)
        await message.answer('Waiting Step 2')
        await state.set_state(BotState.waiting_step_2)

    async def answer_fsm_state_2(self, message: Message, state: FSMContext):
        await state.update_data(step_2=message.text)
        data = await  state.get_data()
        await message.answer(f"Step 1: {data['step_1']}\n" f"Step 2: {data['step_2']}")
        await state.clear()

    async def answer_inline_button(self, message: Message):
        callback = SaveCallbackFactory(message_id=message.message_id).pack()
        await message.answer(text='This help message', reply_markup=self.kb.get_inline_button(callback_data=callback))

    async def reply(self, message: Message):
        await message.reply(text=self.bot_service.upper(message.text))

    async def process_any_inline_button_press(self, callback: CallbackQuery, callback_data: SaveCallbackFactory):
        await callback.message.answer(text=callback_data.pack())
        await callback.answer()

    async def __send_message(self, chat_id: int, text: str, reply_to_message_id: Optional[int] = None) -> int:
        await self.bot.send_chat_action(chat_id, ChatAction.TYPING)
        message = await self.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)

        return message.message_id
