import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from truelove.logger import logger
from truelove.config import config
from .base import Base

import logging

sqlogger = logging.getLogger("sqlalchemy")
sqlogger.setLevel(logging.WARNING)

db_file_path = os.path.join(config.root_dir, "truelove.db")

DATABASE_URL = f"sqlite+aiosqlite:///{db_file_path}"
engine = create_async_engine(DATABASE_URL, echo=False)

SessionFactory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.debug("Database initialized.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")


def session_handler(func):
    async def wrapper(*args, **kwargs):
        async with SessionFactory() as session:
            async with session.begin():
                try:
                    return await func(*args, **kwargs, session=session)
                except SQLAlchemyError as e:
                    logger.error(f"Database error in {func.__name__}: {e}")
                    raise

    return wrapper
