from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.users import UserSchema


class UsersRepository:

    @staticmethod
    async def get_users(
            db: Session,
    ) -> list[UserSchema]:
        """
        return list of users from db
        """
        query = db.query(User)
        return query
