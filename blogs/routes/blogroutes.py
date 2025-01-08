from datetime import date
import json
from fastapi import APIRouter

from blogs.models.blogsmodel import BlogSchema, BlogsTable
from serive.models.servicemodel import ServiceSchema, ServiceTable

router = APIRouter()

@router.post("/api/v1/add-blog")
async def addblog(body: BlogSchema):
    current_date = date.today()

# Format the date
    formatted_date = current_date.strftime("%d-%m-%Y")   
    saveData = BlogsTable(
        title=body.title, 
        shortDec=body.shortDec, 
        bannerImg=body.bannerImg, 
        seo_title=body.seo_title,
        seo_description=body.seo_description,
        service_category=body.service_category,
        cr_date=formatted_date,
        description=body.description
        )
    saveData.save()
    return {
        "message":"blog added",
        "status": 201
    }
 
    
@router.get("/api/v1/get-allblogs")
async def getAllblog():
    serviceData = []
    findData = BlogsTable.objects.all()
    for blog in findData:
        serviceTojson = blog.to_json()
        fromjson = json.loads(serviceTojson)
        serviceData.append({
            "blog": fromjson,
            "seo_title": blog.seo_title.replace(" ", "-")
        })
    return {
        "message": "All blogs data",
        "data" : serviceData,
        "staus": 200
    }


@router.get("/api/v1/get-blog/{blogTitle}")
async def getService(blogTitle: str):
    query = blogTitle.replace("-", " ")
    findata = BlogsTable.objects.get(seo_title=query)
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Blog data",
        "data": fromjson,
        "status": 200
    }
    