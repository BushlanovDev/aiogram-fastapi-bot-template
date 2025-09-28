from collections.abc import Mapping

from bot.i18n.en import LEXICON_EN
from bot.i18n.ru import LEXICON_RU


class Lexicon:
    def __init__(self, default_language: str):
        self.default_language = default_language
        self._lexicons: dict[str, Mapping[str, str]] = {
            'en': LEXICON_EN,
            'ru': LEXICON_RU,
        }

    def get_text(self, key: str, lang: str | None = None) -> str:
        language = lang or self.default_language
        translation = self._lexicons.get(language, {})

        if key in translation:
            return translation[key]

        default_translation = self._lexicons.get(self.default_language, {})
        if key in default_translation:
            return default_translation[key]

        fallback_translation = self._lexicons.get('en', {})
        return fallback_translation.get(key, key)

    def get_translations(self, key: str) -> set[str]:
        values = {translations[key] for translations in self._lexicons.values() if key in translations}
        return values or {key}
