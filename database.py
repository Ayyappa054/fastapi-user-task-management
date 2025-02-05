from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database URL
DATABASE_URL = "mysql+mysqlconnector://root:Ayyappa%400505@localhost:3306/demo"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
