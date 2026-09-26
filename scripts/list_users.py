import asyncio
import sys
import os
from sqlalchemy.future import select
from app.db.session import SessionLocal
from app.models.user import User

async def list_users():
    async with SessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Active: {user.is_active}, Superuser: {user.is_superuser}")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(list_users())
