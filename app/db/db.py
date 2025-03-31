from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated, AsyncGenerator

load_dotenv()
DB_URL = getenv("DB_URL")

engine = create_async_engine(DB_URL)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
) 

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]
