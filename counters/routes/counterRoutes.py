import json
from fastapi import APIRouter
from counters.models.counters import CountersModel, CountersTable



router = APIRouter()

@router.post("/api/v1/add-counters")
async def addCounters(body: CountersModel):
    savedata = CountersTable(**body.dict())
    savedata.save()
    
    return {
        "message": "Counters Added",
        "status":200
    }


@router.get("/api/v1/get-all-counters")
async def getAllCounters():
    findata = CountersTable.objects.all()
    return {
        "message": "all Counters",
        "data": json.loads(findata.to_json()),
        "status": 200
    }
    

@router.put("/api/v1/update-counter/{counter_id}")
async def updateCounter(counter_id: str, body: CountersModel):
    counter = CountersTable.objects.filter(id=counter_id).first()
    if not counter:
        return {"message": "Counter not found", "status": 404}
    
    counter.update(**body.dict())
    return {"message": "Counter updated successfully", "status": 200}
    
@router.delete("/api/v1/deleteCounters")
def delete_all_samples():
    deleted = CountersTable.objects.all().delete()
    return {
        "message": f"Deleted  successfully",
        "status": 200
    }