from mongoengine import Document, StringField, ListField, IntField
from pydantic import BaseModel


class SamplePaperTable(Document):
    seo_title = StringField(required=True)
    seo_description = StringField(required=True)
    fileimages = ListField(required=True)
    pageCount = IntField(required=True)
    moduleName = StringField(required=True)
    wordcount = IntField(required=True)
    description = StringField(required=True)
    file = StringField(required=True)

class  SamplePaperModel(BaseModel):
    seo_title:str
    seo_description : str
    pageCount:int
    moduleName:str
    wordcount:int
    description: str
