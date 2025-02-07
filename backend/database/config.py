from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:aryany19@localhost/chatbot_db"

#engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)


#create session
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()