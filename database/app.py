from collections.abc import Generator
from uuid import uuid4

from functoolz import curry

import ogm
from models import models


class OgmApp:

    @staticmethod
    def get_users(user: models.UserBase) -> Generator[models.User]:
        dicts = ogm.User.get(user.model_dump())
        yield from map(lambda d: models.User.model_validate(d), dicts)

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
        return OgmApp.get_user_one(user)

    @staticmethod
    def delete_user(user: models.User):
        ogm.User.delete(user.model_dump())
        return None

    @staticmethod
    def detach_user(user: models.User):
        ogm.User.detach(user.model_dump())
        return None

    @staticmethod
    def get_queries(query: models.Query):
        records = ogm.Query.get(query.did)
        for query in records:
            query = dict(query['q'])
            query['create_time'] = query['create_time'].to_native()
            query = models.Query.model_validate(query)
            yield query

    @staticmethod
    def create_dialogue(user: models.User, query: models.QueryCreate) -> models.Dialogue:
        query.did = str(uuid4())
        query.index = 1
        parameters = query.model_dump()
        parameters["username"] = user.username
        ogm.User.begin_dialogue(parameters)
        return OgmApp.get_dialogue_one(query)

    @staticmethod
    def append_dialogue(dialogue: models.Dialogue, query: models.QueryCreate):
        query.did = dialogue.did
        ogm.Query.create(query.model_dump())
        ogm.Query.append(query)
        return OgmApp.get_dialogue_one(query)

    @staticmethod
    def get_dialogues(user: models.User):
        dicts = ogm.User.get_dialogues(user.model_dump())
        yield from map(lambda d: models.Dialogue.model_validate(d), dicts)

    @staticmethod
    def get_dialogue_one(query: models.Query) -> models.Dialogue:
        queries = list(OgmApp.get_queries(query))
        dialogue = models.Dialogue(did=query.did, history=queries)
        return dialogue
