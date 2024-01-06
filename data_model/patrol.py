from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Date, Integer, JSON, DateTime, Boolean, String, TIMESTAMP
from config import db_config
Base = declarative_base()

class Patrol(Base):
    __tablename__ = "study_documents"
    __table_args__ = {"schema": db_config["DATABASE_SCHEMA"]}

    qr_id = Column(Integer, autoincrement=True, primary_key=True)
    qr_code = Column(Text)
    patrol_name = Column(Text)
    starting_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
