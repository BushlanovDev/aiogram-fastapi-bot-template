from bot.i18n.en import LEXICON_EN
from bot.i18n.ru import LEXICON_RU


class Lexicon:
    def __init__(self, default_language: str):
        self.default_language = default_language

    def get_text(self, param: str, lang: str | None = None) -> str:
        if lang is None:
            lang = self.default_language

        match lang:
            case 'ru':
                ret = LEXICON_RU.get(param, param)
            case 'en':
                ret = LEXICON_EN.get(param, param)
            case _:
                ret = LEXICON_EN.get(param, param)

        return ret
