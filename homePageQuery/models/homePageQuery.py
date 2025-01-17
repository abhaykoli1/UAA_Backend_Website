from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class HomeQueryTable(Document):
    service_type = StringField(required =True)
    email = StringField(required=True)
    country_code = StringField(required=True)
    phone = StringField(required=True)
    name = StringField(required=True)
    deadline = StringField(required =True)
    course_name = StringField(required=True)

class HomeQueryModel(BaseModel):
    service_type : str
    email : str
    country_code : str
    phone : str
    name : str
    deadline : str
    course_name : str