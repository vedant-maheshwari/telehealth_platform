from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./telehealth.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread' : False}
)

session_local = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()