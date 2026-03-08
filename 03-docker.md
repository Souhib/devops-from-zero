# Module 3 : Docker

## C'est quoi Docker et pourquoi ça existe ?

**Le problème :** "Ça marche sur ma machine !" — la phrase la plus frustrante en informatique. Tu développes sur Ubuntu 22, ton collègue est sur macOS, le serveur de prod est sur Debian 11. Chacun a des versions différentes de Python, de Node, de tout. Résultat : ça pète en prod.

**Docker emballe ton application avec TOUT ce qu'il lui faut** (code, dépendances, configuration, OS) dans un "container" qui tourne de la même façon partout. C'est comme un plat sous vide : même goût que tu le réchauffes à Paris ou à Tokyo.

**Les analogies :**
- **Image** = recette de cuisine (les instructions pour préparer le plat)
- **Container** = plat cuisiné (une instance de la recette, en train de tourner)
- **Dockerfile** = fiche recette (le fichier texte qui décrit comment construire l'image)
- **Docker Hub** = bibliothèque de recettes (registre public d'images)
- **Docker Compose** = menu complet (plusieurs plats/services ensemble)

## Installation

```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
# ⚠️ Déconnecte-toi et reconnecte-toi pour que le changement prenne effet
# (ferme et rouvre ton terminal WSL)

docker --version
# Docker version 24.x.x
```

Vérifie que ça marche :
```bash
docker run hello-world
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

## Images vs Containers

| Concept | C'est quoi | Analogie |
|---------|-----------|----------|
| **Image** | Un template en lecture seule | La recette |
| **Container** | Une instance en cours d'exécution | Le plat cuisiné |

Une image peut donner naissance à plein de containers, comme une recette peut faire plein de plats.

```bash
# Télécharger une image
docker pull python:3.12-slim

# Lister les images
docker images
# REPOSITORY    TAG           IMAGE ID       SIZE
# python        3.12-slim     abc123         150MB

# Lancer un container
docker run python:3.12-slim python3 -c "print('hello docker')"
# hello docker
```

## Le Dockerfile

Un Dockerfile décrit comment construire une image. Chaque ligne = une étape.

```dockerfile
# Image de base (on part de quelque chose qui existe déjà)
FROM python:3.12-slim

# Installer uv (le gestionnaire de dépendances Python)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dossier de travail dans le container
WORKDIR /app

# Copier les dépendances et les installer
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copier le code
COPY . .

# Le port sur lequel l'app écoute (documentation)
EXPOSE 8000

# La commande qui lance l'app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Les instructions principales :

| Instruction | Ce que ça fait |
|------------|---------------|
| `FROM` | Image de base (toujours en premier) |
| `WORKDIR` | Définit le dossier de travail |
| `COPY` | Copie des fichiers de ta machine vers l'image |
| `RUN` | Exécute une commande pendant la construction |
| `EXPOSE` | Documente le port (ne l'ouvre pas réellement) |
| `CMD` | Commande par défaut au lancement du container |

## Commandes Docker essentielles

```bash
# Construire une image
docker build -t mon-app:1.0 .
# -t = tag (nom:version)
# . = contexte (le dossier courant)

# Lancer un container
docker run -d -p 8000:8000 --name mon-backend mon-app:1.0
# -d = détaché (en arrière-plan)
# -p 8000:8000 = port machine:port container
# --name = donner un nom au container

# Lister les containers qui tournent
docker ps
# CONTAINER ID   IMAGE        STATUS          PORTS                    NAMES
# abc123         mon-app:1.0  Up 2 minutes    0.0.0.0:8000->8000/tcp   mon-backend

# Voir TOUS les containers (même arrêtés)
docker ps -a

# Voir les logs
docker logs mon-backend
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Suivre les logs en temps réel
docker logs -f mon-backend

# Arrêter un container
docker stop mon-backend

# Supprimer un container
docker rm mon-backend

# Supprimer une image
docker rmi mon-app:1.0

# Entrer dans un container en cours d'exécution
docker exec -it mon-backend bash
# Tu es maintenant "dans" le container
```

## Volumes

Un container est éphémère — quand tu le supprimes, ses données disparaissent. Un volume persiste les données.

```bash
docker run -d -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  --name ma-db \
  postgres:16
# postgres_data = nom du volume (Docker le gère)
# /var/lib/postgresql/data = chemin DANS le container
```

## Réseau entre containers

Les containers peuvent se parler par leur nom s'ils sont sur le même réseau Docker.

```bash
# Créer un réseau
docker network create mon-reseau

# Lancer deux containers sur le même réseau
docker run -d --network mon-reseau --name backend mon-app:1.0
docker run -d --network mon-reseau --name db postgres:16

# Depuis "backend", tu peux accéder à "db" par son nom :
# postgresql://db:5432/mabase
```

## Docker Compose

Docker Compose gère plusieurs containers ensemble dans un seul fichier YAML.

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/tasks

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=tasks
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Lancer tout
docker compose up -d
# [+] Running 3/3
# ✔ Container db        Started
# ✔ Container backend   Started
# ✔ Container frontend  Started

# Voir l'état
docker compose ps

# Voir les logs
docker compose logs -f

# Tout arrêter et supprimer
docker compose down
```

## CMD vs ENTRYPOINT

- **CMD** : la commande par défaut, remplaçable au lancement. `docker run mon-app echo "autre chose"` remplace le CMD.
- **ENTRYPOINT** : la commande fixe, non remplaçable. Les arguments du `docker run` sont ajoutés après. Utilise ENTRYPOINT quand ton container a un seul rôle.

En pratique, `CMD` suffit dans 90% des cas.

## Multi-stage builds

Permet de réduire la taille de l'image finale en séparant la phase de build et la phase d'exécution.

```dockerfile
# Étape 1 : Build
FROM node:20 AS build
WORKDIR /app
COPY package.json bun.lock ./
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : Production (image légère)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

L'image finale ne contient que nginx + les fichiers buildés, pas Node.js ni les node_modules.

## Projet pratique : Dockerize le projet fil rouge

### 1. Dockerfile pour le backend

Crée `~/devops-project/backend/Dockerfile` :
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Dockerfile pour le frontend

Crée `~/devops-project/frontend/Dockerfile` :
```dockerfile
FROM node:20-slim AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

Crée `~/devops-project/frontend/nginx.conf` :
```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
    location /api {
        proxy_pass http://backend:8000;
    }
}
```

### 3. Docker Compose

Crée `~/devops-project/docker-compose.yml` :
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### 4. Lance tout

```bash
cd ~/devops-project
docker compose up -d --build
# [+] Building ...
# [+] Running 2/2
# ✔ Container devops-project-backend-1   Started
# ✔ Container devops-project-frontend-1  Started

# Vérifie
docker compose ps
curl http://localhost:8000/api/tasks
# Ouvre http://localhost dans ton navigateur
```

💡 **Si le build échoue :** vérifie que le Dockerfile est bien dans le bon dossier et que les fichiers référencés existent.

## Coin entretien

**Q : C'est quoi Docker ?**
R : Un outil qui emballe une application avec toutes ses dépendances dans un container isolé. Le container tourne de la même façon partout.

**Q : Différence entre image et container ?**
R : L'image est un template en lecture seule (la recette). Le container est une instance en cours d'exécution (le plat cuisiné). Une image peut créer plusieurs containers.

**Q : C'est quoi un Dockerfile ?**
R : Un fichier texte qui décrit étape par étape comment construire une image Docker. FROM pour la base, COPY pour les fichiers, RUN pour les commandes, CMD pour le lancement.

**Q : C'est quoi Docker Compose ?**
R : Un outil pour gérer plusieurs containers ensemble avec un fichier YAML. Tu définis tes services, réseaux et volumes, puis `docker compose up` lance tout.

**Q : Comment les containers communiquent entre eux ?**
R : Via un réseau Docker. Docker Compose crée automatiquement un réseau. Les containers se trouvent par leur nom de service (ex: `http://backend:8000`).

**Q : C'est quoi un volume Docker ?**
R : Un stockage persistant. Sans volume, les données disparaissent quand le container est supprimé. Essentiel pour les bases de données.

**Q : C'est quoi un multi-stage build ?**
R : Un Dockerfile avec plusieurs étapes. On build dans une image lourde, puis on copie uniquement le résultat dans une image légère. Ça réduit la taille finale.

## Erreurs courantes

- **"Permission denied" avec docker** → Tu n'as pas fait `usermod -aG docker $USER` ou tu ne t'es pas reconnecté.
- **"Port already in use"** → Un autre processus utilise ce port. `docker ps` pour voir ou `ss -tlnp | grep PORT`.
- **Oublier `-p` au `docker run`** → Le container tourne mais tu ne peux pas y accéder depuis ta machine.
- **Modifier le code sans rebuilder** → `docker compose up -d --build` pour reconstruire après un changement.
- **Gros images** → Utilise des images `-slim` ou `-alpine`, et le multi-stage build.

## Pour aller plus loin

- **Docker security** : rootless Docker, ne pas tourner en root dans le container
- **Podman** : alternative à Docker, sans daemon (plus sécurisé)
- **Docker Swarm** : orchestration basique intégrée à Docker
- **Optimisation d'images** : `.dockerignore`, ordre des layers, cache
- **BuildKit** : le nouveau builder Docker, plus rapide
- **Distroless images** : images ultra-minimalistes de Google
