from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import main_menu

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выбери опцию:",
        reply_markup=main_menu
    )

@router.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@router.message(F.text == "Пока")
async def say_bye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")