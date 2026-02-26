from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .database import Base

class ApiRequest(Base):
    __tablename__ = "api_requests"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    response_time_ms = Column(Float)
