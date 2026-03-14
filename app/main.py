from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import apis, pages
from .database import Base, engine
from .utils import update_daily_summaries
from apscheduler.schedulers.background import BackgroundScheduler

#### Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="API Monitor v0")
app.mount("/static", StaticFiles(directory="static"), name="static")

scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():
    # run every hour
    scheduler.add_job(update_daily_summaries, 'interval', hours=2)
    scheduler.start()


# include the routers
app.include_router(pages.router)
app.include_router(apis.router)

# @app.get("/system/health")
# defid
