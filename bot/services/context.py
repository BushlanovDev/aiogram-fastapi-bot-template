from dataclasses import dataclass

from bot.i18n.lexicon import Lexicon
from bot.keyboards.keyboards import Keyboards
from bot.services.bot_service import BotService


@dataclass
class HandlerContext:
    lexicon: Lexicon
    keyboards: Keyboards
    bot_service: BotService
