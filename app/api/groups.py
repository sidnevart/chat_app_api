from fastapi import APIRouter, Depends
from ..schemas.group import GroupCreate, GroupResponse
from ..services.group_service import GroupService
from ..database import get_db

router = APIRouter()

@router.post("/groups/", response_model=GroupResponse)
async def create_group(group: GroupCreate, db = Depends(get_db)):
    service = GroupService(db)
    return await service.create_group(group)

@router.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(group_id: int, db = Depends(get_db)):
    service = GroupService(db)
    return await service.get_group_by_id(group_id)