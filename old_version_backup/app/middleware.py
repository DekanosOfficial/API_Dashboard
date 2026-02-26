import time
from fastapi import Request
from app.database import SessionLocal
from app.models import ApiRequest

async def request_logger(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000

    db = SessionLocal()
    try:
        log = ApiRequest(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            response_time_ms=duration_ms
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

    return response
