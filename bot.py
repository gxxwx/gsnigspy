import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import instaloader
import os
import requests

# === Настройки ===
TOKEN = "7845620091:AAHSXifU8tUjCmmtsJhe3mV4J9OOJ9KJ1XU"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# === Обработка старта ===
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("👋 Отправь ссылку на Instagram-профиль, и я соберу данные!")

# === Основная логика парсинга ===
@dp.message_handler(lambda msg: "instagram.com" in msg.text)
async def handle_instagram_link(message: types.Message):
    try:
        # Извлекаем username из ссылки
        link = message.text.strip()
        username = link.split("instagram.com/")[1].split("/")[0].split("?")[0]

        # Загружаем данные профиля
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)

        # Получаем нужные данные
        name = profile.full_name or "—"
        bio = profile.biography or "—"
        followers = profile.followers
        following = profile.followees
        posts = profile.mediacount
        is_private = "🔒 Закрыт" if profile.is_private else "🌐 Открыт"
        avatar_url = profile.profile_pic_url

        # Скачиваем аватар
        avatar_path = f"{username}_avatar.jpg"
        with open(avatar_path, "wb") as f:
            f.write(requests.get(avatar_url).content)

        # Формируем сообщение
        msg = (
            f"📄 <b>Профиль:</b> @{username}\n"
            f"👤 <b>Имя:</b> {name}\n"
            f"📌 <b>О себе:</b> {bio}\n"
            f"📷 <b>Постов:</b> {posts}\n"
            f"👥 <b>Подписчиков:</b> {followers}\n"
            f"🔁 <b>Подписок:</b> {following}\n"
            f"🔐 <b>Тип:</b> {is_private}"
        )

        await bot.send_photo(chat_id=message.chat.id, photo=InputFile(avatar_path), caption=msg, parse_mode="HTML")
        os.remove(avatar_path)

    except Exception as e:
        await message.reply(f"❌ Не удалось получить данные.\nОшибка: {e}")

# === Запуск ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
