import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base Model of User. Username is the unique identifier of a user."""
    username: str


class User(UserBase):
    """This model is returned by OmgApp, and should not be instantiated by other means.
    Any instance of this model represents the existence of the user in database.
    """
    password: str
    telephone: str
    email: str
    profile: str
    create_time: datetime.date


class UserCreate(User):
    """Client should create an instance of UserCreate first and pass it to OmgApp to create a
    user in the database. This class inherits from User and set default values to several fields
    of it, as well as additional fields' validators.
    """
    telephone: str = ""
    email: str = ""
    profile: str = ""
    create_time: datetime.date = datetime.date.today()


class QueryBase(BaseModel):
    """Base model of Query. Queries with the same did form a dialogue.
    User can get a dialogue through did.
    """
    question: str
    answer: str
    create_time: datetime.datetime


class Query(QueryBase):
    """This model is used by OmgApp, and should not be accessed by others. The OgmApp returns
    dialogues which has a filed history specifies a list of quires ordered by create_time."""
    ...


class QueryCreate(Query):
    """User begin a new dialogue or append to existing one with QueryCreate."""
    question: str = ""
    answer: str = ""
    create_time: datetime.datetime = datetime.datetime.now()


class Dialogue(BaseModel):
    """A dialogue can not be found equivalence in the database since it's a view of a list of
    queries.
    """
    did: str
    title: str = ""
    creator: str
    history: list[QueryBase]

