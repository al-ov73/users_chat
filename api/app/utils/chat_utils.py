from fastapi import WebSocket

from ..config.logger_config import get_logger
from ..tasks.tasks import send_message_to_telegram

logger = get_logger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        """
        accept websocket connection and add it to active connections list
        """
        await websocket.accept()
        logger.info(f'Got new websocket connection from {user_id}')
        self.active_connections[user_id] = websocket
        logger.info('active_connections', self.active_connections)

    def disconnect(self, user_id: int):
        """
        remove socket from active connetions
        """
        logger.info(f'User id:{user_id} disconnected from websocket')
        self.active_connections.pop(user_id)

    async def send_personal_message(
            self,
            message: dict,
            author_id: int,
            receiver_id: int
    ):
        """
        send message to receiver and author
        """
        # send message to author
        author_wc = self.active_connections.get(author_id)
        await author_wc.send_json(message)

        # send message to receiver
        if self.active_connections.get(receiver_id):
            receiver_wc = self.active_connections.get(receiver_id)
            await receiver_wc.send_json(message)
        else:
            print('msg ->>>', message)
            send_message_to_telegram.delay(message)
