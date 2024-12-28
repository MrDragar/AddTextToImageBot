from aiogram.fsm.state import State, StatesGroup


class AddTextToImageState(StatesGroup):
    get_text_step = State()
    additional_menu_step = State()

    get_font_size_step = State()
    get_gravity_step = State()
    get_font_family = State()
    get_text_color_step = State()
