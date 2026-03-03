from fastapi import FastAPI
from app.database import engine
from app import models
from app.middleware import request_logger


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to API Dashboard"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.middleware("http")(request_logger)
