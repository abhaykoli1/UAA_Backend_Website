from mongoengine import Document, StringField, DictField
from pydantic import BaseModel

class ServiceTable(Document):
    title = StringField(required=True)
    shortDec = StringField(required=True)
    bannerImg = StringField(required=True)
    icon = StringField(required=True)
    seo_title = StringField(required=True)
    seo_description=StringField(required=True)
    description = StringField(required=True)

    cr_date = StringField(required=True)
class ServiceSchema(BaseModel):
    title:str
    shortDec:str
    bannerImg:str
    icon : str
    seo_title:str
    seo_description: str
    description : str
