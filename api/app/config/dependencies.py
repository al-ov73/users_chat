from ..repositories.messages_repository import MessagesRepository
from ..repositories.users_repository import UsersRepository


def get_messages_repository():
    return MessagesRepository()

def get_users_repository():
    return UsersRepository()