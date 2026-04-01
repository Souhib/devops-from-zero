# Module 3 : Docker

> **Prérequis :** Module 0 (Git), Module 1 (Linux — commandes de base), Module 2 (Réseau — ports, IP)

> **En résumé :** Tu apprends à empaqueter ton application dans des containers Docker pour qu'elle tourne de la même façon partout. C'est LE module carrefour du cursus — Docker est utilisé dans le CI/CD, le déploiement AWS, Kubernetes et le monitoring.

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
# usermod = modifier un utilisateur
# -aG docker = ajouter (-a) au groupe (-G) "docker"
# $USER = ton nom d'utilisateur (variable automatique de Linux)
# Sans ça, il faudrait taper "sudo" devant chaque commande docker
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

> **Essaie cette commande** — c'est la façon la plus simple de vérifier que Docker marche :

```bash
docker run python:3.12-slim python3 -c "print('hello docker')"
# Docker télécharge l'image python (la première fois ça prend ~30 secondes)
# puis lance un container et exécute la commande Python
# hello docker
```

## Le Dockerfile

Un Dockerfile décrit comment construire une image. Chaque ligne = une étape. Voici la version la plus simple possible :

### Version basique (pour comprendre)

```dockerfile
FROM python:3.12          # Partir d'une image qui contient déjà Python
WORKDIR /app              # Se placer dans le dossier /app dans le container
COPY . .                  # Copier tout ton code dans le container
RUN pip install fastapi uvicorn  # Installer les dépendances
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
                          # La commande qui lance l'app quand le container démarre
```

5 lignes, c'est tout. Ça marche. Mais en production, on peut faire mieux — image plus légère, dépendances mieux gérées, etc.

**Les instructions :**

| Instruction | Ce que ça fait |
|------------|---------------|
| `FROM` | Image de base (toujours en premier) |
| `WORKDIR` | Définit le dossier de travail dans le container |
| `COPY` | Copie des fichiers de ta machine vers le container |
| `RUN` | Exécute une commande pendant la construction de l'image |
| `CMD` | La commande qui se lance quand le container démarre |

### Version bonnes pratiques (ce qu'on utilise dans le projet)

Le projet utilise une version améliorée. Voici les différences et pourquoi :

```dockerfile
# "slim" = version allégée de Python (150 Mo au lieu de 900 Mo)
# Moins de logiciels pré-installés, mais suffisant pour notre app
FROM python:3.12-slim

# Installer uv (le gestionnaire de dépendances rapide, vu au Module 0)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Bonne pratique : copier les fichiers de dépendances AVANT le code
# Pourquoi ? Docker met en cache chaque étape. Si tu changes ton code mais pas
# tes dépendances, Docker ne réinstalle pas les dépendances → build beaucoup plus rapide
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
# --frozen = utiliser le fichier uv.lock tel quel (versions exactes, pas de surprise)
# --no-dev = ne pas installer pytest, ruff, etc. (inutiles en production)

# Maintenant on copie le code (après les dépendances pour le cache)
COPY . .

# --host 0.0.0.0 = écouter sur toutes les interfaces réseau
# Sans ça, l'app n'écoute que sur localhost DANS le container → impossible d'y accéder depuis l'extérieur
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Basique | Bonnes pratiques | Pourquoi |
|---------|-----------------|----------|
| `python:3.12` (900 Mo) | `python:3.12-slim` (150 Mo) | Image 6x plus légère |
| `pip install` | `uv sync --frozen` | Plus rapide, versions verrouillées |
| `COPY . .` en une fois | Dépendances d'abord, code ensuite | Cache Docker = builds plus rapides |
| Toutes les dépendances | `--no-dev` | Pas de pytest/ruff en production |

## Commandes Docker essentielles

> **Ces commandes sont des exemples** pour comprendre la syntaxe. Tu les utiliseras pour de vrai dans la section "Projet pratique" plus bas. Pas besoin de les taper maintenant.

**"Build" (construire)** = transformer ton code source en quelque chose de prêt à tourner. Pour Docker, `docker build` lit ton Dockerfile et crée une image à partir des instructions.

```bash
# Construire une image
docker build -t mon-app:1.0 .
# -t = tag (nom:version) — le nom que tu donnes à l'image
# . = le "contexte" — le dossier que Docker utilise pour trouver les fichiers
#     quand ton Dockerfile fait COPY, il copie depuis CE dossier
#     le "." veut dire "le dossier dans lequel je suis actuellement"

# Lancer un container
docker run -d -p 8000:8000 --name mon-backend mon-app:1.0
# -d = détaché (tourne en arrière-plan, tu récupères ton terminal)
# -p 8000:8000 = port machine:port container (vu au Module 2)
# --name = donner un nom au container (optionnel mais pratique)

# Lister les containers qui tournent
docker ps

# Voir TOUS les containers (même arrêtés)
docker ps -a

# Voir les logs d'un container
docker logs mon-backend

# Suivre les logs en temps réel (Ctrl+C pour arrêter)
docker logs -f mon-backend

# Arrêter un container
docker stop mon-backend

# Supprimer un container (il doit être arrêté d'abord)
docker rm mon-backend

# Entrer dans un container en cours d'exécution
docker exec -it mon-backend bash
# -i = interactif (tu peux taper des commandes)
# -t = terminal (affiche un prompt)
# bash = ouvrir un terminal bash dans le container
# Tu es maintenant "dans" le container — tape "exit" pour en sortir
```

## Volumes

Un container est éphémère — quand tu le supprimes, ses données disparaissent. Un **volume** persiste les données même après suppression du container. Essentiel pour les bases de données.

> **Cet exemple est pour comprendre le concept.** Dans le projet, on utilise Docker Compose qui gère les volumes automatiquement — pas besoin de taper cette commande.

```bash
docker run -d -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  --name ma-db \
  postgres:16
# Le "\" à la fin de chaque ligne = la commande continue sur la ligne suivante
#   (c'est juste pour la lisibilité, c'est une seule commande)
# -v postgres_data:/var/lib/postgresql/data = créer un volume nommé "postgres_data"
#   qui pointe vers le dossier des données PostgreSQL DANS le container
# postgres_data = nom du volume (Docker le gère, tu n'as pas à savoir où c'est stocké)
```

## Comment les containers communiquent entre eux

Quand tu utilises Docker Compose, un réseau est créé automatiquement. Chaque container est accessible par **le nom de son service** dans le fichier `docker-compose.yml`.

Dans notre projet :
- Le backend accède à PostgreSQL via `db:5432` (pas `localhost:5432`)
- Le frontend (nginx) accède au backend via `backend:8000` (pas `localhost:8000`)

**Pourquoi pas `localhost` ?** Chaque container est isolé. `localhost` dans le container backend, c'est le backend lui-même — pas la base de données. Pour parler à un autre container, tu utilises son **nom de service** (`db`, `backend`, `frontend`).

Docker fait tourner un serveur DNS interne (comme le DNS d'Internet vu au Module 2) qui traduit le nom du service en adresse IP du container.

## Docker Compose

Docker Compose gère plusieurs containers ensemble dans un seul fichier YAML. Au lieu de lancer chaque container un par un avec `docker run`, tu décris tout dans un fichier `docker-compose.yml` et tu lances tout d'un coup.

Les commandes principales :

```bash
docker compose up -d          # Lancer tous les services (-d = en arrière-plan)
docker compose up -d --build  # Lancer + reconstruire les images (après un changement de code)
docker compose ps             # Voir l'état de tous les services
docker compose logs -f        # Voir les logs en temps réel (Ctrl+C pour arrêter)
docker compose down           # Tout arrêter et supprimer les containers
```

On verra le fichier `docker-compose.yml` du projet dans la section pratique juste en dessous.

## `.dockerignore` — Ne pas tout copier

Quand tu fais `COPY . .` dans un Dockerfile, Docker copie **tout** le dossier dans l'image. Y compris `.git/` (historique Git, peut faire 100+ Mo), `node_modules/`, `.venv/`, `.env` (secrets !)...

Le fichier `.dockerignore` fonctionne exactement comme `.gitignore` (vu au Module 0) : il dit à Docker quels fichiers **ne pas copier**. Le projet en a déjà un dans chaque dossier :

```
# backend/.dockerignore (déjà dans le projet)
.venv/
__pycache__/
.git/
.env
test_main.py
```

```
# frontend/.dockerignore (déjà dans le projet)
node_modules/
dist/
.git/
.env
```

Sans `.dockerignore`, tes images seront inutilement lourdes et potentiellement dangereuses (secrets dans l'image).

## Debugger un container qui crash

C'est 50% du quotidien DevOps. Un container ne démarre pas ou crash en boucle. Voilà la méthode :

### Étape 1 — Voir l'état du container

```bash
docker ps -a
# CONTAINER ID  IMAGE       STATUS                     NAMES
# abc123        mon-app     Exited (1) 30 seconds ago  backend
#                           ^^^^^^ le code de sortie (1 = erreur)
```

### Étape 2 — Lire les logs

```bash
docker logs backend
# Traceback (most recent call last):
#   File "main.py", line 2, in <module>
#     from fastapi import FastAPI
# ModuleNotFoundError: No module named 'fastapi'
# ← Les dépendances ne sont pas installées dans l'image !
```

### Étape 3 — Entrer dans le container pour investiguer

Si le container tourne encore :
```bash
docker exec -it backend bash
# Tu es maintenant dans le container, tu peux explorer
ls /app/
cat /app/pyproject.toml
```

Si le container a crashé (impossible de `exec`), lance un nouveau container avec bash au lieu de l'app :
```bash
docker run -it --entrypoint bash mon-app:1.0
# --entrypoint bash = au lieu de lancer l'app, ouvre un terminal bash
# Tu es dans le container, l'app n'a pas démarré
# Tu peux explorer, tester des commandes, comprendre ce qui ne va pas
# Tape "exit" pour en sortir
```

### Les erreurs les plus fréquentes

| Symptôme | Cause probable | Fix |
|----------|---------------|-----|
| `Exited (1)` | Erreur dans l'app (bug, dépendance manquante) | `docker logs` pour lire l'erreur |
| `Exited (137)` | Container tué (Out Of Memory) | Augmenter la mémoire ou optimiser l'app |
| Container restart en boucle | L'app crash au démarrage | Logs + vérifier le CMD/ENTRYPOINT |
| `port already in use` | Un autre container/process utilise ce port | `docker ps` ou `ss -tlnp` |

## Multi-stage builds

Un Dockerfile peut avoir **plusieurs étapes**. L'idée : utiliser une grosse image pour construire l'app (avec tous les outils), puis copier uniquement le résultat dans une petite image légère.

C'est ce qu'on fait pour le frontend : on a besoin de Bun pour builder le code React, mais en production on a juste besoin de nginx pour servir les fichiers HTML/JS/CSS générés.

```dockerfile
# Étape 1 : Builder le frontend (image lourde avec Bun)
FROM oven/bun:latest AS build
# "AS build" = donner un nom à cette étape pour y faire référence plus tard
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
# --frozen-lockfile = utiliser les versions exactes du fichier bun.lock (même idée que --frozen pour uv)
COPY . .
RUN bun run build
# Ça génère un dossier "dist/" avec les fichiers HTML/JS/CSS prêts à servir

# Étape 2 : Servir en production (image légère avec nginx)
FROM nginx:alpine
# "alpine" = version ultra-légère de Linux (~5 Mo)
COPY --from=build /app/dist /usr/share/nginx/html
# --from=build = copier depuis l'étape 1 (pas depuis ta machine)
# On ne copie QUE le résultat du build, pas Bun ni node_modules
EXPOSE 80
```

**Résultat :** L'image finale ne contient que nginx (~20 Mo) + les fichiers buildés (~2 Mo). Pas Bun, pas node_modules (300+ Mo). C'est beaucoup plus léger et sécurisé.

## Projet pratique : Dockerize le projet fil rouge

### 1. Dockerfile pour le backend

Le projet fournit déjà les Dockerfiles. Voici celui du backend (`backend/Dockerfile`) :
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

Le frontend utilise un **multi-stage build** (`frontend/Dockerfile`) :
```dockerfile
FROM oven/bun:latest AS build
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

Le fichier `frontend/nginx.conf` configure nginx (le serveur web) :
```nginx
server {
    listen 80;                              # Écouter sur le port 80 (HTTP)

    location / {                            # Quand quelqu'un accède à "/"
        root /usr/share/nginx/html;         # Servir les fichiers buildés (HTML/JS/CSS)
        try_files $uri /index.html;         # Si le fichier demandé n'existe pas, renvoyer index.html
                                            # (nécessaire pour React qui gère ses propres URLs)
    }

    location /api {                         # Quand quelqu'un accède à "/api/..."
        proxy_pass http://backend:8000;     # Rediriger vers le container backend sur le port 8000
                                            # "backend" = le nom du service dans docker-compose.yml
    }
}
```

En résumé : nginx sert le frontend ET redirige les appels `/api` vers le backend. C'est le **reverse proxy** (vu au Module 2).

### 3. Docker Compose

Le projet fournit déjà un `docker-compose.yml` avec backend + frontend + PostgreSQL :
```yaml
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
      - "80:80"
    depends_on:
      - backend

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

Ce qu'il y a de nouveau par rapport aux exemples précédents :
- **`db`** : un service PostgreSQL. **PostgreSQL** est un logiciel de base de données — il stocke les données de façon permanente (les tâches de notre app). L'image `postgres:16` vient de Docker Hub (un site web qui héberge des images Docker prêtes à l'emploi, comme un catalogue), pas besoin de Dockerfile.
- **`environment`** : les variables d'environnement passées au container. Le backend utilise `DATABASE_URL` pour se connecter à PostgreSQL au lieu du stockage in-memory.

> **Le pattern "variable d'environnement"** : En DevOps, on ne modifie jamais le code pour changer d'environnement. Le même code tourne en local, en staging, et en prod. Ce qui change, ce sont les variables d'environnement. Ici, `DATABASE_URL` est absente en local (→ in-memory) et présente avec Docker Compose (→ PostgreSQL). Tu retrouveras ce pattern dans tous les modules suivants.

> Les variables d'environnement sont expliquées dans le Module 1 (Linux). Docker les passe aux containers via `environment:` ou `-e`.

- **`volumes`** : `postgres_data` persiste les données de la base. Sans ça, les données disparaissent quand tu fais `docker compose down`.
- **`depends_on`** : Docker lance le backend après la base. **Attention :** `depends_on` garantit que le container DB est **lancé**, pas que PostgreSQL est **prêt à recevoir des connexions**. En pratique, la DB met quelques secondes à démarrer. Si le backend crash au premier lancement parce que la DB n'est pas prête, un `docker compose restart backend` suffit. En production, on ajoute un script de retry ou un health check sur la DB.

> **Pourquoi `/api/health` ?** L'endpoint health check (`GET /api/health → {"status": "ok"}`) ne fait rien de métier. Il sert aux outils qui surveillent l'application : Docker vérifie que le container répond, Kubernetes décide si le pod est prêt à recevoir du traffic (Module 8), le load balancer retire un serveur qui ne répond plus (Module 5). C'est un standard — quasiment toute app en production expose un `/health`.

### Comment le backend passe de in-memory à PostgreSQL

En local (sans Docker), le backend stocke les tâches dans une simple liste Python en mémoire. C'est suffisant pour développer et tester.

Avec Docker Compose, on passe la variable `DATABASE_URL` au backend. Le code de `main.py` vérifie si cette variable existe :
- **`DATABASE_URL` absente** → stockage in-memory (liste Python)
- **`DATABASE_URL` présente** → connexion à PostgreSQL

C'est le même code, le même fichier `main.py`. Seule la variable d'environnement change le comportement. Ce pattern est très courant en DevOps : on ne modifie pas le code entre les environnements, on change la configuration.

### 4. Lance tout

```bash
cd ~/devops-project
docker compose up -d --build
# [+] Building ...
# [+] Running 3/3
# ✔ Container devops-project-db-1        Started
# ✔ Container devops-project-backend-1   Started
# ✔ Container devops-project-frontend-1  Started

# Vérifie
docker compose ps
# 3 services running

curl http://localhost:8000/api/tasks
# [{"id":1,"title":"Apprendre Docker","done":false}, ...]

# Ouvre http://localhost dans ton navigateur
```

💡 **Si le build échoue :** vérifie que le Dockerfile est bien dans le bon dossier et que les fichiers référencés existent.

### 5. Tester la persistence des données

C'est le moment de vérifier que les volumes PostgreSQL fonctionnent vraiment. On va ajouter une tâche, arrêter tout, relancer, et vérifier qu'elle est toujours là.

```bash
# 1. Ajouter une tâche via curl
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Cette tâche survit au redémarrage"}'
# {"id":3,"title":"Cette tâche survit au redémarrage","done":false}

# 2. Vérifier qu'elle existe
curl http://localhost:8000/api/tasks
# [..., {"id":3,"title":"Cette tâche survit au redémarrage","done":false}]

# 3. Tout arrêter (les containers sont supprimés)
docker compose down
# [+] Running 3/3
# ✔ Container devops-project-frontend-1  Removed
# ✔ Container devops-project-backend-1   Removed
# ✔ Container devops-project-db-1        Removed

# 4. Tout relancer
docker compose up -d
# Les containers sont recréés, mais le volume postgres_data est toujours là

# 5. Vérifier que la tâche est toujours là
curl http://localhost:8000/api/tasks
# [..., {"id":3,"title":"Cette tâche survit au redémarrage","done":false}]
# ✅ Elle est toujours là ! Le volume a persisté les données.
```

**Pourquoi ça marche :** `docker compose down` supprime les containers mais **pas les volumes**. PostgreSQL stocke ses données dans le volume `postgres_data`, qui survit aux redémarrages.

**Maintenant, compare avec le mode in-memory :**

```bash
# Arrête Docker Compose
docker compose down

# Lance le backend sans Docker (= sans DATABASE_URL = mode in-memory)
cd ~/devops-project/backend
uv run uvicorn main:app --reload &

# Tu vois les 2 tâches de démo, mais PAS celle que tu as ajoutée
curl http://localhost:8000/api/tasks
# [{"id":1,"title":"Apprendre Docker","done":false},{"id":2,"title":"Configurer CI/CD","done":false}]
# La tâche ajoutée a disparu — le stockage in-memory ne persiste rien

# Arrête le serveur
kill %1
```

C'est concrètement la différence entre une base de données (les données survivent) et le stockage en mémoire (tout disparaît au redémarrage). En production, on utilise toujours une base de données avec un volume.

## Exercice debug : Trouve les 3 erreurs

Le `docker-compose.yml` suivant contient 3 erreurs. Trouve-les avant de regarder les indices.

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@localhost:5432/tasks

  frontend:
    build: ./frontend
    ports:
      - "8000:80"
    depends_on:
      - backend

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=tasks
```

<details>
<summary>💡 Indice 1</summary>

Regarde les ports exposés par le backend et le frontend. Deux services peuvent-ils utiliser le même port sur ta machine ?

</details>

<details>
<summary>💡 Indice 2</summary>

Regarde le `DATABASE_URL` du backend. À quelle machine fait référence `localhost` dans un container Docker ?

</details>

<details>
<summary>💡 Indice 3</summary>

Si tu fais `docker compose down` puis `docker compose up`, les données de PostgreSQL survivent-elles ?

</details>

<details>
<summary>✅ Solution</summary>

**Erreur 1 — Conflit de ports :** Le backend ET le frontend utilisent le port `8000` côté machine. Le frontend devrait être sur un autre port, par exemple `"80:80"` ou `"3000:80"`.

**Erreur 2 — `localhost` au lieu du nom du service :** Dans un container, `localhost` désigne le container lui-même, pas la machine hôte. Le backend doit se connecter à `db:5432` (le nom du service Docker Compose), pas à `localhost:5432`. Fix : `DATABASE_URL=postgresql://user:pass@db:5432/tasks`.

**Erreur 3 — Pas de volume pour PostgreSQL :** Sans volume, les données disparaissent quand le container est supprimé. Il faut ajouter :
```yaml
  db:
    # ...
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

</details>

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

**Q : Différence entre CMD et ENTRYPOINT ?**
R : `CMD` = la commande par défaut, remplaçable au lancement (`docker run mon-app echo "autre chose"` remplace le CMD). `ENTRYPOINT` = la commande fixe, les arguments du `docker run` sont ajoutés après. En pratique, `CMD` suffit dans 90% des cas. On utilise `ENTRYPOINT` quand le container a un seul rôle et qu'on ne veut pas que quelqu'un puisse remplacer la commande.

## Bonnes pratiques

- **Toujours un `.dockerignore`.** Sans ça, `COPY . .` embarque `.git/`, `node_modules/`, `.env` (secrets) dans ton image.
- **Images légères.** Utilise `python:3.12-slim` au lieu de `python:3.12` (900 Mo vs 150 Mo). Utilise le multi-stage build pour le frontend.
- **Un processus par container.** Ne mets pas l'API et la DB dans le même container. Sépare les responsabilités.
- **Ne tourne pas en root dans le container.** Ajoute `USER appuser` dans le Dockerfile. Si le container est compromis, l'attaquant a moins de pouvoir.
- **Copie les dépendances avant le code.** `COPY pyproject.toml .` puis `RUN uv sync`, puis `COPY . .`. Comme ça Docker cache les dépendances et ne les réinstalle que si le fichier de dépendances change.
- **Tag tes images.** Ne te repose pas sur `:latest`. Utilise des tags explicites (`:v1.2`, `:abc123` avec le hash du commit).
- **Nettoie régulièrement.** `docker system prune` supprime les images, containers et volumes orphelins. Sans ça, ton disque se remplit en quelques jours.

```bash
# Voir l'espace utilisé par Docker
docker system df
# TYPE           TOTAL   ACTIVE   SIZE      RECLAIMABLE
# Images         15      3        4.2GB     3.1GB (73%)

# Nettoyer tout ce qui n'est pas utilisé
docker system prune -a
# WARNING! This will remove all stopped containers, unused networks, unused images...
# Total reclaimed space: 3.1GB
```

## Erreurs courantes

- **"Permission denied" avec docker** → Tu n'as pas fait `usermod -aG docker $USER` ou tu ne t'es pas reconnecté.
- **"Port already in use"** → Un autre processus utilise ce port. `docker ps` pour voir ou `ss -tlnp | grep PORT`.
- **Oublier `-p` au `docker run`** → Le container tourne mais tu ne peux pas y accéder depuis ta machine.
- **Modifier le code sans rebuilder** → `docker compose up -d --build` pour reconstruire après un changement.
- **Disque plein** → `docker system prune -a` pour nettoyer. Les images Docker s'accumulent vite.
- **Gros images** → `.dockerignore` + images `-slim`/`-alpine` + multi-stage build.

## Pour aller plus loin

- **Docker security** : rootless Docker, ne pas tourner en root dans le container
- **Podman** : alternative à Docker, sans daemon (plus sécurisé)
- **Docker Swarm** : orchestration basique intégrée à Docker
- **Optimisation d'images** : `.dockerignore`, ordre des layers, cache
- **BuildKit** : le nouveau builder Docker, plus rapide
- **Distroless images** : images ultra-minimalistes de Google

## Tu peux passer au module suivant si...

- [ ] Tu sais la différence entre image et container
- [ ] Tu sais lire un Dockerfile (FROM, COPY, RUN, CMD)
- [ ] Tu sais faire `docker build`, `docker run -d -p`, `docker ps`, `docker logs`
- [ ] Tu sais écrire un `docker-compose.yml` et lancer `docker compose up -d`
- [ ] Le projet fil rouge tourne avec `docker compose up -d --build` (backend + frontend + PostgreSQL)
- [ ] Tu comprends le service discovery (les containers se trouvent par leur nom de service)
- [ ] Tu comprends pourquoi les volumes sont nécessaires pour persister les données
