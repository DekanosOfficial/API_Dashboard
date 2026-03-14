from datetime import datetime, date
from sqlalchemy.orm import Session
from .models import APIService, HealthCheck, DailyAPISummary
from .database import SessionLocal

def update_daily_summaries():
    db: Session = SessionLocal()
    today = date.today()

    apis =db.query(APIService).all()

    for api in apis:
    # fetch all health checks for this API today
        checks = db.query(HealthCheck).filter(
            HealthCheck.api_id == api.id,
            HealthCheck.checked_at >= datetime(today.day, today.month, today.year)
        ).all()

        if not checks:
            continue # skip apis with no checks

        total_checks = len(checks)
        failures = sum(1 for c in checks if c.status_code >= 500)
        uptime = round((total_checks - failures) / total_checks * 100, 2)
        avg_response = round(sum(c.response_time_ms for c in checks) / total_checks, 2)

        # check if summary exists for toady
        summary = db.query(DailyAPISummary).filter(
            DailyAPISummary.api_id == api.id,
            DailyAPISummary.date == today
        ).first()

        if summary:
            # update existing
            summary.total_checks = total_checks
            summary.total_failures = failures
            summary.uptime_percentage = uptime
            summary.avg_response_time = avg_response
        else:
            # insrt new
            summary = DailyAPISummary(
                api_id=api.id,
                date=today,
                total_checks=total_checks,
                total_failures=failures,
                uptime_percentage=uptime,
                avg_response_time=avg_response
            )
            db.add(summary)

    db.commit()
    db.close()
    print(f"[{datetime.now()}] Daily summaries updated")