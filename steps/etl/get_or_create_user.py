from loguru import logger
from clearml import Task
from typing import Dict

from application import utils
from domain.documents import UserDocument


def get_or_create_user(task_args: Dict) -> UserDocument:
    user_full_name = task_args['user_full_name']
    logger.info(f"Getting or creating user: {user_full_name}")

    first_name, last_name = utils.split_user_full_name(user_full_name)

    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    task = Task.current_task()
    task.upload_artifact("user_metadata", _get_metadata(user_full_name, user))

    return user


def _get_metadata(user_full_name: str, user: UserDocument) -> Dict:
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }