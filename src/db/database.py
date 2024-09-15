import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from dotenv import load_dotenv
from models import UserRequest

load_dotenv()

DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def log_user_request(user_id: str, db: Session):
    """Log user request and update request count."""
    user = db.query(UserRequest).filter_by(user_id=user_id).first()
    if user:
        user.request_count += 1
    else:
        user = UserRequest(user_id=user_id, request_count=1)
    db.add(user)
    db.commit()

def rate_limit_check(user_id: str, db: Session) -> bool:
    """Check if a user has exceeded request limit."""
    user = db.query(UserRequest).filter_by(user_id=user_id).first()
    if user and user.request_count > 5:
        return True
    return False
