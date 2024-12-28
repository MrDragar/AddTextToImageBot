from aiogram.fsm.state import State, StatesGroup


class AddTextToImageState(StatesGroup):
    get_text_step = State()