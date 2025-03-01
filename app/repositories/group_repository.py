from sqlalchemy.ext.asyncio import AsyncSession
from ..models.group import Group
from ..schemas.group import GroupCreate
from sqlalchemy.future import select
import logging

class GroupRepository:
    def __init__(self, db: AsyncSession):
        if db is None:
            logging.error("Received None for db in GroupRepository")
        self.db = db

    async def create_group(self, group: GroupCreate):
        logging.info(f"Received database session: {group} {group.name} {group.creator_id}")
        if self.db is None:
            logging.error("Database session is None in create_group")
            raise ValueError("Database session is None")
        db_group = Group(name=group.name, creator_id=group.creator_id)
        self.db.add(db_group)
        await self.db.commit()
        await self.db.refresh(db_group)
        return db_group

    async def get_group_by_id(self, group_id: int):
        if self.db is None:
            logging.error("Database session is None in get_group_by_id")
            raise ValueError("Database session is None")
        result = await self.db.execute(select(Group).filter(Group.id == group_id))
        return result.scalars().first()