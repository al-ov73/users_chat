from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_users_repository
from ..repositories.users_repository import UsersRepository
from ..schemas.messages import MessageSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user
from ..utils.chat_utils import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.get(
    "",
    dependencies=[Depends(get_current_user)],
)
async def get_users(
        db: Session = Depends(get_db),
        users_repo: UsersRepository = Depends(get_users_repository),
) -> List[UserDbSchema]:
    """
    return list of all users
    """
    users = await users_repo.get_users(db)
    return users
