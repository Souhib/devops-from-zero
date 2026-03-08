# DevOps Project — Task List

Application simple (frontend React + backend FastAPI) utilisée tout au long du cursus DevOps.

> En entreprise, le frontend et le backend sont généralement dans des dépôts (repos) séparés, avec chacun son propre pipeline CI/CD. Ici, on les met dans le même repo pour simplifier l'apprentissage.

## Structure

```
frontend/           → Vite + React (géré par Bun)
  Dockerfile        → Multi-stage build (Node → nginx)
  nginx.conf        → Reverse proxy vers le backend
backend/            → Python FastAPI (géré par uv)
  Dockerfile        → Image Python avec uv
docker-compose.yml  → Backend + Frontend + PostgreSQL
```

## Lancer en local (sans Docker)

**Backend :**
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
# L'API tourne sur http://localhost:8000
# Sans DATABASE_URL → stockage in-memory (pas besoin de PostgreSQL)
```

**Frontend :**
```bash
cd frontend
bun install
bun run dev
# Le frontend tourne sur http://localhost:3000
# Les appels /api sont proxyfiés vers le backend
```

## Lancer avec Docker Compose

```bash
docker compose up -d --build
# Frontend : http://localhost (port 80)
# Backend :  http://localhost:8000
# PostgreSQL : port 5432 (accessible uniquement depuis le backend)
```

## API Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/api/tasks` | Lister les tâches |
| `POST` | `/api/tasks` | Créer une tâche (`{"title": "..."}`) |
| `DELETE` | `/api/tasks/{id}` | Supprimer une tâche |
| `GET` | `/api/health` | Health check |

## Linting

```bash
# Backend (Ruff)
cd backend && uv run ruff check .

# Frontend (Oxlint)
cd frontend && bunx oxlint .
```

## Tests

```bash
cd backend && uv run pytest
# 5 tests : GET, POST, DELETE, DELETE 404, health
```
