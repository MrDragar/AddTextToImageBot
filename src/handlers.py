import asyncio
import tempfile

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.utils.chat_action import ChatActionSender

from src.keyboards import (
    get_menu_keyboard, get_gravity_keyboard,
    get_font_family_keyboard, get_color_keyboard,
)
from src.services import add_text_to_image, GRAVITY_TRANSLATIONS, \
    COLOR_TRANSLATIONS
from src.states import AddTextToImageState

router = Router()
file_id_storage: dict[str, str] = {}


@router.message(Command("help"))
@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        text="Привет. Я помогу тебе добавить текст к твоей фотографии.\n"
             f"Просто отправь мне картинку и тест для неё."
    )


@router.message(F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data({"photo_id": photo_id})
    await message.reply(
        text="Теперь напиши мне текст, который вы хотите добавить на фотографию"
    )
    await state.set_state(AddTextToImageState.get_text_step)


@router.message(AddTextToImageState.get_text_step, F.text)
async def get_text(message: Message, state: FSMContext):
    await state.update_data({"text": message.text})
    await state.set_state(AddTextToImageState.additional_menu_step)
    await message.reply(
        text="Выберите пункт меню", reply_markup=get_menu_keyboard()
    )


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "поменять текст")
async def change_text(message: Message, state: FSMContext):
    await message.reply("Напишите новый текст")
    await state.set_state(AddTextToImageState.get_text_step)


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "поменять размер шрифта")
async def change_font_size(message: Message, state: FSMContext):
    await message.reply("Напишите новый размер шрифта (число)")
    await state.set_state(AddTextToImageState.get_font_size_step)


@router.message(AddTextToImageState.get_font_size_step, F.text)
async def get_font_size(message: Message, state: FSMContext):
    try:
        font_size = int(message.text)
        await state.update_data({"font_size": font_size})
        await message.reply("Размер шрифта изменён. Выберите пункт меню", reply_markup=get_menu_keyboard())
        await state.set_state(AddTextToImageState.additional_menu_step)
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число.")


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "поменять расположение текста")
async def change_gravity(message: Message, state: FSMContext):
    await message.reply("Выберите расположение текста", reply_markup=get_gravity_keyboard())
    await state.set_state(AddTextToImageState.get_gravity_step)


@router.message(AddTextToImageState.get_gravity_step, F.text.lower() == "назад")
async def gravity_back(message: Message, state: FSMContext):
    await message.reply("Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_gravity_step, F.text)
async def set_gravity(message: Message, state: FSMContext):
    gravity_ru = message.text
    if gravity_ru in GRAVITY_TRANSLATIONS:
        gravity_en = GRAVITY_TRANSLATIONS[gravity_ru]
        await state.update_data({"gravity": gravity_en})
        await message.reply(f"Расположение текста изменено на '{gravity_ru}'. Выберите пункт меню", reply_markup=get_menu_keyboard())
        await state.set_state(AddTextToImageState.additional_menu_step)
    else:
        await message.reply("Пожалуйста, выберите корректное расположение из списка.")


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "поменять шрифт")
async def change_font_family(message: Message, state: FSMContext):
    await message.reply("Выберите шрифт", reply_markup=get_font_family_keyboard())
    await state.set_state(AddTextToImageState.get_font_family)


@router.message(AddTextToImageState.get_font_family, F.text.lower() == "arial")
async def set_font_arial(message: Message, state: FSMContext):
    await state.update_data({"font_family": "Arial"})
    await message.reply("Шрифт изменён на 'Arial'. Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_font_family, F.text.lower() == "times new roman")
async def set_font_times_new_roman(message: Message, state: FSMContext):
    await state.update_data({"font_family": "Times New Roman"})
    await message.reply("Шрифт изменён на 'Times New Roman'. Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_font_family, F.text.lower() == "verdana")
async def set_font_verdana(message: Message, state: FSMContext):
    await state.update_data({"font_family": "Verdana"})
    await message.reply("Шрифт изменён на 'Verdana'. Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_font_family, F.text.lower() == "courier new")
async def set_font_courier_new(message: Message, state: FSMContext):
    await state.update_data({"font_family": "Courier New"})
    await message.reply("Шрифт изменён на 'Courier New'. Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_font_family, F.text.lower() == "назад")
async def font_family_back(message: Message, state: FSMContext):
    await message.reply("Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "поменять цвет текста")
async def change_text_color(message: Message, state: FSMContext):
    await message.reply("Выберите цвет текста", reply_markup=get_color_keyboard())
    await state.set_state(AddTextToImageState.get_text_color_step)


@router.message(AddTextToImageState.get_text_color_step, F.text.lower() == "назад")
async def text_color_back(message: Message, state: FSMContext):
    await message.reply("Выберите пункт меню", reply_markup=get_menu_keyboard())
    await state.set_state(AddTextToImageState.additional_menu_step)


@router.message(AddTextToImageState.get_text_color_step, F.text)
async def set_text_color(message: Message, state: FSMContext):
    color_ru = message.text
    if color_ru in COLOR_TRANSLATIONS:
        color_en = COLOR_TRANSLATIONS[color_ru]
        await state.update_data({"text_color": color_en})
        await message.reply(f"Цвет текста изменён на '{color_ru}'. Выберите пункт меню", reply_markup=get_menu_keyboard())
        await state.set_state(AddTextToImageState.additional_menu_step)
    else:
        await message.reply("Пожалуйста, выберите корректный цвет из списка.")


@router.message(AddTextToImageState.additional_menu_step, F.text.lower() == "получить изображение")
async def send_new_photo(message: Message, state: FSMContext):
    await message.answer("Начинаю обработку фотографии")
    data = await state.get_data()
    photo_id = data["photo_id"]

    file = await message.bot.get_file(photo_id)
    file_path = file.file_path
    downloaded_file = await message.bot.download_file(file_path)
    await state.clear()

    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        with tempfile.NamedTemporaryFile(
                delete=True, suffix=".jpg",
                dir=tempfile.gettempdir()) as temp_file:
            temp_file_path = temp_file.name

            with open(temp_file_path, "wb") as f:
                read_file = await asyncio.to_thread(downloaded_file.read)
                await asyncio.to_thread(f.write, read_file)

            new_photo = await asyncio.to_thread(
                add_text_to_image, temp_file_path, **data
            )

        bot_info = await message.bot.get_me()
        await message.reply_photo(
            photo=URLInputFile(new_photo),
            caption=f"Изменено с помощью @{bot_info.username}",
            reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(F.text.lower() == 'отмена')
async def cancel(message: Message, state: FSMContext):
    await message.reply(text="Отмена", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
