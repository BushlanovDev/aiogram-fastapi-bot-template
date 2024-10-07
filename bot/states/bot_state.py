from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):
    waiting_step_1 = State()
    waiting_step_2 = State()
