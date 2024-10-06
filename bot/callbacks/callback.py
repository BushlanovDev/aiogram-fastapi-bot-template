from aiogram.filters.callback_data import CallbackData


class SaveCallbackFactory(CallbackData, prefix='save'):
    message_id: int
