# DevOps Project — Task List

Application simple (frontend React + backend FastAPI) utilisée tout au long du cursus DevOps.

> En entreprise, le frontend et le backend sont généralement dans des dépôts (repos) séparés, avec chacun son propre pipeline CI/CD. Ici, on les met dans le même repo pour simplifier l'apprentissage.

## Structure

```
frontend/   → Vite + React (géré par Bun)
backend/    → Python FastAPI
```

## Lancer en local

**Backend :**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend :**
```bash
cd frontend
bun install
bun run dev
```

Le frontend tourne sur `http://localhost:3000` et proxy les appels `/api` vers le backend sur `http://localhost:8000`.

## Linting

```bash
# Backend (Ruff)
cd backend && ruff check .

# Frontend (Oxlint)
cd frontend && bunx oxlint .
```

## Tests

```bash
cd backend && pytest
```
