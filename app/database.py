import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Load the .env file
load_dotenv()

# 2. Get the URL
DATABASE_URL = os.getenv("DATABASE_URL", "")

# 3. Create the engine
# Note: If DATABASE_URL is None, this will show an error. 
# Make sure your .env file is in the root folder!
engine = create_async_engine(DATABASE_URL, echo=True)

# 4. Setup the session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 5. Define Base
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session