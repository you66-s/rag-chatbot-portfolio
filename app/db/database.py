from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from core.config import get_settings

settings = get_settings()

url = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER_NAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOSTNAME,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE_NAME
)

engine = create_engine(
    url=url,
    pool_pre_ping=True,     # checks connection health before using it
    pool_size=10,           # keep 10 connections ready
    max_overflow=10         # allow 20 extra under heavy load
)

session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)