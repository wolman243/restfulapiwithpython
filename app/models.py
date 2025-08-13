from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class JobResult(Base):
    
    __tablename__ = "job_results"

    id = Column(Integer, primary_key = True, index = True)
    job_name = Column(String(100), index = True)

    status = Column(String(50), default = "pending")
    result = Column(Text)

    created_at = Column(DateTime(timezone = True), server_default = func.now())

    updated_at = Column(DateTime(timezone = True), onupdate = func.now())