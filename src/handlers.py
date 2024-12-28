import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import tempfile

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
    data = await state.get_data()
    photo_id = data["photo_id"]
    file = await message.bot.get_file(photo_id)
    file_path = file.file_path
    downloaded_file = await message.bot.download_file(file_path)
    await state.clear()

    with tempfile.NamedTemporaryFile(
            delete=True, suffix=".jpg",
            dir=tempfile.gettempdir()) as temp_file:
        temp_file_path = temp_file.name

        with open(temp_file_path, "wb") as f:
            read_file = await asyncio.to_thread(downloaded_file.read)
            await asyncio.to_thread(f.write, read_file)

