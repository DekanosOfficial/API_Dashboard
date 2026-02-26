from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class APIService(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    base_url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    health_checks = relationship("HealthCheck", back_populates="api")

class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True)
    api_id = Column(Integer, ForeignKey=("apis.id"))
    status_code = Column(Integer)
    response_time = Column(Float)
    is_up = Column(Boolean)
    checked_at = Column(DateTime, default=datetime.utcnow)

    api = relationship("APIService", back_populates="health_checks")