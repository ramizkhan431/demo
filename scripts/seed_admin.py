import asyncio
import sys
import os

# Add backend directory to sys.path so 'app' can be resolved
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.db.base_class import Base
from app.db.session import engine
from app.models.user import User
from app.services.auth import get_password_hash
from sqlalchemy.future import select

async def seed_admin():
    # Make sure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        result = await db.execute(select(User).filter(User.email == "admin1"))
        admin_user = result.scalars().first()

        if not admin_user:
            print("Admin user not found. Creating admin user...")
            hashed_pw = get_password_hash("12345678")
            admin_user = User(
                email="admin",
                hashed_password=hashed_pw,
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            await db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists. Updating password...")
            admin_user.hashed_password = get_password_hash("12345678")
            await db.commit()
            print("Admin password updated successfully.")

        # Seed admin1 too
        result = await db.execute(select(User).filter(User.email == "admin1"))
        admin1 = result.scalars().first()
        if not admin1:
            hashed_pw = get_password_hash("12345678")
            admin1 = User(
                email="admin1",
                hashed_password=hashed_pw,
                is_active=True,
                is_superuser=True
            )
            db.add(admin1)
            await db.commit()
            print("Admin1 user created successfully.")

if __name__ == "__main__":
    asyncio.run(seed_admin())
