import json
from fastapi import APIRouter

from query.models.contactquery import ContactQueryModel, ContactQueryTable


router = APIRouter()

@router.post("/api/v1/add-contact-query")
async def adContactQuery(body: ContactQueryModel):
    savedata = ContactQueryTable(**body.dict())
    savedata.save()

    return {
        "message": "contact added",
        "status":200
    }


@router.get("/api/v1/get-all-contact")
async def getAllContact():
    findata = ContactQueryTable.objects.all()
    return {
        "message": "all contact query",
        "data": json.loads(findata.to_json()),
        "status": 200
    }