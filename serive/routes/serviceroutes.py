from datetime import date
from http.client import HTTPException
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
    findata = ServiceTable.objects(seo_title=query)
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Service data",
        "data": fromjson,
        "status": 200
    }

@router.put("/api/v1/update-service/{seo_title}")
async def update_service(seo_title: str, body: ServiceSchema):
    query = seo_title.replace("-", " ")
    try:
        # Find the service by seo_title
        service = ServiceTable.objects(seo_title=query).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        # Update the fields with new data
        service.update(
            title=body.title,
            shortDec=body.shortDec,
            bannerImg=body.bannerImg,
            icon=body.icon,
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            description=body.description,
        )
        return {
            "message": "Service updated successfully",
            "data": json.loads(service.to_json())
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/api/v1/delete-service/{serviceTitle}")
async def delete_service(serviceTitle: str):
    query = serviceTitle.replace("-", " ")
    
    # Find the service
    findata = ServiceTable.objects.filter(seo_title=query).first()
    
    if not findata:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Delete the service
    findata.delete()
    
    return {
        "message": "Service deleted successfully",
        "status": 200
    }
    
    
