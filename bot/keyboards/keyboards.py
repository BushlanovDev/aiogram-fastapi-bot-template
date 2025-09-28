from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from bot.i18n.lexicon import Lexicon


class Keyboards:
    def __init__(self):
        pass

    def get_start_button(self, lexicon: Lexicon, user_lang: str | None) -> ReplyKeyboardMarkup:
        kb_list = [
            [
                KeyboardButton(text=lexicon.get_text('start_button_hi', user_lang)),
                KeyboardButton(text=lexicon.get_text('start_button_test', user_lang)),
            ],
            [
                KeyboardButton(text=lexicon.get_text('start_button_inline', user_lang)),
                KeyboardButton(text=lexicon.get_text('start_button_fsm', user_lang)),
            ],
        ]

        return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)

    def get_inline_button(
        self, lexicon: Lexicon, user_lang: str | None, callback_data: str | None = None
    ) -> InlineKeyboardMarkup:
        inline_kb_list = [
            [
                InlineKeyboardButton(
                    text=lexicon.get_text('inline_save_button', user_lang),
                    callback_data=callback_data,
                ),
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
