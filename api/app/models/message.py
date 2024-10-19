from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import created_at
from .user import intpk
from ..config.db_config import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[intpk]
    text: Mapped[str]
    created_at: Mapped[created_at]

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
        )
    receiver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
        )

    author: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[author_id]
    )
    receiver: Mapped["User"] = relationship(  # noqa: F821
        foreign_keys=[receiver_id]
    )

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "author": {
                "username": self.author.username,
                "id": self.author.id,
            },
            "receiver": {
                "username": self.receiver.username,
                "id": self.receiver.id,
            },
        }
