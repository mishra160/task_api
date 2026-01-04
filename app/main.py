from fastapi import FastAPI

from app.database import Base, engine
from app.models.task import Task
from app.routes.task_routes import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="task_api")

app.include_router(task_router)


@app.get("/health")
def health():
    return {"status": "ok"}
