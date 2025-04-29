import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Задание 1: Приветствие
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!",
        reply_markup=kb.reply_keyboard_greetings
    )


@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message(F.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# Задание 2: Кнопки с URL-ссылками
@dp.message(Command("links"))
async def show_links(message: Message):
    await message.answer("Вот ссылки:", reply_markup=kb.inline_links_keyboard)


# Задание 3: Динамическое меню
@dp.message(Command("dynamic"))
async def show_dynamic(message: Message):
    await message.answer("Нажмите кнопку ниже:", reply_markup=kb.inline_show_more)


@dp.callback_query(F.data == "show_more")
async def expand_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите опцию:",
        reply_markup=kb.inline_options_keyboard
    )


@dp.callback_query(F.data.in_({"option_1", "option_2"}))
async def handle_option(callback: CallbackQuery):
    option_text = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.answer()
    await callback.message.answer(f"Вы выбрали: {option_text}")


# Запуск
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
