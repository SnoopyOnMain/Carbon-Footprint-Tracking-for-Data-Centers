from urllib.parse import quote_plus # Add this import
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. Store your raw password here
raw_password = "Joleia#1273" 

# 2. Encode it (this turns the '#' into '%23')
safe_password = quote_plus(raw_password)

# 3. Use the safe_password in the URL
DATABASE_URL = f"postgresql+asyncpg://postgres:{safe_password}@localhost:5432/carbon_tracker_db"

engine = create_async_engine(DATABASE_URL, echo=True)

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# REPLACE 'your_password' with the password you chose during installation
DATABASE_URL = "postgresql+asyncpg://postgres:Joleia#1273@localhost:5432/carbon_tracker_db"

# This engine handles the actual connection
engine = create_async_engine(DATABASE_URL, echo=True)

# This creates 'sessions' (temporary connections for each API request)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# This is the base class our tables will inherit from
class Base(DeclarativeBase):
    pass

# This is a 'Dependency' - it gives our API routes access to the DB
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session