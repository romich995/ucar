import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = f"""postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@"""\
               f"""{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}"""

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()
