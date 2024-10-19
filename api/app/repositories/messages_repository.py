from sqlalchemy.orm import Session, joinedload

from ..models.message import Message
from ..schemas.messages import MessageSchema


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
            new_message: MessageSchema,
            db: Session,
    ) -> MessageSchema:
        """
        add message to db
        """
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
