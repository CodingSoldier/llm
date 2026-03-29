from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/cpq?charset=utf8mb4")

def get_session():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()


