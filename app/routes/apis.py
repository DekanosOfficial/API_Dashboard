from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import APIService, HealthCheck, DailyAPISummary
from datetime import datetime
import httpx

router = APIRouter()

@router.get("/apis")
def get_apis(db:Session = Depends(get_db)):
    apis = db.query(APIService).all()

    return [
        {
            "id": api.id,
            "name": api.name,
            "base_url": api.base_url,
            "created_at": api.created_at
        }
        for api in apis
    ]


@router.get("/apis/{api_id}/metrics")
def api_metrics(api_id: int, request: Request, db: Session = Depends(get_db)):
    # 1. Fetch only the specific API request
    api = db.query(APIService).filter(APIService.id == api_id).first()
    if not api:
        return{"error": "API not found"}
    
    # 2. first all checks for this API
    checks = db.query(HealthCheck).filter(HealthCheck.api_id == api_id).order_by(HealthCheck.checked_at.asc()).all()

    if not checks:
        return {"error": "No health checks found"}
        

    # 3. Calculate metrics    
    total = len(checks)
    failures = sum(1 for c in checks if c.status_code >= 500)
    uptime_percentage = round((total - failures) / total * 100, 2)
    avg_response = round(sum(c.response_time_ms for c in checks) / total, 2)

    # 4. Find Last Error Logic
    last_error_check = db.query(HealthCheck).filter(
        HealthCheck.api_id == api_id, 
        HealthCheck.status_code >= 500
        ).order_by(HealthCheck.checked_at.desc()).first()


    last_error_data = None
    if last_error_check:
        last_error_data = {
            "status_code": last_error_check.status_code,
            "checked_at": last_error_check.checked_at.strftime("%d-%m-%Y %H:%M")
        }

    # 5.Prepare chart data
    response_times = [c.response_time_ms for c in checks]
    timestamps = [c.checked_at.strftime("%d-%m-%Y %H:%M") for c in checks]

    status = "healthy"

    if uptime_percentage < 95:
        status = "failing"
    elif avg_response > 400:
        status = "degraded"
    else:
        status = "healthy"

    api_data = {
        "id": api.id,
        "name":api.name,
        "uptime_percentage": uptime_percentage,
        "avg_response_time": avg_response,
        "total_checks": total,
        "total_failures": failures,
        "last_error": last_error_data,
        "response_times": response_times,
        "timestamps": timestamps,
        "status": status
    }

    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        "metrics.html",
        {
            "request": request,
            "apis": [api_data],
            
        }
    )


@router.post("/check/{api_id}")
async def check_api(api_id: int, db: Session = Depends(get_db)):
    api = db.query(APIService).filter(APIService.id == api_id).first()
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    
    start = datetime.utcnow()
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(str(api.base_url))
        status_code = response.status_code
    except Exception:
        status_code = 500

    elapsed = (datetime.utcnow() - start). total_seconds() * 1000


    # save health check
    hc = HealthCheck(
        api_id=api.id,
        status_code=status_code,
        response_time_ms=elapsed,
        checked_at=datetime.utcnow()
    )
    db.add(hc)
    db.commit()
    db.refresh(hc)

    return {
        "status": "checked",
        "api_id": api.id,
        "status_code": status_code,
        "response_time_ms": elapsed
    }