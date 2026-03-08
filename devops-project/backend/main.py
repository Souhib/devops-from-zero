from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (pas de base de données pour l'instant)
tasks: list[dict] = [
    {"id": 1, "title": "Apprendre Docker", "done": False},
    {"id": 2, "title": "Configurer CI/CD", "done": False},
]


class TaskCreate(BaseModel):
    title: str


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False,
    }
    tasks.append(new_task)
    return new_task


@app.get("/api/health")
def health():
    return {"status": "ok"}
