from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

postgres_dsn = str(settings.postgres_dsn)

engine = create_async_engine(url=postgres_dsn, echo=settings.DEBUG)

sessionmaker = async_sessionmaker(bind=engine)
