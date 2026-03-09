# Module 0 : Prérequis

> **Prérequis :** Aucun — c'est le point de départ !

> **En résumé :** Tu installes ton environnement de travail (WSL + VS Code + outils) et tu apprends Git — le système de sauvegarde et de collaboration que tu utiliseras dans TOUS les modules suivants. Tu mets aussi en place le projet fil rouge (React + FastAPI) que tu feras évoluer tout au long du cursus.

## C'est quoi et pourquoi ?

Avant de faire du DevOps, il te faut deux choses : un **environnement Linux** (parce que 90% des serveurs tournent sous Linux) et **Git** (parce que tout le code vit dans Git).

**C'est quoi un serveur ?** Un serveur, c'est juste un ordinateur qui tourne 24/7 et qui répond aux demandes d'autres ordinateurs. Quand tu tapes `google.com`, ton navigateur envoie une demande à un serveur de Google, qui lui répond avec la page web. Le serveur de ton application, c'est l'ordinateur sur lequel ton app tourne et attend les requêtes des utilisateurs.

**Git**, c'est comme un **système de sauvegarde de jeu vidéo**. Chaque commit = un point de sauvegarde. Tu peux revenir en arrière, créer des branches (des univers parallèles), et fusionner le tout. Sans Git, c'est `projet_final_v2_FINAL_vraiment_final.zip`.

**WSL** (Windows Subsystem for Linux) te permet de faire tourner un vrai Linux dans Windows, sans machine virtuelle lourde.

## Installation WSL2 + Ubuntu

Ouvre **PowerShell en administrateur** et tape :

```powershell
wsl --install
```

Ça installe WSL2 + Ubuntu. Redémarre ton PC. Au redémarrage, Ubuntu s'ouvre et te demande un nom d'utilisateur et un mot de passe.

Vérifie que ça marche :
```bash
wsl --list --verbose
# Tu dois voir : Ubuntu    Running    2
```

## Installation VS Code + Remote WSL

1. Installe [VS Code](https://code.visualstudio.com/)
2. Installe l'extension **WSL** (cherche "WSL" dans les extensions)
3. Dans Ubuntu, tape `code .` dans n'importe quel dossier — ça ouvre VS Code connecté à WSL

## Installation Python, uv et Bun (les outils du projet)

> **Tu n'as pas besoin d'apprendre Python ou Bun pour ce cursus.** On les installe parce que le projet fil rouge en a besoin (backend en Python, frontend en JavaScript). Tu vas juste copier-coller les commandes pour installer et lancer l'app. Le but du cursus, c'est le DevOps, pas le développement.

Avant de commencer, quelques termes que tu vas voir partout :

| Terme | Explication simple |
|-------|-------------------|
| **Application (app)** | Un programme qui fait quelque chose. Notre app = une liste de tâches. |
| **Dépendance (= paquet)** | Un bout de code écrit par quelqu'un d'autre que ton app utilise. Au lieu de tout coder toi-même, tu réutilises du travail existant. Comme des ingrédients tout prêts au lieu de tout faire de zéro. On appelle aussi ça un **paquet** (package en anglais) parce que c'est du code empaqueté et prêt à être installé. FastAPI est un paquet. Pytest est un paquet. |
| **Gestionnaire de paquets** | Un outil qui télécharge, installe et met à jour les paquets (dépendances) automatiquement. Tu lui dis "j'ai besoin de FastAPI" et il va le chercher sur Internet, l'installe, et gère les mises à jour. Chaque langage a le sien : **pip/uv** pour Python, **npm/bun** pour JavaScript, **apt** pour Linux. |
| **Framework** | Un ensemble d'outils prêts à l'emploi pour créer un type d'application. FastAPI est un framework pour créer des API en Python. React est un framework pour créer des interfaces web. |
| **API** | Application Programming Interface — un moyen pour deux programmes de se parler. Concrètement, c'est un ensemble d'URLs (comme `/api/tasks`) sur lesquelles on peut envoyer des requêtes et recevoir des réponses (en JSON). |
| **Endpoint** | Une URL précise d'une API qui fait une action. `GET /api/tasks` est un endpoint qui retourne la liste des tâches. |

### Python — Le backend

Python est un langage de programmation très populaire. Notre backend (API FastAPI) est écrit en Python. Tu as juste besoin de l'installer :

```bash
sudo apt update && sudo apt install -y python3
python3 --version
# Python 3.x.x
```

### uv — Le gestionnaire de dépendances Python

Historiquement, pour gérer les dépendances Python, on utilisait **pip** (le gestionnaire de paquets de Python — il télécharge et installe les dépendances) + **venv** (un outil qui crée un dossier isolé pour chaque projet, pour que les dépendances d'un projet n'interfèrent pas avec celles d'un autre — imagine des boîtes séparées pour chaque recette). Ça marche, mais c'est lent et verbeux.

**uv** est une alternative récente qui remplace pip + venv en un seul outil, beaucoup plus rapide et simple à utiliser. C'est le même concept, juste un meilleur outil.

| | pip + venv (ancien) | uv (ce qu'on utilise) |
|--|--------------------|-----------------------|
| Créer un environnement | `python3 -m venv venv && source venv/bin/activate` | `uv sync` (automatique) |
| Installer les dépendances | `pip install -r requirements.txt` | `uv sync` |
| Ajouter une dépendance | Éditer `requirements.txt` à la main + `pip install` | `uv add fastapi` |
| Lancer une commande | `source venv/bin/activate && pytest` | `uv run pytest` |

> **En entreprise**, tu verras encore beaucoup de `pip` + `requirements.txt`. uv est plus récent mais gagne rapidement du terrain. Les concepts sont les mêmes, seuls les outils changent.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Relance ton terminal, puis :
uv --version
# uv 0.x.x
```

### Bun — Le frontend

Pour faire tourner du JavaScript, on a historiquement besoin de **Node.js** (un programme qui permet d'exécuter du code JavaScript en dehors du navigateur) et **npm** (le gestionnaire de paquets de JavaScript — comme pip pour Python, il installe les dépendances). **Bun** est une alternative récente qui fait les deux en un seul outil, en beaucoup plus rapide.

En résumé : Bun = Node.js + npm, mais plus rapide et plus simple. On l'utilise ici pour cette raison.

```bash
curl -fsSL https://bun.sh/install | bash
# Relance ton terminal, puis :
bun --version
# 1.x.x
```

> **En entreprise**, tu verras souvent `npm install` / `npm run dev` au lieu de `bun install` / `bun run dev`. C'est la même chose, juste un outil différent.

## Git — Les 7 commandes essentielles

### Configurer Git (une seule fois)
```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton@email.com"
```

### Les commandes

| Commande | Ce que ça fait | Analogie |
|----------|---------------|----------|
| `git init` | Crée un nouveau repo | Commencer une nouvelle partie |
| `git add fichier` | Prépare un fichier pour le commit | Mettre des objets dans le carton |
| `git commit -m "message"` | Sauvegarde | Point de sauvegarde |
| `git push` | Envoie sur GitHub | Upload ta sauvegarde dans le cloud |
| `git pull` | Récupère depuis GitHub | Télécharge la dernière sauvegarde |
| `git branch nom` | Crée une branche | Ouvrir un univers parallèle |
| `git merge nom` | Fusionne une branche | Combiner deux univers |

### Workflow basique

```bash
# Voir l'état actuel
git status

# Ajouter des fichiers modifiés
git add main.py
# Ou tout ajouter d'un coup :
git add .

# Sauvegarder
git commit -m "ajout endpoint GET /tasks"

# Envoyer sur GitHub
git push
```

### Branches

```bash
# Créer et aller sur une branche
git checkout -b ma-feature

# Travailler, commit, etc.
git add .
git commit -m "ajout feature X"

# Revenir sur main et fusionner
git checkout main
git merge ma-feature
```

## Créer un compte GitHub

1. Va sur [github.com](https://github.com) et crée un compte
2. Crée un nouveau repository : bouton **+** → **New repository**
3. Nomme-le `devops-project`, laisse-le public, ne coche rien d'autre

## Projet pratique : Mettre en place le projet fil rouge

### 1. Créer le dossier du projet

```bash
mkdir -p ~/devops-project
cd ~/devops-project
git init
```

### 2. Copier le code de l'application

Copie les dossiers `frontend/` et `backend/` depuis le dossier `devops-project/` fourni dans ce cursus.

```bash
# Structure attendue :
# ~/devops-project/
#   docker-compose.yml
#   frontend/
#     Dockerfile, nginx.conf, package.json, vite.config.js, src/App.jsx, ...
#   backend/
#     Dockerfile, main.py, test_main.py, pyproject.toml, uv.lock
```

> **C'est quoi le frontend/backend ?** Le **backend** est la partie invisible — le programme qui tourne sur le serveur, gère les données, et répond aux demandes. Ici, c'est écrit en Python avec FastAPI. Le **frontend** est la partie visible — la page web que l'utilisateur voit dans son navigateur. Ici, c'est écrit en JavaScript avec React. Le frontend appelle le backend via des requêtes HTTP (`GET /api/tasks`, `POST /api/tasks`, etc.) et affiche les réponses. Tu n'as pas besoin de comprendre le code React ou FastAPI pour ce cursus — juste de savoir que le frontend appelle le backend.

### 3. Lancer le backend

```bash
cd ~/devops-project/backend
uv sync
# Resolved 12 packages in 0.5s
# Installed 12 packages in 0.3s

uv run uvicorn main:app --reload
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

`uv sync` crée automatiquement un environnement isolé et installe toutes les dépendances listées dans le fichier `pyproject.toml` (le fichier qui dit "ce projet a besoin de FastAPI, Pytest, etc."). `uv run` exécute une commande dans cet environnement.

Teste dans un autre terminal :
```bash
curl http://localhost:8000/api/tasks
# [{"id":1,"title":"Apprendre Docker","done":false}, ...]
```

### 4. Lancer le frontend

```bash
cd ~/devops-project/frontend
bun install
bun run dev
# VITE v6.x.x  ready in xxx ms
# ➜  Local:   http://localhost:3000/
```

### 5. Ajouter un `.gitignore`

Avant de commit, crée un fichier `.gitignore` à la racine du projet. Ce fichier dit à Git **quels fichiers ignorer** — ne pas les inclure dans les commits.

Sans `.gitignore`, tu vas committer `node_modules/` (des milliers de fichiers), `.venv/` (l'environnement Python), et potentiellement des fichiers `.env` contenant des mots de passe.

Le projet en fournit déjà un, mais voici ce qu'il contient et pourquoi :

```bash
cat .gitignore
# __pycache__/     ← fichiers compilés Python (inutiles, régénérés automatiquement)
# .venv/           ← environnement virtuel Python (lourd, chaque dev le recrée avec uv sync)
# node_modules/    ← dépendances JS (lourd, chaque dev les recrée avec bun install)
# dist/            ← fichiers buildés du frontend (régénérés par bun run build)
# .env             ← variables d'environnement (SECRETS! ne jamais committer)
# *.tfstate        ← state Terraform (peut contenir des secrets)
# .terraform/      ← dossier interne Terraform
```

### 6. Premier commit et push

```bash
cd ~/devops-project
git add .
git status
# Vérifie que tu ne vois PAS node_modules/, .venv/, .env dans la liste

git commit -m "init: projet task list (React + FastAPI)"
git remote add origin https://github.com/TON_USER/devops-project.git
git push -u origin main
```

> **Note :** En entreprise, le frontend et le backend sont généralement dans des dépôts (repos) séparés, avec chacun son propre pipeline CI/CD. Ici, on les met dans le même repo pour simplifier l'apprentissage.

💡 **Si tu es bloqué sur le push :** GitHub te demande peut-être de t'authentifier. Utilise un [Personal Access Token](https://github.com/settings/tokens) ou configure SSH.

### 7. Le workflow Pull Request (comment on travaille en équipe)

Jusqu'ici on push directement sur `main`. **En entreprise, personne ne fait ça.** On passe par des Pull Requests (PR) pour que quelqu'un relise le code avant de le merger.

Le workflow réel :

```bash
# 1. Créer une branche pour ta feature
git checkout -b feat/add-delete-endpoint

# 2. Travailler, commit
git add .
git commit -m "feat: ajout endpoint DELETE /api/tasks/{id}"

# 3. Pousser la branche sur GitHub
git push -u origin feat/add-delete-endpoint
```

Ensuite, sur GitHub :
1. Tu verras un bouton **"Compare & pull request"**
2. Tu décris ce que tu as fait et pourquoi
3. Un collègue relit ton code (code review)
4. Si c'est bon → **Merge** la PR dans `main`
5. La branche est supprimée

**Pourquoi c'est important :**
- Quelqu'un d'autre vérifie ton code avant qu'il arrive en prod
- On garde un historique de POURQUOI chaque changement a été fait
- Le pipeline CI/CD tourne sur la PR → tu sais si ça casse AVANT de merger

> Dans ce cursus, tu peux continuer à push directement sur main pour simplifier. Mais sache que le workflow PR, c'est le standard en entreprise.

### Exercice : Faire ta première PR

On va ajouter une vraie feature à l'app : un endpoint pour récupérer une tâche par son ID (`GET /api/tasks/{task_id}`). Tu n'as pas besoin de comprendre le code Python — juste de le copier, tester, et faire la PR.

**Étape 1 — Créer une branche**

```bash
cd ~/devops-project
git checkout -b feat/get-single-task
```

**Étape 2 — Ajouter le code**

Ouvre `backend/main.py` et ajoute ce bloc **juste avant** la ligne `@app.get("/api/health")` :

```python
@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    tasks = _list_tasks()
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")
```

**Étape 3 — Tester en local**

```bash
cd ~/devops-project/backend
uv run uvicorn main:app --reload &

curl http://localhost:8000/api/tasks/1
# {"id":1,"title":"Apprendre Docker","done":false}

curl http://localhost:8000/api/tasks/99999
# {"detail":"Task not found"} (avec un code 404)

# Arrêter le serveur
kill %1
```

**Étape 4 — Commit et push**

```bash
git add backend/main.py
git commit -m "feat: add GET endpoint to retrieve single task by ID"
git push -u origin feat/get-single-task
```

**Étape 5 — Créer la PR sur GitHub**

1. Va sur ton repo GitHub — tu verras un bandeau jaune **"Compare & pull request"**
2. Titre : `feat: add GET endpoint to retrieve single task by ID`
3. Description : explique ce que tu as ajouté et comment le tester
4. Clique **Create pull request**
5. Regarde la PR, puis clique **Merge pull request**
6. Reviens en local et mets-toi à jour :

```bash
git checkout main
git pull
```

C'est exactement ce workflow que tu feras des centaines de fois en entreprise. La différence, c'est qu'en vrai un collègue review ta PR avant le merge.

### Bonus : comprendre le frontend (copier-coller)

Le frontend (`frontend/src/App.jsx`) est la page web que l'utilisateur voit. Tu n'as pas besoin de comprendre React — juste de savoir que **le frontend appelle le backend via des requêtes HTTP**.

Ouvre `frontend/src/App.jsx` et regarde les commentaires dans le code. Chaque fonction correspond à un appel vers le backend :

| Ce que fait l'utilisateur | Fonction JS | Appel HTTP |
|--------------------------|-------------|------------|
| La page se charge | `useEffect` | `GET /api/tasks` |
| Clic sur "Ajouter" | `addTask` | `POST /api/tasks` |
| Clic sur une tâche | `toggleTask` | `PATCH /api/tasks/{id}` |
| Clic sur "✕" | `deleteTask` | `DELETE /api/tasks/{id}` |

Lance le frontend et le backend en même temps pour voir le résultat :

```bash
# Terminal 1 — Backend
cd ~/devops-project/backend
uv run uvicorn main:app --reload

# Terminal 2 — Frontend
cd ~/devops-project/frontend
bun run dev
# Ouvre http://localhost:3000
```

Tu devrais voir la liste de tâches. Essaie :
- Ajouter une tâche → elle apparaît en bas de la liste
- Cliquer sur une tâche → elle est barrée (done)
- Cliquer sur ✕ → elle disparaît

C'est ça la connexion frontend ↔ backend. Le frontend envoie des requêtes HTTP, le backend répond avec du JSON, et le frontend affiche le résultat.

## Coin entretien

**Q : C'est quoi Git et pourquoi on l'utilise ?**
R : Git est un système de versioning. Il garde l'historique de toutes les modifications du code. On peut revenir en arrière, travailler à plusieurs sans écraser le travail des autres, et créer des branches pour développer des features en parallèle.

**Q : Quelle est la différence entre `git add` et `git commit` ?**
R : `git add` prépare les fichiers (staging area), `git commit` les sauvegarde dans l'historique. C'est comme mettre des objets dans un carton (add) puis fermer et étiqueter le carton (commit).

**Q : C'est quoi une branche ?**
R : Une copie parallèle du code. On développe dessus sans toucher à la branche principale (main). Quand c'est prêt, on fusionne (merge).

**Q : Différence entre `git pull` et `git fetch` ?**
R : `git fetch` télécharge les changements distants sans les appliquer. `git pull` = `git fetch` + `git merge`. Pull applique directement les changements.

## Bonnes pratiques

- **Commits petits et fréquents.** Un commit = un changement logique. Pas "j'ai bossé 3 jours et je commit tout d'un coup". C'est impossible à reviewer et à rollback.
- **Messages de commit clairs.** "fix bug" ne dit rien. "fix: le endpoint POST /tasks retournait 500 si le titre était vide" dit tout. Le message explique **pourquoi**, pas **quoi** (le diff montre le quoi).
- **Ne commit jamais de secrets.** Mots de passe, clés API, tokens → fichier `.env` + `.gitignore`. Si tu as committé un secret par erreur, change-le immédiatement.
- **Un `.gitignore` dès le premier commit.** Avant de commit quoi que ce soit. C'est la première chose à faire dans un projet.
- **Pull avant de push.** `git pull` avant `git push` pour éviter les conflits. Surtout si tu travailles à plusieurs.

## Erreurs courantes

- **"fatal: not a git repository"** → Tu n'es pas dans un dossier avec `git init`. Fais `git init` ou `cd` vers le bon dossier.
- **"Permission denied (publickey)"** → Ton SSH n'est pas configuré pour GitHub. Utilise HTTPS ou configure une clé SSH.
- **Oublier `git add` avant `git commit`** → Le commit sera vide. Toujours vérifier avec `git status` avant de commit.
- **Conflits de merge** → Deux personnes ont modifié la même ligne. Git te montre les deux versions, tu choisis laquelle garder.

## Pour aller plus loin

- **Git rebase** : réécrire l'historique pour le rendre plus propre (utile mais dangereux)
- **Cherry-pick** : prendre un commit spécifique d'une branche et l'appliquer ailleurs
- **Git flow** : une convention pour organiser les branches en équipe
- **Conventional Commits** : une norme pour écrire des messages de commit (`feat:`, `fix:`, `docs:`)
- Doc officielle Git : https://git-scm.com/doc

## Tu peux passer au module suivant si...

- [ ] WSL2 + Ubuntu fonctionnent (tu peux ouvrir un terminal Ubuntu)
- [ ] VS Code s'ouvre avec `code .` depuis WSL
- [ ] `python3 --version`, `uv --version` et `bun --version` retournent quelque chose
- [ ] Tu sais faire `git add`, `git commit`, `git push`
- [ ] Le projet fil rouge est cloné et pushé sur ton GitHub
- [ ] Tu peux lancer le backend (`uv run uvicorn main:app --reload`) et voir la réponse de `curl localhost:8000/api/tasks`
