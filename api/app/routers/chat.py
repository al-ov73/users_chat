from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_messages_repository
from ..config.logger_config import get_logger
from ..repositories.messages_repository import MessagesRepository
from ..schemas.messages import MessageSchema
from ..utils.auth_utils import get_current_user
from ..utils.chat_utils import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

logger = get_logger(__name__)


@router.get(
    "/messages/talk",
    dependencies=[Depends(get_current_user)],
)
async def get_messages_for_couple_users(
        first_user_id: str,
        second_user_id: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        messages_repo: MessagesRepository = Depends(get_messages_repository),
) -> List[MessageSchema]:
    """
    send all messages where user is author or receiver
    """
    logger.info(
        f'Get request for users id:{first_user_id} id:{second_user_id} messages.'
        f'Skip: {skip}, Limit: {limit}'
    )
    messages = await messages_repo.get_messages_for_couple_users(
        first_user_id, second_user_id, skip, limit, db
    )
    return messages


@router.get(
    "/messages/{user_id}",
    dependencies=[Depends(get_current_user)],
)
async def get_messages_for_user(
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        messages_repo: MessagesRepository = Depends(get_messages_repository),
) -> List[MessageSchema]:
    """
    send all messages where user is author or receiver
    """
    logger.info(f'Get request for users messages. Skip: {skip}, Limit: {limit}')
    messages = await messages_repo.get_messages_for_user(
        user_id, skip, limit, db
    )
    return messages


@router.get(
    "/messages",
    dependencies=[Depends(get_current_user)],
)
async def get_last_messages(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        messages_repo: MessagesRepository = Depends(get_messages_repository),
) -> List[MessageSchema]:
    """
    send all last chat messages
    """
    logger.info(f'Get request for last messages. Skip: {skip}, Limit: {limit}')
    messages = await messages_repo.get_messages(skip, limit, db)
    return messages


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        user_id: int,
        db: Session = Depends(get_db),
        messages_repo: MessagesRepository = Depends(get_messages_repository),
):
    """
    wait message from Websocket and send it through all opened connections
    """
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            new_message = await messages_repo.add_message(data, db)
            logger.info(f'-----new message in db {new_message}---------')

            if new_message:
                author_id = new_message.author.id
                receiver_id = new_message.receiver.id
                await manager.send_personal_message(
                    new_message.to_dict(), author_id, receiver_id
                )
    except WebSocketDisconnect:
        manager.disconnect(user_id)
