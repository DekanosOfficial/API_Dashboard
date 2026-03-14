from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import APIService, HealthCheck


def seed_data():
    db: Session = SessionLocal()


    # Check if we already have an API
    if db.query(APIService).count() > 0:
        print("Data already seeded")
        return
    

    # 1. create fake api service
    api = APIService(name="Example API", base_url="https://example.com")
    db.add(api)
    db.commit()
    db.refresh(api)

    # 2. add fake health checks (last 7 days)
    for i in range(7):
        check_time = datetime.utcnow() - timedelta(days=i)
        status = 200 if i % 3 != 0 else 500 # some fails
        response_time = round(100 + i*10, 2)

        hc = HealthCheck(
            api_id=api.id,
            status_code=status,
            response_time_ms=response_time,
            checked_at=check_time
        )
        db.add(hc)

    db.commit()
    db.close()
    print("Seeded example API and health checks")

if __name__ == "__main__":
    seed_data()