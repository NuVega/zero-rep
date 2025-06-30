from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(Command("dynamic"))
async def show_initial_button(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )
    await message.answer("Нажми кнопку ниже:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "show_more")
async def show_options(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
            [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
        ]
    )
    await callback.message.edit_text("Выбери опцию:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("option_"))
async def handle_option(callback: types.CallbackQuery):
    option = "1" if callback.data == "option_1" else "2"
    await callback.message.answer(f"Вы выбрали: Опция {option}")
    await callback.answer()