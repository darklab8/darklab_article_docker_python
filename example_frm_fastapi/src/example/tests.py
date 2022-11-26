import pytest
from sqlalchemy.dialects.postgresql import insert
from utils.database.sql import Database
from . import models

@pytest.mark.asyncio
async def test_example(database: Database):
    async with database.get_async_session() as session:
        stmt = insert(models.Example).values(name="123")
        await session.execute(stmt)
        await session.commit()