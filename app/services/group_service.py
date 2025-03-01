from ..repositories.group_repository import GroupRepository
from ..schemas.group import GroupCreate, GroupResponse
from ..database import get_db

class GroupService:
    def __init__(self, db):
        self.repo = GroupRepository(db)

    async def create_group(self, group: GroupCreate):
        return await self.repo.create_group(group)

    async def get_group_by_id(self, group_id: int):
        return await self.repo.get_group_by_id(group_id)