from ..repositories.messages_repository import MessagesRepository
from ..repositories.users_repository import UsersRepository


def get_messages_repository():
    """
    return message repository
    override it in test environment if necessary
    """
    return MessagesRepository()

def get_users_repository():
    """
    return users repository
    override it in test environment if necessary
    """
    return UsersRepository()