from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

SQLALCHEMY_DATABASE_URL = "postgresql:///cscrub-api"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def reset_table(table):
    """Resets the autoincrementing index count for a table."""

    statement = text(f"ALTER SEQUENCE {table}_id_seq RESTART")
    with engine.begin() as connection:
        connection.execute(statement)
    return
