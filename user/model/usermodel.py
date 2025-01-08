from mongoengine import Document, StringField
from pydantic import BaseModel


class UserTable(Document):
    name= StringField(required=True)
    email = StringField(required=True)
    password = StringField(required= True)
    phone = StringField(required=True)
    country_code = StringField(required=True)
    
class UserCreateModel(BaseModel):
    name: str
    email:str
    password:str
    phone:str
    country_code:str
    
class UserLoginModel(BaseModel):
    email:str
    password:str