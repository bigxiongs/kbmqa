import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base Model of User."""
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
