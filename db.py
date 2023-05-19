# db.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Form the connection string
DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create the engine
engine = create_engine(DATABASE_URL)

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the metadata
Base = declarative_base()

def get_db() -> Session:
    """
    Initialize a new database session,
    yield it to the caller for database operations,
    and close the session when the caller is done.
    """
    
    # Initialize a new session
    db = SessionLocal()
    try:
        # Yield the session to the caller
        yield db
    finally:
        # Close the session 
        db.close()