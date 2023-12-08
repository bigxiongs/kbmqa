from database.session import execute


class User:
    match_stmt = "MATCH (u:User {username: $username}) RETURN u"
    create_stmt = ("CREATE (u:User {username: $username, password: $password, "
                   "telephone: $telephone, email: $email, profile: $profile, "
                   "create_time: $create_time}) RETURN u")
    delete_stmt = "MATCH (u:User {username: $username}) DELETE u"
    set_stmt = "MATCH (u:User {username: $username}) SET u.username = $new_name"

    @classmethod
    def get(cls, username: str):
        return execute(cls.match_stmt, {"username": username})

    @classmethod
    def create(cls, parameters: dict):
        return execute(cls.create_stmt, parameters)

    @classmethod
    def delete(cls, username: str):
        return execute(cls.delete_stmt, {"username": username})

    @classmethod
    def set(cls, parameters: dict):
        return execute(cls.set_stmt, parameters)


