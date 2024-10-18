from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.users import UserSchema


class UsersRepository:

    async def get_users(
            self,
            db: Session,
    ) -> list[UserSchema]:
        """
        return list of users from db
        """
        query = db.query(User).all()
        return query
