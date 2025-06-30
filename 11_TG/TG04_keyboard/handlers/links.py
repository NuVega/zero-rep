from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import url_keyboard

router = Router()

@router.message(Command("links"))
async def send_links(message: Message):
    await message.answer("Вот полезные ссылки:", reply_markup=url_keyboard)