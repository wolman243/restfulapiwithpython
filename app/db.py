from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:rootpass@mysql:3306/s4edb"

engine = create_engine(DATABASE_URL, echo = True)
session_local = sessionmaker(bind = engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()