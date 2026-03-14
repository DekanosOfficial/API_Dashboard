from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import APIService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    apis = db.query(APIService).all()

    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "apis": apis
        }
    )
          


@router.get("/health")
def health():
    return {"status": "ok"}