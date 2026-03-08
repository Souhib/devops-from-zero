import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    title: str


# --- Storage : PostgreSQL si DATABASE_URL est défini, sinon in-memory ---
# En local (sans Docker) : in-memory, pas besoin de base de données
# Avec Docker Compose : PostgreSQL via DATABASE_URL

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    import psycopg2

    def _conn():
        return psycopg2.connect(DATABASE_URL)

    @app.on_event("startup")
    def _init_db():
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        done BOOLEAN DEFAULT FALSE
                    )
                """)
                cur.execute("SELECT COUNT(*) FROM tasks")
                if cur.fetchone()[0] == 0:
                    cur.execute(
                        "INSERT INTO tasks (title) VALUES "
                        "('Apprendre Docker'), ('Configurer CI/CD')"
                    )

    def _list_tasks():
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
                return [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]

    def _add_task(title):
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done", (title,)
                )
                r = cur.fetchone()
                return {"id": r[0], "title": r[1], "done": r[2]}

    def _remove_task(task_id):
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="Task not found")

else:
    _tasks: list[dict] = [
        {"id": 1, "title": "Apprendre Docker", "done": False},
        {"id": 2, "title": "Configurer CI/CD", "done": False},
    ]
    _next_id = 3

    def _list_tasks():
        return _tasks

    def _add_task(title):
        global _next_id
        task = {"id": _next_id, "title": title, "done": False}
        _next_id += 1
        _tasks.append(task)
        return task

    def _remove_task(task_id):
        for i, t in enumerate(_tasks):
            if t["id"] == task_id:
                _tasks.pop(i)
                return
        raise HTTPException(status_code=404, detail="Task not found")


# --- Routes ---


@app.get("/api/tasks")
def get_tasks():
    return _list_tasks()


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    return _add_task(task.title)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    _remove_task(task_id)


@app.get("/api/health")
def health():
    return {"status": "ok"}
