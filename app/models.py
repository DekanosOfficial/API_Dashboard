from sqlalchemy import UniqueConstraint, ForeignKey, Column, Integer, String, DateTime, Float,  Date, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class APIService(Base):
    __tablename__ = "api_service"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    base_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    health_checks = relationship("HealthCheck", back_populates="api_service", cascade = "all, delete-orphan")
    daily_api_summaries = relationship("DailyAPISummary", back_populates="api_service", cascade = "all, delete-orphan")



class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    api_id = Column(Integer, ForeignKey('api_service.id', ondelete="CASCADE"), index=True)
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    api_service = relationship("APIService", back_populates="health_checks")
    
    __table_args__ = (
        UniqueConstraint("api_id", "checked_at", name="uq_apiid_checkedat"),
    )


class DailyAPISummary(Base):
    __tablename__ = "daily_api_summaries"
    id = Column(Integer, primary_key=True)
    api_id = Column(Integer, ForeignKey('api_service.id', ondelete="CASCADE"), index=True)
    date = Column(Date, index=True)
    uptime_percentage = Column(Numeric(5, 4), CheckConstraint('uptime_percentage BETWEEN 0.0000 AND 1.0000')) ### example 0.97 would mean 97% not 0.97%
    avg_response_time = Column(Float)
    total_checks = Column(Integer)
    total_failures = Column(Integer)
    api_service = relationship("APIService", back_populates="daily_api_summaries")

    __table_args__ = (
        UniqueConstraint("date", "api_id", name="uq_date_apiid"),
    )


