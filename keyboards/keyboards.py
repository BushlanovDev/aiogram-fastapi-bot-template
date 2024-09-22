from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:

    def __init__(self):
        pass

    def get_start_button(self) -> ReplyKeyboardMarkup:
        kb_list = [
            [KeyboardButton(text='hi'), KeyboardButton(text='test')],
            [KeyboardButton(text='inline button'), KeyboardButton(text='fsm')],
        ]

        return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)

    def get_inline_button(self) -> InlineKeyboardMarkup:
        inline_kb_list = [
            [
                InlineKeyboardButton(text='Save', callback_data='save'),
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
