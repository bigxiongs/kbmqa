from datetime import date

import ogm
from models import models


class OgmApp:
    @staticmethod
    def get_users(user: models.UserBase) -> list[models.User]:
        records = ogm.User.get(user.username)
        users = map(lambda record: dict(record['u']), records)
        for user in users:
            user['create_time'] = user['create_time'].to_native()
            yield models.User.model_validate(user)

    @staticmethod
    def get_user_one(user: models.UserBase) -> models.User:
        users = list(OgmApp.get_users(user))
        if not len(users):
            raise Exception('user %s not found' % user.username)
        elif len(users) > 1:
            raise Exception('more than one %s found' % user.username)
        return users[0]

    @staticmethod
    def create_user(user: models.UserCreate) -> models.User:
        if any(OgmApp.get_users(user)):
            raise Exception('user %s already exists' % user.username)
        ogm.User.create(user.model_dump())
        user = OgmApp.get_user_one(user)
        return models.User.model_validate(user)

    @staticmethod
    def delete_user(user: models.User):
        ogm.User.delete(user.username)
        return None
