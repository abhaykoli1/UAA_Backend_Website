from datetime import date
import json
from fastapi import APIRouter, Request
from serive.models.servicemodel import ServiceSchema, ServiceTable




router = APIRouter()


@router.post("/api/v1/add-service")
async def addService(body: ServiceSchema):
    current_date = date.today()

# Format the date
    formatted_date = current_date.strftime("%d-%m-%Y")   
    saveData = ServiceTable(
        title=body.title,
        shortDec=body.shortDec,
        bannerImg=body.bannerImg,
        seo_title=body.seo_title,
        seo_description=body.seo_description,
        cr_date=formatted_date,
        description=body.description,
        icon=body.icon
        )
    saveData.save()
    return {
        "message":"service added",
        "status": 201
    }

@router.get("/api/v1/get-allService")
async def getAllService():
    serviceData = []
    findData = ServiceTable.objects.all()
    for service in findData:
        serviceTojson = service.to_json()
        fromjson = json.loads(serviceTojson)
        serviceData.append({
            "service": fromjson,
            "seo_title": service.seo_title.replace(" ", "-")
        })

    return {
        "message": "All serive data",
        "data" : serviceData,
        "status": 200
    }

@router.get("/api/v1/get-service/{serviceTitle}")
async def getService(serviceTitle: str):
    query = serviceTitle.replace("-", " ")
    findata = ServiceTable.objects.get(seo_title=query)
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Service data",
        "data": fromjson,
        "status": 200
    }

    
    
