from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

url_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📰 Новости", url="https://ru.wikipedia.org/wiki/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8")],
    [InlineKeyboardButton(text="🎵 Музыка", url="https://music.yandex.ru/")],
    [InlineKeyboardButton(text="📹 Видео", url="https://youtube.com/")],
])