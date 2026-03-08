# Module 0 : Prérequis

## C'est quoi et pourquoi ?

Avant de faire du DevOps, il te faut deux choses : un **environnement Linux** (parce que 90% des serveurs tournent sous Linux) et **Git** (parce que tout le code vit dans Git).

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

### Python — Le backend

Python est un langage de programmation très populaire. Notre backend (API FastAPI) est écrit en Python. Tu as juste besoin de l'installer :

```bash
sudo apt update && sudo apt install -y python3
python3 --version
# Python 3.x.x
```

### uv — Le gestionnaire de dépendances Python

Historiquement, pour gérer les dépendances Python, on utilisait **pip** (le gestionnaire de paquets) + **venv** (pour isoler les dépendances par projet). Ça marche, mais c'est lent et verbeux.

**uv** est une alternative récente, écrite en Rust, qui remplace pip + venv en un seul outil ultra-rapide. C'est le même concept, juste beaucoup plus rapide et plus simple à utiliser.

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

Pour faire tourner du JavaScript, on a historiquement besoin de **Node.js** (un runtime JS) et **npm** (un gestionnaire de paquets). **Bun** est une alternative récente qui fait les deux en un seul outil, en beaucoup plus rapide. Dans l'industrie, tu verras surtout Node.js + npm, mais Bun gagne du terrain.

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

### 3. Lancer le backend

```bash
cd ~/devops-project/backend
uv sync
# Resolved 12 packages in 0.5s
# Installed 12 packages in 0.3s

uv run uvicorn main:app --reload
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

`uv sync` crée automatiquement un environnement virtuel et installe toutes les dépendances du `pyproject.toml`. `uv run` exécute une commande dans cet environnement.

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

L'app a déjà un endpoint `DELETE /api/tasks/{task_id}` dans le code. Mais imagine qu'il n'existe pas encore et que tu dois l'ajouter. Voici comment tu ferais en équipe :

1. Crée une branche : `git checkout -b feat/add-delete-endpoint`
2. Fais ton changement (ici c'est déjà fait, mais en vrai tu modifierais `main.py`)
3. Teste en local : `curl -X DELETE http://localhost:8000/api/tasks/1`
4. Commit : `git commit -am "feat: add DELETE /api/tasks/{id} endpoint"`
5. Push : `git push -u origin feat/add-delete-endpoint`
6. Va sur GitHub → ouvre la PR → décris ce que tu as fait
7. Merge la PR

C'est exactement ce workflow que tu feras des centaines de fois en entreprise.

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
