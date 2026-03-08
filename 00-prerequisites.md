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

## Installation Python + Bun (les outils du projet)

> **Tu n'as pas besoin d'apprendre Python ou Bun pour ce cursus.** On les installe parce que le projet fil rouge en a besoin (backend en Python, frontend en JavaScript). Tu vas juste copier-coller les commandes pour installer et lancer l'app. Le but du cursus, c'est le DevOps, pas le développement.

### Python — Le backend

Python est un langage de programmation très populaire. Notre backend (API FastAPI) est écrit en Python. Tu as juste besoin de l'installer :

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
python3 --version
# Python 3.x.x
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
#   frontend/
#     package.json, vite.config.js, src/App.jsx, src/main.jsx, ...
#   backend/
#     main.py, test_main.py, requirements.txt, pyproject.toml
```

### 3. Lancer le backend

```bash
cd ~/devops-project/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

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

### 5. Premier commit et push

```bash
cd ~/devops-project
git add .
git commit -m "init: projet task list (React + FastAPI)"
git remote add origin https://github.com/TON_USER/devops-project.git
git push -u origin main
```

> **Note :** En entreprise, le frontend et le backend sont généralement dans des dépôts (repos) séparés, avec chacun son propre pipeline CI/CD. Ici, on les met dans le même repo pour simplifier l'apprentissage.

💡 **Si tu es bloqué sur le push :** GitHub te demande peut-être de t'authentifier. Utilise un [Personal Access Token](https://github.com/settings/tokens) ou configure SSH.

## Coin entretien

**Q : C'est quoi Git et pourquoi on l'utilise ?**
R : Git est un système de versioning. Il garde l'historique de toutes les modifications du code. On peut revenir en arrière, travailler à plusieurs sans écraser le travail des autres, et créer des branches pour développer des features en parallèle.

**Q : Quelle est la différence entre `git add` et `git commit` ?**
R : `git add` prépare les fichiers (staging area), `git commit` les sauvegarde dans l'historique. C'est comme mettre des objets dans un carton (add) puis fermer et étiqueter le carton (commit).

**Q : C'est quoi une branche ?**
R : Une copie parallèle du code. On développe dessus sans toucher à la branche principale (main). Quand c'est prêt, on fusionne (merge).

**Q : Différence entre `git pull` et `git fetch` ?**
R : `git fetch` télécharge les changements distants sans les appliquer. `git pull` = `git fetch` + `git merge`. Pull applique directement les changements.

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
