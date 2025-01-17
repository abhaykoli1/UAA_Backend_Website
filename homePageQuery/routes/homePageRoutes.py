import json
from fastapi import APIRouter

from homePageQuery.models.homePageQuery import HomeQueryModel, HomeQueryTable



router = APIRouter()

@router.post("/api/v1/add-home-query")
async def addHomeQuery(body: HomeQueryModel):
    savedata = HomeQueryTable(**body.dict())
    savedata.save()
    
    return {
        "message": "Query Added added",
        "status":200
    }


@router.get("/api/v1/get-all-queries")
async def getAllQueries():
    findata = HomeQueryTable.objects.all()
    return {
        "message": "all Queries",
        "data": json.loads(findata.to_json()),
        "status": 200
    }