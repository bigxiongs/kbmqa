from database import OgmApp
from models import User, UserBase, UserCreate

rene_info = {
    "username": "rene",
    "password": "000",
}

rene = UserCreate.model_validate(rene_info)
rene = OgmApp.create_user(rene)
print(rene)
rene = OgmApp.get_user_one(rene)
OgmApp.delete_user(rene)
rene = OgmApp.get_user_one(rene)

