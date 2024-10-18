from aiogram import Bot

from ..config.app_config import BOT_TOKEN, ADMIN_ID

bot = Bot(token=BOT_TOKEN)


async def send_message():
    await bot.send_message(ADMIN_ID, 'text')
