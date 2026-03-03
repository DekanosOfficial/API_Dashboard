from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal, Base
from .models import APIService, HealthCheck, DailyAPISummary



#### Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="API Monitor v0")


#### Dependecncy get DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def index():
    return {"Hello World"}
          

@app.get("/health")
def health():
    return {"status": "ok"}

# @app.get("/system/health")
# defid