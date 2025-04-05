
import io
import json
import os
from typing import List
import uuid
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from samplepapers.model.samplepaperModel import SamplePaperTable, SampleBodyModel
from boto3 import client


PACES_ACCESS_KEY = 'DO00AJFUXFALT4K6L69E'
SPACES_SECRET_KEY = 'kn2jUm8ox9W6fPQXvJ6E5kBtVZtzF5V5MvY6sJ8Cr8U'
SPACES_ENDPOINT_URL = 'https://blackwhite.blr1.digitaloceanspaces.com'
SPACES_BUCKET_NAME = 'UAASITE'

# S3 client for DigitalOcean Spaces
s3 = client('s3',
            region_name='blr1',
            endpoint_url=SPACES_ENDPOINT_URL,
            aws_access_key_id=PACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY)

router = APIRouter()

# Function to upload file to DigitalOcean Spaces
def upload_file_to_space(file_content: bytes, filename: str) -> str:
    try:
        # Generate a random filename with the original extension
        random_filename = str(uuid.uuid4())
        file_extension = os.path.splitext(filename)[1]
        random_filename_with_extension = f"{random_filename}{file_extension}"

        # Create a BytesIO stream
        file_content_stream = io.BytesIO(file_content)

        # Upload the file without setting ContentLength
        s3.upload_fileobj(
            file_content_stream,
            SPACES_BUCKET_NAME,
            random_filename_with_extension,
            ExtraArgs={
                'ACL': 'public-read'
            }
        )

        # Return the file's public URL
        return f"{SPACES_ENDPOINT_URL}/UAASITE/{random_filename_with_extension}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    



# FastAPI route to upload a sample
@router.post("/api/v1/upload-sample")
async def upload_sample(
    body: SampleBodyModel
):
    try:
        # Upload main file to Spaces
        # Save data to MongoDB (Example: Ensure `SamplePaperTable` exists)
        sample_paper = SamplePaperTable(
            **body.dict()
        )
        sample_paper.save()

        return JSONResponse(content={
            "message": "Sample uploaded successfully",
            "data": sample_paper.to_json()
        }, status_code=201)

    except Exception as e:
        import traceback
        traceback.print_exc()  # Log the stack trace for debugging
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/api/v1/update-sample/{seo_title}")
async def update_sample(seo_title: str, body: SampleBodyModel):
    try:
        # Find the document by seo_title
        sample_paper = SamplePaperTable.objects(seo_title=seo_title).first()
        
        if not sample_paper:
            raise HTTPException(status_code=404, detail="Sample paper not found")

        sample_paper.update(
            seo_title=body.seo_title,
            seo_description=body.seo_description,
            fileimages=body.fileimages,
            pageCount=body.pageCount,
            moduleName=body.moduleName,
            wordcount=body.wordcount,
            description=body.description,
            file=body.file
        )
        return {
            "message": "Sample paper updated successfully",
            "data": sample_paper.to_json()
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/api/v1/all-sample")
async def getAllSample():
    allSample = []
    sample = SamplePaperTable.objects.all()
    for value in sample:
        allSample.append({
            "sample":json.loads(value.to_json()),
            "seo_title":value.seo_title.replace(" ", "-")
        })
    return {
        "message": "here is all sample",
        "data":allSample,
        "status":200
    }
    

@router.get("/api/v1/search/sample/{query}")
async def searchSAmple(query: str):
    findata = SamplePaperTable.objects(moduleName__icontains = query)
    return {
        "message":"search data",
        "data": json.loads(findata.to_json()),
        "status":200
    }

@router.get("/api/v1/get-sample-perticuler/{title}")
async def getSamplePerticuler(title: str):
    query = title.replace("-", " ")
    findata = SamplePaperTable.objects.get(seo_title=query)
    return {
        "message":"sample data",
        "data": json.loads(findata.to_json()),
        "status": 200
    }
 
   
@router.delete("/api/v1/delete-sample/{sampleTitle}")
async def delete_sample(sampleTitle: str): 
    query = sampleTitle.replace("-", " ")
    
    # Find the sample
    findata = SamplePaperTable.objects.filter(seo_title=query).first()
    
    if not findata:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    # Delete the sample
    findata.delete()
    
    return {
        "message": "Sample deleted successfully",
        "status": 200
    }


@router.post("/api/v1/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read file content
        file_content = await file.read()

        # Upload to DigitalOcean Spaces
        file_url = upload_file_to_space(file_content, file.filename)

        return {"message": "File uploaded successfully", "file_url": file_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    


