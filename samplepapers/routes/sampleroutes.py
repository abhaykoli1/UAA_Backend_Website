
import io
import json
import os
from typing import List
import uuid
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from samplepapers.model.samplepaperModel import SamplePaperTable
from boto3 import client


router = APIRouter()

SPACES_ACCESS_KEY = 'DO00AJFUXFALT4K6L69E'
SPACES_SECRET_KEY = 'kn2jUm8ox9W6fPQXvJ6E5kBtVZtzF5V5MvY6sJ8Cr8U'
SPACES_ENDPOINT_URL = 'https://blackwhite.blr1.digitaloceanspaces.com'
SPACES_BUCKET_NAME = 'UAASITE'

# S3 client
s3 = client('s3',
            region_name='blr1',
            endpoint_url=SPACES_ENDPOINT_URL,
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY)

def upload_file_to_space(file_content: bytes, filename: str):
    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]
    random_filename_with_extension = f"{random_filename}{file_extension}"

    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(
        file_content_stream,
        SPACES_BUCKET_NAME,
        random_filename_with_extension,
        ExtraArgs={'ACL': 'public-read'}
    )

    return f"{SPACES_ENDPOINT_URL}/{SPACES_BUCKET_NAME}/{random_filename_with_extension}"

@router.post("/api/v1/upload-sample")
async def upload_sample(
    seo_title: str = Form(...),
    seo_description: str = Form(...),
    pageCount: int = Form(...),
    moduleName: str = Form(...),
    wordcount: int = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    fileimages: List[UploadFile] = File(...)
):
    try:
        # Upload main file to Spaces
        file_content = await file.read()
        file_url = upload_file_to_space(file_content, file.filename)

        # Upload images to Spaces
        file_images_urls = []
        for image in fileimages:
            image_content = await image.read()
            image_url = upload_file_to_space(image_content, image.filename)
            file_images_urls.append(image_url)

        # Save data to MongoDB
        sample_paper = SamplePaperTable(
            seo_title=seo_title,
            seo_description=seo_description,
            fileimages=file_images_urls,
            pageCount=pageCount,
            moduleName=moduleName,
            wordcount=wordcount,
            description=description,
            file=file_url
        )
        sample_paper.save()

        return JSONResponse(content={"message": "Sample uploaded successfully", "data": sample_paper.to_json()}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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