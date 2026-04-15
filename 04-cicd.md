# Module 4 : CI/CD (GitHub Actions)

> **Prérequis :** Module 0 (Git, GitHub), Module 3 (Docker — build, images)

> **En résumé :** Tu automatises la vérification et le déploiement de ton code avec GitHub Actions. À chaque push, un pipeline vérifie le code (lint), lance les tests, build les images Docker et les pousse sur Docker Hub — sans intervention humaine.

> Dans le Module 3, tu as appris à construire des images Docker et à les lancer avec `docker compose`. Mais qui construit ces images quand tu push ton code ? Qui vérifie que les tests passent ? Qui pousse les images sur Docker Hub ? C'est le rôle du CI/CD — automatiser tout ça.

## C'est quoi CI/CD et pourquoi ça existe ?

**Le problème :** Sans CI/CD, chaque deployment est manuel. Quelqu'un lance les tests sur sa machine, quelqu'un d'autre fait le build, un troisième déploie en SSH. C'est lent, risqué, et source d'erreurs humaines. "J'ai oublié de lancer les tests avant de déployer" — boom, la prod est cassée.

C'est la différence entre cuire chaque pizza à la main et avoir un four automatique avec un tapis roulant.

**CI (Continuous Integration) :** À chaque push, on vérifie automatiquement que le code est propre (lint) et qu'il marche (tests). On n'attend pas la veille de la livraison pour découvrir que c'est cassé.

**CD (Continuous Delivery / Deployment) :**
- **Delivery** = le code est prêt à être déployé (bouton manuel)
- **Deployment** = le code est déployé automatiquement si tout est vert

**L'analogie :** Une chaîne de montage en usine. Tu pousses la matière première (le code) sur le tapis roulant. Station 1 = contrôle qualité (lint). Station 2 = dégustation (tests). Station 3 = emballage (build). Station 4 = livraison (deploy). Si un défaut est détecté à n'importe quelle station → la chaîne s'arrête. C'est le principe du "fail fast".

## Les 4 étapes classiques d'un pipeline

| Étape | Ce que ça fait | Analogie | Outils (pour nous) |
|-------|---------------|----------|-------------------|
| **Lint** | Vérifie le style et la qualité du code (erreurs de syntaxe, variables inutilisées, mauvaises pratiques) — comme un correcteur d'orthographe pour le code | Correcteur d'orthographe | Ruff (Python), Oxlint (JS) |
| **Test** | Vérifie que le code fait ce qu'il doit | Goûter le plat | Pytest |
| **Build** | Compile/package l'application | Emballer le plat | Docker build |
| **Deploy** | Met en production | Livrer au client | Docker push |

Ces étapes se lancent en séquence. Si le lint échoue → pas de tests. Si les tests échouent → pas de build. Fail fast.

## GitHub Actions — Les bases

GitHub Actions exécute des workflows (pipelines) définis dans des fichiers YAML dans `.github/workflows/`.

### Vocabulaire

| Terme | Ce que c'est |
|-------|-------------|
| **Workflow** | Le pipeline complet (le fichier YAML) |
| **Trigger** | Ce qui déclenche le workflow (`on: push`) |
| **Job** | Un groupe d'étapes qui s'exécutent sur une même machine |
| **Step** | Une action individuelle dans un job |
| **Runner** | La machine (un serveur distant) qui exécute le job. GitHub en fournit gratuitement — tu n'as rien à installer. |

### Structure d'un workflow

Un fichier YAML dans `.github/workflows/` décrit le pipeline. Voici un exemple minimal avec chaque ligne expliquée :

```yaml
# .github/workflows/ci.yml          ← le fichier doit être dans ce dossier exact
name: CI Pipeline                    # Le nom affiché dans l'onglet Actions de GitHub

on:                                  # "on" = QUAND est-ce que ce pipeline se déclenche ?
  push:                              #   → quand quelqu'un push du code
    branches: [main]                 #   → mais seulement sur la branche "main"
  pull_request:                      #   → OU quand une Pull Request est créée/mise à jour
    branches: [main]                 #   → ciblant la branche "main"

jobs:                                # La liste des jobs (groupes d'étapes) à exécuter
  lint:                              # Le nom du job (tu choisis le nom que tu veux)
    runs-on: ubuntu-latest           # Sur quelle machine exécuter ? → un serveur Ubuntu fourni par GitHub
    steps:                           # La liste des étapes de ce job

      - uses: actions/checkout@v4    # "uses" = utiliser une action pré-faite par quelqu'un d'autre
                                     # "actions/checkout" = une action officielle GitHub qui télécharge
                                     # ton code sur le runner (sinon le runner est vide, il n'a pas ton code)
                                     # "@v4" = la version 4 de cette action

      - name: Setup uv               # "name" = un nom lisible pour cette étape (affiché dans l'UI)
        uses: astral-sh/setup-uv@v4  # Installe uv sur le runner (comme tu l'as fait sur ta machine)

      - run: cd backend && uv run ruff check .
                                     # "run" = exécuter une commande bash directement
                                     # (contrairement à "uses" qui appelle une action pré-faite)
```

**En résumé — les 4 mots-clés à retenir :**

| Mot-clé | Ce que ça fait | Exemple |
|---------|---------------|---------|
| `on:` | Quand le pipeline se déclenche | `on: push` = à chaque push |
| `runs-on:` | Sur quelle machine | `ubuntu-latest` = un serveur Ubuntu gratuit de GitHub |
| `uses:` | Utiliser une action pré-faite | `actions/checkout@v4` = télécharger le code |
| `run:` | Exécuter une commande bash | `run: uv run pytest` = lancer les tests |

> **`uses` vs `run` :** `uses` appelle un "plugin" (une action prête à l'emploi écrite par quelqu'un d'autre — installer Python, se connecter à Docker Hub, etc.). `run` exécute une commande bash que TU écris. Si une action existe pour ce que tu veux faire, utilise `uses`. Sinon, `run`.

## Projet pratique : Pipeline CI/CD complet

### 1. Configurer le linting dans le projet

Le backend utilise **Ruff** (linter Python ultra-rapide) et le frontend utilise **Oxlint** (linter JS rapide).

Vérifie que les configs existent :

**`backend/pyproject.toml`** (déjà créé) :
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]
```

**`frontend/oxlintrc.json`** (déjà créé) :
```json
{
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off",
    "eqeqeq": "warn"
  }
}
```

Teste en local :
```bash
# Backend
cd ~/devops-project/backend
uv run ruff check .
# All checks passed!

# Frontend
cd ~/devops-project/frontend
bunx oxlint .
# Finished in xxxms
```

### 2. Vérifier les tests

```bash
cd ~/devops-project/backend
uv run pytest
# ===== 7 passed in 0.5s =====
```

### 3. Le pipeline GitHub Actions

Le projet fournit déjà le fichier `.github/workflows/ci.yml`. Avant de le lire, voici les syntaxes que tu vas rencontrer :

**Syntaxes à connaître pour lire le fichier :**

| Syntaxe | Ce que ça veut dire | Exemple |
|---------|-------------------|---------|
| `needs: lint` | "Ce job attend que le job `lint` soit terminé avant de commencer" — c'est comme ça qu'on crée l'ordre lint → test → build → push | Le job `test` attend `lint` |
| `run: |` | Le `|` après `run:` permet d'écrire **plusieurs lignes** de commandes (sinon `run:` n'accepte qu'une seule ligne) | `run: |` puis `cd backend` puis `uv run pytest` |
| `${{ ... }}` | Insérer une **variable** GitHub Actions. C'est comme `$VARIABLE` en bash mais avec la syntaxe `${{ }}` propre à GitHub Actions | `${{ github.sha }}` = le hash du commit |
| `${{ secrets.NOM }}` | Accéder à un **secret** stocké dans GitHub (Settings → Secrets). Le secret n'apparaît jamais dans les logs | `${{ secrets.DOCKERHUB_TOKEN }}` |
| `with:` | Passer des **paramètres** à une action `uses:`. C'est comme passer des arguments à une fonction | `with: username: ...` pour l'action de login Docker |
| `if:` | Exécuter ce job **seulement si** la condition est vraie. `==` veut dire "est égal à", `&&` veut dire "ET" | `if: github.ref == 'refs/heads/main'` = seulement sur la branche main |

Voici le fichier complet avec des commentaires :

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ─── JOB 1 : LINT (vérifier la qualité du code) ───
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # Télécharge le code du repo sur le runner

      - name: Setup uv
        uses: astral-sh/setup-uv@v4       # Installe uv (gestionnaire Python)

      - name: Lint backend (Ruff)
        run: |                             # | = plusieurs lignes de commandes
          cd backend
          uv run ruff check .

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2        # Installe Bun (runtime JS)

      - name: Lint frontend (Oxlint)
        run: |
          cd frontend
          bunx oxlint .

  # ─── JOB 2 : TEST (vérifier que le code marche) ───
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint                            # Attend que le job "lint" soit terminé
    steps:
      - uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v4

      - name: Run tests
        run: |
          cd backend
          uv run pytest

  # ─── JOB 3 : BUILD (construire les images Docker) ───
  build:
    name: Build Docker Images
    runs-on: ubuntu-latest
    needs: test                            # Attend que le job "test" soit terminé
    steps:
      - uses: actions/checkout@v4

      - name: Build backend image
        run: docker build -t devops-backend:${{ github.sha }} ./backend
        # ${{ github.sha }} = le hash unique du commit (ex: a1b2c3d)
        # On l'utilise comme tag de l'image pour savoir de quel commit elle vient

      - name: Build frontend image
        run: docker build -t devops-frontend:${{ github.sha }} ./frontend

  # ─── JOB 4 : PUSH (envoyer les images sur Docker Hub) ───
  push:
    name: Push to Docker Hub
    runs-on: ubuntu-latest
    needs: build                           # Attend que le job "build" soit terminé
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    # ↑ Ce job ne tourne QUE si :
    #   - on est sur la branche main (refs/heads/main)
    #   - ET c'est un push (pas une pull request)
    #   Pas besoin de pousser les images pour une PR — on veut juste vérifier que ça build
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3       # Action pré-faite pour se connecter à Docker Hub
        with:                              # "with" = les paramètres de l'action
          username: ${{ secrets.DOCKERHUB_USERNAME }}   # Ton username Docker Hub (stocké dans les secrets GitHub)
          password: ${{ secrets.DOCKERHUB_TOKEN }}      # Ton token Docker Hub (stocké dans les secrets GitHub)

      # Note : on rebuild les images ici même si le job "build" les a déjà construites.
      # Pourquoi ? Chaque job tourne sur un runner différent (une machine séparée).
      # Les images construites dans le job "build" n'existent plus ici.
      # Le job "build" servait à VÉRIFIER que le build passe. Ici, on build ET push.
      - name: Build and push backend
        run: |
          docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/devops-backend:latest ./backend
          docker push ${{ secrets.DOCKERHUB_USERNAME }}/devops-backend:latest
          # Format de l'image : username/nom-image:tag
          # "latest" = la version la plus récente

      - name: Build and push frontend
        run: |
          docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/devops-frontend:latest ./frontend
          docker push ${{ secrets.DOCKERHUB_USERNAME }}/devops-frontend:latest
```

### 4. Configurer les secrets

Sur GitHub → ton repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** :
- `DOCKERHUB_USERNAME` : ton nom d'utilisateur Docker Hub
- `DOCKERHUB_TOKEN` : un access token (pas ton mot de passe !) créé sur [hub.docker.com/settings/security](https://hub.docker.com/settings/security)

### 5. Push et regarde

Le fichier `ci.yml` est déjà dans le projet. Si tu as bien tout pushé, le pipeline tourne automatiquement.

```bash
cd ~/devops-project
git add .
git commit -m "ci: pipeline GitHub Actions"
git push
```

Va dans l'onglet **Actions** de ton repo GitHub. Tu verras le pipeline tourner : Lint → Test → Build → Push.

💡 **Si le push Docker Hub échoue :** vérifie que les secrets sont bien configurés. Le job `push` ne tourne que sur la branche `main` (pas sur les pull requests).

## Secrets et variables d'environnement

**Ne mets JAMAIS de mots de passe ou tokens dans le code.** Utilise les secrets GitHub.

```yaml
# Dans le workflow, accède à un secret :
${{ secrets.MON_SECRET }}

# Variables d'environnement (non sensibles) :
env:
  NODE_ENV: production
```

## Autres outils CI/CD

| Outil | Particularité |
|-------|--------------|
| **GitLab CI** | Très utilisé en France, intégré à GitLab |
| **Jenkins** | Le dinosaure — vieux mais encore partout |
| **CircleCI** | SaaS, simple à configurer |

## Coin entretien

**Q : C'est quoi CI/CD ?**
R : CI = vérifier automatiquement le code à chaque push (lint, tests). CD = déployer automatiquement si tout passe. Ça réduit les erreurs humaines et accélère les livraisons.

**Q : Quelles sont les étapes d'un pipeline CI/CD typique ?**
R : Lint (qualité du code) → Tests → Build (construction de l'artefact) → Deploy. Chaque étape bloque la suivante si elle échoue.

**Q : C'est quoi le "fail fast" ?**
R : Si une étape échoue, on arrête tout immédiatement. Pas besoin de builder si les tests ne passent pas. Ça fait gagner du temps et des ressources.

**Q : Où stocker les secrets dans un pipeline ?**
R : Dans les secrets du CI/CD (GitHub Secrets, GitLab Variables, etc.). Jamais dans le code, jamais dans les fichiers YAML committés.

**Q : Différence entre Continuous Delivery et Continuous Deployment ?**
R : Delivery = prêt à déployer mais bouton manuel. Deployment = deployment automatique. La plupart des entreprises font du Delivery.

**Q : C'est quoi un runner ?**
R : La machine (serveur) qui exécute les jobs du pipeline. GitHub fournit des runners gratuits (ubuntu-latest). On peut aussi utiliser ses propres runners.

**Q : C'est quoi un blue/green deployment ?**
R : Une stratégie de déploiement avec deux environnements identiques. Le "blue" sert la prod, on déploie la nouvelle version sur le "green", on teste, puis on bascule le traffic. Si ça casse, on rebascule en quelques secondes. Avantage : rollback instantané.

**Q : C'est quoi un canary deployment ?**
R : On déploie la nouvelle version sur un petit pourcentage de serveurs (ex: 5%). On surveille les métriques. Si tout va bien, on augmente progressivement (25% → 50% → 100%). Si ça casse, seul 5% des utilisateurs sont impactés.

## Bonnes pratiques

- **Le pipeline doit être rapide.** Si le CI met 20 min, les devs arrêtent de l'utiliser. Parallélise les jobs indépendants (lint backend ∥ lint frontend), utilise le cache (dépendances, images Docker).
- **Fail fast.** Mets les étapes les plus rapides en premier (lint < tests < build < deploy). Pas besoin de builder 5 min si le lint échoue en 10 secondes.
- **Jamais de secrets dans le code.** Utilise les secrets du CI (GitHub Secrets, GitLab Variables). Si un secret a été committé par erreur, change-le immédiatement — un `git rm` ne suffit pas (l'historique garde tout).
- **Un pipeline par branche, pas que main.** Lance le CI sur les Pull Requests aussi. L'objectif c'est de savoir si le code est cassé AVANT de merger.
- **Reproductibilité.** Épingle les versions de tes actions (`actions/checkout@v4`, pas `@latest`). Un pipeline qui casse tout seul parce qu'une dépendance a été mise à jour, c'est le cauchemar.
- **Pas de `git push --force` depuis le CI.** Le CI ne doit jamais modifier la branche source de façon destructive.

## Erreurs courantes

- **Oublier `actions/checkout@v4`** → Le runner n'a pas le code, tout échoue.
- **Secrets mal nommés** → `${{ secrets.DOCKER_HUB }}` ≠ `${{ secrets.DOCKERHUB_TOKEN }}`. Le nom doit correspondre exactement.
- **Tests qui passent en local mais pas en CI** → Souvent un problème de dépendances ou de variables d'environnement manquantes.
- **Pipeline trop long** → Parallélise les jobs indépendants (lint backend et lint frontend en parallèle).
- **Committer des secrets** → Si ça arrive, change-les IMMÉDIATEMENT. Git garde l'historique.

## Pour aller plus loin

- **Stratégies de deployment** : blue-green (deux environnements), canary (déploiement progressif) — au-delà du rolling update vu dans le cursus
- **Quality gates** : seuils de couverture de tests, analyse de sécurité automatique (SonarQube, Snyk) — de plus en plus demandé
- **ArgoCD** : GitOps — le repo Git EST la source de vérité pour le déploiement. Tu push du YAML, ArgoCD déploie automatiquement sur K8s (nécessite d'avoir vu le Module 9 — Kubernetes)

## Tu peux passer au module suivant si...

- [ ] Tu sais expliquer CI (vérification automatique) et CD (déploiement automatique)
- [ ] Tu connais les 4 étapes d'un pipeline (lint → test → build → deploy)
- [ ] Tu comprends le concept de "fail fast"
- [ ] Le pipeline GitHub Actions tourne sur ton repo (onglet Actions)
- [ ] Tu sais configurer des secrets dans GitHub (Settings → Secrets)
- [ ] Tu sais ce qu'est un runner
