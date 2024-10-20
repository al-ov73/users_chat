from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc

from ..config.logger_config import get_logger
from ..models.message import Message
from ..schemas.messages import MessageSchema

logger = get_logger(__name__)

class MessagesRepository:

    @staticmethod
    async def get_messages(
            skip: int,
            limit: int,
            db: Session,
    ) -> list[MessageSchema]:
        """
        return list of messages from db
        """
        query = (db.query(Message)
            .options(joinedload(Message.author))
            .options(joinedload(Message.receiver))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query

    @staticmethod
    async def get_messages_for_user(
            user_id: str,
            skip: int,
            limit: int,
            db: Session,
    ) -> list[MessageSchema]:
        """
        return list of messages from db
        """
        query = (db.query(Message)
            .options(joinedload(Message.author))
            .options(joinedload(Message.receiver))
            .filter(
            Message.author_id == user_id or Message.receiver_id == user_id
        )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query

    @staticmethod
    async def get_messages_for_couple_users(
            first_user_id: str,
            second_user_id: str,
            skip: int,
            limit: int,
            db: Session,
    ) -> list[MessageSchema]:
        """
        return list of messages from db
        """
        query = (db.query(Message)
            .filter((
            Message.author_id ==first_user_id  and Message.receiver_id == second_user_id
        ) or (
            Message.author_id == second_user_id and Message.receiver_id == first_user_id
        )
        )
            .options(joinedload(Message.author))
            .options(joinedload(Message.receiver))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return query

    @staticmethod
    async def get_message(
            message_id: str,
            db: Session,
    ) -> MessageSchema | str:
        """
        return message from db by id
        """
        message = db.get(Message, message_id)
        if not message:
            return 'message not exist'
        return message

    @staticmethod
    async def add_message(
            data: dict,
            db: Session,
    ) -> MessageSchema:
        """
        add message to db
        """
        try:
            new_message = Message(
                text=data['text'], author_id=data['author'],
                receiver_id=data['receiver']
                )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            return new_message
        except exc.IntegrityError as e:
            logger.error(f'Error to add new message: {data}')
            logger.error(e)
            db.rollback()
        except KeyError as e:
            logger.error(f'Error to add new message: {data}')
            logger.error(e)

