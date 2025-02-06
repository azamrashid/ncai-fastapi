from sqlmodel import SQLModel, create_engine, Session
from config import settings

engine = create_engine(settings.DATABASE_URL_NEON)

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency for database session
def get_db():
    with Session(engine) as session:
        yield session