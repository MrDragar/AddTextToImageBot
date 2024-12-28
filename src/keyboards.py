from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.add(types.KeyboardButton(text="получить изображение"))
    keyboard_builder.row(
        types.KeyboardButton(text="поменять размер шрифта"),
        types.KeyboardButton(text="поменять расположение текста"),
    )
    keyboard_builder.row(
        types.KeyboardButton(text="поменять текст"),
        types.KeyboardButton(text="поменять шрифт"),
        types.KeyboardButton(text="поменять цвет текста"),
    )
    keyboard_builder.row(types.KeyboardButton(text="Отмена"))

    return keyboard_builder.as_markup(resize_keyboard=True)


def get_gravity_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        types.KeyboardButton(text="Север"),
        types.KeyboardButton(text="Юг"),
    )
    keyboard_builder.row(
        types.KeyboardButton(text="Центр"),
        types.KeyboardButton(text="Восток"),
        types.KeyboardButton(text="Запад"),
    )
    keyboard_builder.row(types.KeyboardButton(text="Назад"))
    return keyboard_builder.as_markup(resize_keyboard=True)


def get_font_family_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        types.KeyboardButton(text="Arial"),
        types.KeyboardButton(text="Times New Roman"),
    )
    keyboard_builder.row(
        types.KeyboardButton(text="Verdana"),
        types.KeyboardButton(text="Courier New"),
    )
    keyboard_builder.row(types.KeyboardButton(text="Назад"))
    return keyboard_builder.as_markup(resize_keyboard=True)


def get_color_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.row(
        types.KeyboardButton(text="Красный"),
        types.KeyboardButton(text="Зеленый"),
        types.KeyboardButton(text="Синий"),
    )
    keyboard_builder.row(
        types.KeyboardButton(text="Желтый"),
        types.KeyboardButton(text="Черный"),
        types.KeyboardButton(text="Белый"),
    )
    keyboard_builder.row(types.KeyboardButton(text="Назад"))
    return keyboard_builder.as_markup(resize_keyboard=True)