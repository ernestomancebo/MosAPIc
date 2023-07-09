from fastapi import APIRouter

router = APIRouter(prefix="/test",
                   tags=["test"],
                   responses={404: {"description": "Not found"}})


@router.get("/")
async def root():
    return {"response": "Test Route"}
