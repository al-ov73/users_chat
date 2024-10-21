from aiogram import Bot

from ..config.app_config import BOT_TOKEN, TELEGRAM_USER_ID

if BOT_TOKEN:
    bot = Bot(token=BOT_TOKEN)


async def send_message(message: dict):
    """
    send message to receiver's telegram
    """
    msg_author = message['author']['username']
    msg_text = message['text']
    msg_to_user = (f'Пользователь {msg_author} отправил Вам сообщение:\n'
                   f'"{msg_text}"')
    await bot.send_message(TELEGRAM_USER_ID, msg_to_user)
