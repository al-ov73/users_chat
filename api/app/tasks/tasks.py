import asyncio

from celery import Celery

from ..aiogram_bot.main import send_message
from ..config.app_config import CELERY_BROKER_URL

celery = Celery('tasks', broker=CELERY_BROKER_URL)


@celery.task
def send_message_to_telegram(message: dict):
    """
    send message to receiver's telegram
    """
    asyncio.run(send_message(message))
