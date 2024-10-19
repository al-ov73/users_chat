import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from ..config.db_config import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=func.now())
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    registered_at: Mapped[created_at]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
