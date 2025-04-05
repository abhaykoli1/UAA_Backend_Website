from datetime import date
import json
from fastapi import APIRouter

from user.model.usermodel import UserCreateModel, UserLoginModel, UserTable

router = APIRouter()

@router.post("/api/v1/user-create")
async def userCreate(body: UserCreateModel):
    findUser = UserTable.objects(email=body.email).first()
    if (findUser):
        return {
            "message": "user already exist",
            "data": None,
            "status": 401
        }
    else:
        saveData = UserTable(**body.dict())
        saveData.save()
        tojson = saveData.to_json()
        fromjson = json.loads(tojson)
        return {
            "message": "user created success",
            "data": fromjson,
            "status": 201
        }
        
@router.get("/api/v1/get-all-users")
async def getAllUsers():
    findata = UserTable.objects.all()
    return {
        "message": "all Users",
        "data": json.loads(findata.to_json()),
        "status": 200
    }   
        
@router.post("/api/v1/user-login")
async def userLogin(body: UserLoginModel):
    findata = UserTable.objects(email=body.email).first()
    if (findata):
        if findata.password == body.password:
            tojson = findata.to_json()
            fromjson = json.loads(tojson)
            return {
                "message": "user login success",
                "data": fromjson,
                "status": 200
            }
        else:
            return {
                "message": "Incorrect password",
                "data": None,
                "status": 401
            }
    else:
        return {
                "message": "User not found",
                "data": None,
                "status": 404
            }