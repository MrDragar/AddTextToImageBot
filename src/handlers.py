from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()
file_id_storage: dict[str, str] = {}


@router.message(Command("help"))
@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        text="Привет. Я помогу тебе добавить текст к твоей фотографии.\n"
             f"Просто отправь мне картинку и тест для неё."
    )


