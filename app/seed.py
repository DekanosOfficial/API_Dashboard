from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import APIService, HealthCheck


def seed_dat():
    db: Session = SessionLocal()


    # Check if we already have an API