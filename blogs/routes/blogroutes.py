from datetime import date
from http.client import HTTPException
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


@router.put("/api/v1/update-blog/{seo_title}")
async def update_blog(seo_title: str, body: BlogSchema):
    query = seo_title.replace("-", " ")
    try:
        # Find the blog by seo_title
        blog = BlogsTable.objects(seo_title=query).first()
        
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        # Update the fields with new data
        blog.update(
            title=body.title,
            shortDec=body.shortDec,
            bannerImg=body.bannerImg,
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            service_category=body.service_category,
            description=body.description
        )

        return {
            "message": "Blog updated successfully",
            "data": json.loads(blog.to_json())
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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
    
@router.delete("/api/v1/delete-blog/{blogTitle}")
async def delete_blog(blogTitle: str):
    query = blogTitle.replace("-", " ")
    
    # Find the blog
    findata = BlogsTable.objects.filter(seo_title=query).first()
    
    if not findata:
        raise HTTPException(status_code=404, detail="blog not found")
    
    # Delete the blog
    findata.delete()
    
    return {
        "message": "Blog deleted successfully",
        "status": 200
    }
    