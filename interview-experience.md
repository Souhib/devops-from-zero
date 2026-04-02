# Préparer les questions d'expérience — Entretien DevOps

> En entretien, on te posera deux types de questions : les questions **techniques** ("c'est quoi un VPC ?") et les questions **d'expérience** ("raconte-moi un incident en prod que tu as géré"). Les premières sont dans [interview-questions.md](interview-questions.md). Ce fichier prépare les secondes.

## Pourquoi ce fichier existe

Un recruteur DevOps pose toujours des questions sur ton vécu : incidents, déploiements, choix techniques, problèmes résolus. Si tu sors d'une formation ou d'un cursus, tu n'as pas forcément de vraie expérience à raconter.

On va créer un **contexte fictif mais réaliste** — une entreprise, une infra, des problèmes, des solutions. C'est un support pour t'entraîner à répondre de manière structurée et crédible. **Ce n'est pas un script à réciter** — c'est une base que tu adaptes à ta propre histoire.

> **Si tu as ta propre expérience** (stage, alternance, projet perso, freelance), utilise-la. Le recruteur préfère une vraie histoire, même petite, qu'une histoire inventée parfaite. Ce fichier te sert de filet de sécurité si tu n'as rien à raconter, ou de modèle pour structurer tes réponses.

> **Tu n'es pas censé tout savoir.** En entretien, certains choix techniques étaient déjà en place quand tu es arrivé. Savoir dire "c'était comme ça quand je suis arrivé, et voilà ce que j'aurais fait différemment" est une réponse très mature. Le recruteur ne cherche pas quelqu'un qui a tout fait — il cherche quelqu'un qui comprend, qui réfléchit, et qui sait expliquer.

---

## Le contexte : QuickBite

**QuickBite** est une startup de livraison de repas (comme Uber Eats, mais plus petite). ~80 personnes, 12 développeurs, 2 DevOps (toi + un collègue senior).

### La stack technique

| Composant | Technologie |
|-----------|------------|
| Frontend | React (Vite) |
| Backend | Python (FastAPI) |
| Base de données | PostgreSQL |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS (EC2, RDS, ECS, S3) |
| IaC | Terraform |
| Monitoring | Prometheus + Grafana |

### L'état de l'infra quand tu arrives

Quand tu rejoins QuickBite, tout est fragile :

- **1 seul serveur EC2** fait tourner tout (backend + frontend + PostgreSQL) avec Docker Compose
- **Pas de CI/CD** — les devs déploient en SSH : `ssh serveur` → `git pull` → `docker compose up -d`
- **Pas de monitoring** — on sait que l'app est down quand un utilisateur se plaint sur Twitter
- **La base de données est dans un container Docker** — pas de backups automatiques, pas de RDS
- **Les secrets sont dans un fichier `.env` sur le serveur** — pas de gestion centralisée
- **Pas d'Infrastructure as Code** — tout a été créé à la main dans la console AWS

### Ce que tu as fait en 6 mois

| Mois | Ce que tu as fait | Pourquoi |
|------|------------------|----------|
| **Mois 1** | Mis en place GitHub Actions (lint → test → build → push Docker Hub) | Les devs déployaient du code non testé. Un bug en prod tous les 2 jours. |
| **Mois 2** | Migré PostgreSQL vers RDS + nettoyé la gestion des secrets (.env → GitHub Secrets) | La DB dans Docker = pas de backup. Un dev avait committé un token dans Git. |
| **Mois 3** | Géré un incident en prod (DB saturée pendant une promo) | Les connexions PostgreSQL étaient épuisées. 502 en cascade. 2h de downtime. |
| **Mois 4** | Ajouté Prometheus + Grafana | Après l'incident du mois 3, on ne pouvait plus se permettre de ne pas savoir ce qui se passe. |
| **Mois 4** | Résolu un problème de disque plein sur l'EC2 | Les images Docker s'accumulaient. Le serveur s'est figé à 3h du matin. |
| **Mois 5** | Tout passé en Terraform | L'infra était créée à la main. Impossible de la recréer ou de documenter ce qui existait. |
| **Mois 5** | Diagnostiqué et corrigé une fuite mémoire dans le backend | Le container backend crashait toutes les ~12h. RAM qui grimpait sans s'arrêter. |
| **Mois 6** | Migré le backend vers ECS Fargate | Un seul EC2 ne suffisait plus aux heures de pointe (midi et soir). Besoin d'auto-scaling. |

### Quickfix vs fix permanent — une réalité du métier

En DevOps, tu vas souvent devoir faire un choix : **est-ce que je corrige proprement maintenant (ça prend 2 jours) ou est-ce que je mets un pansement pour que la prod remarche (ça prend 10 minutes) ?**

La réponse : **le pansement d'abord, la correction propre ensuite.** Quand la production est down et que les utilisateurs ne peuvent pas payer, tu n'as pas 2 jours devant toi. Tu fais un quickfix pour remettre la prod debout, et tu programmes le vrai fix pour la semaine suivante.

Ce n'est pas du bricolage — c'est de la gestion de priorités. Le recruteur veut voir que tu sais faire les deux.

Voici des exemples concrets qu'on a vécus chez QuickBite :

| Incident | Quickfix (minutes) | Fix permanent (jours) |
|----------|-------------------|----------------------|
| DB saturée (100 connexions max) | Augmenter `max_connections` à 300 sur le RDS | Implémenter un **connection pool** dans le code (réutiliser les connexions au lieu d'en ouvrir une nouvelle à chaque requête) |
| Disque plein sur l'EC2 (images Docker) | `docker system prune -a` pour libérer l'espace immédiatement | Mettre en place un **cron job** qui nettoie les vieilles images tous les jours. Plus tard, migrer vers ECS (plus de gestion locale des images) |
| Fuite mémoire (container backend crash toutes les ~12h) | Ajouter un **restart automatique** du container toutes les 8h (`restart: always` dans Docker Compose + health check) | Profiler le code avec les devs, trouver la fuite (une liste qui grossissait sans jamais être vidée), corriger le code |

**La clé en entretien :** quand tu racontes un incident, mentionne les deux étapes. "D'abord j'ai fait X pour remettre la prod en état (quickfix), puis on a corrigé proprement en faisant Y (fix permanent)." Ça montre que tu sais gérer l'urgence ET que tu ne laisses pas le pansement devenir la solution définitive.

---

## Comment utiliser ces questions

**Le principe :** Pour cet exercice, tu ES le DevOps de QuickBite. Tu y as travaillé pendant 6 mois. Tu as vécu tout ce qui est décrit dans la timeline ci-dessus — les incidents, les migrations, les galères. Quand le recruteur te pose une question, tu réponds en parlant de TON expérience chez QuickBite, comme si tu y avais vraiment été.

Relis bien le contexte et la timeline avant de commencer. Plus tu les connais par coeur, plus tes réponses seront naturelles.

**Pour chaque question, suis cet ordre :**

1. **Lis la question** et réponds comme si tu étais en entretien — à voix haute c'est le mieux. Tu es le DevOps de QuickBite, tu racontes ce que tu as vécu là-bas. Ne regarde pas les indices tout de suite.
2. **Ouvre les indices** — ils te donnent des pistes sur les points à mentionner. Compare avec ta réponse et reformule si tu avais oublié des choses.
3. **Ouvre la réponse modèle** — compare avec la tienne. Ta réponse est différente ? C'est normal. L'important c'est la structure (contexte → problème → action → résultat), pas les mots exacts.
4. **Ouvre "Ce que le recruteur veut entendre"** — ça te montre ce que le recruteur évalue vraiment. Vérifie que ta réponse couvre ces points.

---

## Les questions

### 1. "Quel est le plus gros problème en production que vous ayez résolu ?"

> Réfléchis : dans la timeline QuickBite, c'est le **Mois 3**. Qu'est-ce qui s'est passé ? Comment tu aurais réagi ?

<details>
<summary>💡 Indices</summary>

- Pense à l'incident du Mois 3 : la promo marketing non communiquée
- Quels symptômes tu as vu ? (codes HTTP, comportement de l'app)
- Comment tu as identifié la cause ? (logs, requêtes sur la DB)
- Qu'est-ce que tu as fait en urgence ? (augmenter les connexions)
- Qu'est-ce que tu as fait après pour que ça ne se reproduise pas ? (fix du code, monitoring)

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Le plus gros incident que j'ai géré, c'était chez QuickBite — une saturation de la base de données pendant une promo marketing. Le traffic a été multiplié par 5 en 30 minutes. Le pool de connexions PostgreSQL était à 100 par défaut, et notre code ne fermait pas les connexions proprement. En 20 minutes, les 100 connexions étaient prises, le backend renvoyait des 502 en cascade.

**Comment j'ai réagi :**
1. D'abord j'ai identifié le problème — les logs montraient `too many connections`. J'ai confirmé avec `SELECT count(*) FROM pg_stat_activity` sur la DB.
2. **Quickfix :** J'ai augmenté le `max_connections` à 300 en urgence sur le RDS et redémarré le backend → la prod remarchait.
3. **Fix permanent :** J'ai remonté le diagnostic aux devs. Ils ont corrigé le code pour utiliser un **connection pool** (réutiliser les connexions au lieu d'en ouvrir une nouvelle à chaque requête). C'est du code applicatif, pas de l'infra — mon rôle c'était de diagnostiquer et de fournir les données.
4. J'ai ajouté une alerte Prometheus sur le nombre de connexions actives pour ne plus être surpris.

**Ce que j'en ai tiré :** C'est cet incident qui m'a poussé à mettre en place le monitoring (Prometheus + Grafana). Avant, on volait à l'aveugle."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu as une **méthode** (pas de panique, tu diagnostiques avant d'agir)
- Tu expliques la **cause racine** (pas juste "j'ai redémarré")
- Tu as mis en place des **mesures pour que ça ne se reproduise pas** (monitoring, alertes, fix du code)
- Tu es capable de **communiquer** pendant l'incident (informer l'équipe, le support)

**Follow-ups possibles :**
- "Combien de temps l'incident a duré ?" → ~2h entre les premiers 502 et le retour à la normale
- "Vous avez fait un post-mortem ?" → Oui, on a documenté : cause, timeline, actions prises, mesures préventives
- "C'était votre faute ?" → Non, c'est un concours de circonstances (promo non communiquée + config par défaut + pas de monitoring). L'important c'est le fix, pas le blâme.

</details>

---

### 2. "Avez-vous déjà eu des problèmes de performance ?"

> Réfléchis : après le Mois 4 (monitoring), on découvre des endpoints lents. Comment tu diagnostiquerais ? Quelles solutions progressives tu proposerais ?

<details>
<summary>💡 Indices</summary>

- Le monitoring (Grafana) a révélé un endpoint à 2.5 secondes
- Côté DevOps, tu as activé les slow query logs sur PostgreSQL pour diagnostiquer
- Les corrections (index, cache, requêtes) c'est le boulot des devs backend — toi tu diagnostiques, tu remontes le problème, et tu fournis les métriques
- Mentionne la collaboration avec les devs — c'est ton rôle de leur donner les données pour qu'ils corrigent

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Oui, on avait un endpoint qui mettait 2.5 secondes à répondre. C'est grâce au monitoring que j'ai mis en place qu'on l'a vu — le graphique Grafana montrait clairement un pic de latence sur `/api/orders`.

**Mon rôle (DevOps) — le diagnostic :**
- J'ai activé les **slow query logs** sur PostgreSQL (les requêtes qui prennent plus de 500ms)
- J'ai identifié la requête problématique et remonté le problème aux devs avec les données : "cette requête prend 2.5s, elle fait un SELECT * avec 3 JOINs sur des tables de 500k lignes, sans index"
- J'ai ajouté un dashboard Grafana dédié aux temps de réponse par endpoint pour suivre l'évolution

**Le rôle des devs backend — la correction :**
1. Ajout d'index sur les colonnes utilisées → 2.5s à 200ms
2. Mise en place d'un cache Redis pour les requêtes fréquentes
3. Revue des requêtes SQL pour ne plus faire de `SELECT *`

**Mon rôle après le fix :** Vérifier sur Grafana que le p95 est redescendu (de 2.5s à 150ms), et ajouter une alerte si un endpoint dépasse 1 seconde.

Le DevOps diagnostique et fournit les données — les devs corrigent le code. C'est du travail d'équipe."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu sais **diagnostiquer** avec les outils DevOps (monitoring, slow query logs, métriques)
- Tu fais la **distinction entre ton rôle et celui des devs** — tu ne corriges pas le code, tu fournis les données pour qu'ils le fassent
- Tu sais **communiquer un problème** de manière claire et actionnable ("cette requête, cette table, ce temps")
- Tu **vérifies** que le fix a marché (monitoring après correction)

</details>

---

### 3. "Avez-vous déjà géré une mise en production ? Sur quel outil ?"

> Réfléchis : compare l'état à ton arrivée (SSH + git pull) et ce que tu as mis en place au **Mois 1**. Décris le avant/après.

<details>
<summary>💡 Indices</summary>

- Décris d'abord comment c'était AVANT (manuel, risqué, pas de tests)
- Puis ce que tu as mis en place (GitHub Actions, 4 étapes du pipeline)
- Mentionne le résultat concret (combien de déploiements par jour, confiance de l'équipe)
- Si on te demande "pourquoi GitHub Actions ?", la réponse est simple : le code était sur GitHub

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Quand je suis arrivé, le déploiement était manuel — SSH sur le serveur, `git pull`, `docker compose up`. Ça cassait souvent et personne n'osait déployer le vendredi.

J'ai mis en place un pipeline GitHub Actions en 4 étapes :
1. **Lint** (Ruff + Oxlint) — vérifie la qualité du code
2. **Tests** (Pytest) — vérifie que rien n'est cassé
3. **Build** — construit les images Docker et les tag avec le hash du commit
4. **Push** — envoie les images sur Docker Hub, uniquement sur la branche main

Le déploiement sur le serveur se faisait ensuite via un script qui pull la nouvelle image et relance les containers. Plus tard, quand on est passé sur ECS, le déploiement était géré directement par AWS (on push l'image, ECS la déploie automatiquement).

**Résultat :** On est passé de 'on déploie quand on ose' à 3-4 déploiements par jour, en confiance."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu connais les **étapes d'un pipeline** (lint → test → build → deploy)
- Tu sais expliquer le **avant/après** (l'amélioration concrète)
- Tu comprends pourquoi chaque étape existe (fail fast)

**Follow-ups possibles :**
- "Pourquoi GitHub Actions et pas GitLab CI ?" → Le code était sur GitHub, pas de raison de migrer. GitLab CI est très bien aussi, c'est juste un choix d'écosystème.
- "Combien de temps prenait le pipeline ?" → ~4 minutes (lint 30s, tests 1min, build 2min, push 30s)

</details>

---

### 4. "Comment faites-vous si la mise en production se passe mal ?"

> Réfléchis : un vendredi, un déploiement casse le paiement. Comment tu réagis ? C'est quoi ton plan de rollback ?

<details>
<summary>💡 Indices</summary>

- Comment tu détectes le problème ? (monitoring, alertes Grafana)
- Comment tu fais un rollback ? (images Docker taggées par commit)
- Combien de temps ça prend ? (quelques minutes si bien préparé)
- Qu'est-ce que tu fais APRÈS ? (identifier le bug, ajouter un test, post-mortem)
- Mentionne la stratégie de déploiement (rolling update, health checks)

</details>

<details>
<summary>✅ Réponse modèle</summary>

"On a eu ce cas — un déploiement un vendredi qui a cassé le paiement. L'alerte Grafana a détecté un pic de 500 sur l'endpoint `/api/checkout` en 2 minutes.

**Le rollback :**
1. On a immédiatement re-déployé l'image Docker **précédente** (c'est pour ça qu'on tag les images avec le hash du commit — on peut revenir à n'importe quelle version)
2. Sur ECS, ça prend ~30 secondes : on change le tag de l'image dans la task definition et ECS redéploie
3. Temps total de downtime : ~5 minutes

**Ensuite :**
- On a identifié le bug dans la PR
- On a ajouté un test qui couvre ce cas précis
- On a ajouté une règle : pas de déploiement le vendredi après 16h (culture, pas technique)

**En général, notre stratégie de rollback :**
- Chaque image Docker est taggée avec le hash du commit → on peut revenir à n'importe quelle version
- Le monitoring détecte les problèmes en quelques minutes (taux d'erreurs 5xx)
- On fait du **rolling update** sur ECS → si le nouveau container ne passe pas le health check, ECS garde l'ancien"

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu as un **plan de rollback** (pas "on prie")
- Tu réagis **vite** (monitoring + alertes)
- Tu apprends de tes erreurs (ajout de tests, règles d'équipe)
- Tu connais les **stratégies de déploiement** (rolling update, blue-green, canary)

</details>

---

### 5. "Quel type de déploiement aviez-vous mis en place et pourquoi ?"

> Réfléchis : au **Mois 6**, on migre vers ECS. Quel type de déploiement on choisit ? Pourquoi pas les autres ?

<details>
<summary>💡 Indices</summary>

- Il y a 3 stratégies principales : rolling update, blue-green, canary
- Pense au contexte QuickBite : petite équipe (2 DevOps), budget limité
- Le recruteur veut que tu connaisses les 3 ET que tu justifies ton choix
- Dis aussi ce que tu ferais avec plus de moyens

</details>

<details>
<summary>✅ Réponse modèle</summary>

"On utilisait un **rolling update** sur ECS Fargate. Ça veut dire que quand on déploie une nouvelle version, ECS remplace les containers un par un — il lance un nouveau container avec la nouvelle image, vérifie qu'il répond au health check, puis supprime l'ancien. Pendant la transition, les deux versions coexistent.

**Pourquoi rolling update et pas autre chose :**
- **Pas blue-green** : ça demande le double d'infra (deux environnements complets). Pour notre taille et notre budget, c'était over-kill.
- **Pas canary** : ça demande un système de routage du traffic (envoyer 5% sur la v2, 95% sur la v1). On n'avait pas l'outillage et c'était complexe pour une équipe de 2 DevOps.
- **Rolling update** : natif dans ECS, pas de coût supplémentaire, rollback automatique si le health check échoue. C'est le bon compromis pour notre taille.

Si on avait eu plus de traffic et une équipe DevOps plus grande, j'aurais exploré le canary deployment pour tester les nouvelles versions sur un petit pourcentage d'utilisateurs avant de déployer à tout le monde."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu connais **plusieurs stratégies** (rolling, blue-green, canary)
- Tu sais **justifier un choix** en fonction du contexte (budget, taille de l'équipe, complexité)
- Tu ne proposes pas la solution la plus complexe juste pour impressionner
- Tu sais ce que tu ferais avec **plus de moyens**

</details>

---

### 6. "Qu'est-ce que vous auriez fait différemment ?"

> Réfléchis : regarde la timeline. Certaines choses auraient dû être faites plus tôt. Lesquelles ? Pourquoi on ne l'a pas fait ? (contexte startup, on va vite)

<details>
<summary>💡 Indices</summary>

- Le monitoring est arrivé au Mois 4 — c'était trop tard (après l'incident)
- La DB dans Docker — risque de perte de données
- L'infra créée à la main avant Terraform — pénible à importer après
- Ce ne sont pas des "erreurs" — ce sont des compromis de startup. Explique-le.

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Avec le recul, 3 choses :

1. **Le monitoring dès le jour 1.** On l'a ajouté au mois 4, après un incident. Si on l'avait eu dès le début, on aurait vu les problèmes de performance avant qu'ils ne deviennent des incidents. C'est un investissement de 2-3 jours qui économise des semaines de debugging.

2. **RDS tout de suite au lieu de PostgreSQL dans Docker.** La DB dans un container sans backup, c'est une bombe à retardement. On a eu de la chance de ne pas perdre de données avant la migration. En production, la base de données doit être managée (RDS, Cloud SQL, etc.).

3. **Terraform avant de créer les ressources à la main.** On a d'abord tout créé dans la console AWS, puis on a dû tout importer dans Terraform au mois 5. C'était pénible. Si c'était à refaire, je partirais de Terraform dès le premier EC2.

Ces trois choix étaient des choix de 'on fait vite pour livrer', ce qui se comprend dans une startup. Mais le temps perdu à rattraper est toujours supérieur au temps investi à bien faire dès le début."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu as du **recul** sur tes propres décisions
- Tu sais faire la différence entre "dette technique acceptable" et "erreur évitable"
- Tu ne blâmes pas les autres ("c'était comme ça quand je suis arrivé" → OK, mais qu'est-ce que TU aurais fait ?)
- Tu proposes des **améliorations concrètes**, pas juste "tout refaire from scratch"

</details>

---

### 7. "Comment vous gérez les secrets ?"

> Réfléchis : au **Mois 2**, un dev committe un `.env` avec les clés Stripe. Qu'est-ce que tu fais en urgence ? Qu'est-ce que tu mets en place pour que ça ne se reproduise pas ?

<details>
<summary>💡 Indices</summary>

- La réaction immédiate : changer les secrets compromis (pas juste supprimer le commit — l'historique Git garde tout)
- Les mesures préventives : .gitignore, pre-commit hooks (gitleaks), GitHub Secrets
- Où stocker les secrets en production : variables d'environnement, pas dans des fichiers
- La rotation régulière des secrets

</details>

<details>
<summary>✅ Réponse modèle</summary>

"On a eu un incident où un dev a committé un `.env` avec les clés API Stripe dans un repo public. Ça nous a forcés à changer tous les secrets en urgence.

**Ce qu'on a mis en place après :**
1. **`.gitignore` vérifié** — `.env` est dans le `.gitignore` de tous les repos
2. **Pre-commit hook** avec `gitleaks` — scanne les commits AVANT qu'ils soient poussés, bloque si un secret est détecté
3. **GitHub Secrets** pour le CI/CD — les secrets ne sont jamais dans le code, ils sont injectés par le pipeline
4. **Variables d'environnement sur le serveur** — les secrets sont dans la config ECS (task definition), pas dans des fichiers
5. **Rotation régulière** — on change les mots de passe DB et les tokens API tous les 3 mois

La règle : un secret ne doit **jamais** apparaître dans le code ou dans Git. Même dans un repo privé — un repo privé peut devenir public, un employé peut partir, etc."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu as une **politique de gestion des secrets** (pas juste "on fait attention")
- Tu connais les **outils** (gitleaks, GitHub Secrets, Vault)
- Tu sais réagir à un **incident de sécurité** (changer les secrets en urgence, pas juste supprimer le commit)
- Tu prends des **mesures préventives** (pre-commit hooks, rotation)

</details>

---

### 8. "Décrivez votre journée type en tant que DevOps"

> Réfléchis : avec tout ce que tu sais de QuickBite (monitoring, CI/CD, aide aux devs, incidents), comment se passe une journée ?

<details>
<summary>💡 Indices</summary>

- Le matin : tu vérifies quoi en premier ? (dashboards, alertes)
- En journée : quels types de tâches ? (PRs, aide devs, amélioration infra, automatisation)
- Quand ça va mal : quelle est ta méthode ? (diagnostiquer, corriger, communiquer, post-mortem)
- Quel ratio réactif (incidents, aide) vs proactif (amélioration, automatisation) ?

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Ma journée type chez QuickBite :

**Le matin (30 min) :**
- Checker les **dashboards Grafana** — est-ce que tout tourne bien ? Des erreurs cette nuit ?
- Regarder les **alertes** reçues pendant la nuit (Slack + email) — trier entre le bruit et les vrais problèmes
- Lire les **Pull Requests** en attente — surtout celles qui touchent le Dockerfile, le docker-compose, le pipeline CI/CD ou la config Terraform

**En journée :**
- **Aider les devs** — "mon container crash", "le pipeline échoue", "comment je configure cette variable d'env en staging ?"
- **Améliorer l'infra** — optimiser le pipeline CI (le build était trop lent → ajout de cache Docker), ajouter une alerte manquante, mettre à jour une version
- **Écrire du code d'infra** — Terraform pour un nouveau service, modifier le docker-compose, écrire un nouveau workflow GitHub Actions
- **Automatiser** — tout ce qui est fait à la main plus de 2 fois doit être scripté

**Quand ça va mal (incident) :**
- Diagnostiquer : logs, métriques, traces
- Corriger en urgence (rollback, restart, scale up)
- Communiquer avec l'équipe (Slack, status page)
- Écrire un **post-mortem** après l'incident

Je dirais que c'est 40% réactif (aider les devs, incidents) et 60% proactif (améliorer l'infra, automatiser, anticiper)."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu as une **routine** (monitoring le matin, pas de surprise)
- Tu sais **prioriser** (incidents > aide aux devs > amélioration continue)
- Tu es **proactif** (tu n'attends pas que ça casse)
- Tu es un **facilitateur** pour les devs (tu les débloques, tu ne les bloques pas)
- Tu automatises (la philosophie DevOps)

</details>

---

### 9. "Avez-vous déjà dû mettre un fix temporaire en production ?"

> Réfléchis : dans la timeline, on a eu le disque plein et la fuite mémoire. Dans les deux cas, on a d'abord mis un pansement. Lequel ? Et ensuite, c'était quoi la vraie solution ?

<details>
<summary>💡 Indices</summary>

- Disque plein : qu'est-ce qu'on fait en urgence pour libérer de l'espace ? Et après, comment on empêche que ça se reproduise ?
- Fuite mémoire : le container crash toutes les 12h. Comment tu gardes la prod en vie en attendant de trouver le bug ? Et ensuite, comment tu trouves la fuite ?
- Le recruteur veut voir que tu fais la différence entre "éteindre l'incendie" et "installer un détecteur de fumée"

</details>

<details>
<summary>✅ Réponse modèle</summary>

"Oui, plusieurs fois. Le plus marquant c'est la fuite mémoire qu'on a eue sur le backend. Le container crashait toutes les 12 heures environ — la RAM montait progressivement jusqu'à atteindre la limite, et le container était tué par Docker (OOM kill, code de sortie 137).

**Le quickfix (10 minutes) :**
On a configuré Docker pour redémarrer le container automatiquement (`restart: always`), et ajouté un health check qui vérifie que l'API répond. Comme la mémoire mettait ~12h à saturer, un restart toutes les 8h suffisait à garder la prod stable. C'est moche, mais les utilisateurs ne voyaient plus de coupure.

**Le fix permanent (3 jours) :**
Avec un dev, on a profilé l'application. On a trouvé qu'une liste en mémoire stockait l'historique des requêtes pour du debug — elle grossissait à chaque requête et n'était jamais vidée. Le dev a corrigé le code (limiter la liste aux 1000 dernières entrées), et la consommation mémoire est devenue stable.

**L'autre cas : le disque plein.** À 3h du matin, alerte : le serveur EC2 ne répond plus. Le disque était plein — les images Docker s'accumulaient après chaque déploiement (on avait une nouvelle image à chaque commit, jamais nettoyée).

Quickfix : `docker system prune -a` en SSH → 8 Go libérés → le serveur repart.
Fix permanent : un cron job qui exécute `docker system prune` tous les jours à 4h du matin. Et au mois 6, la migration vers ECS a supprimé le problème complètement (plus de gestion locale des images).

**Ce que j'en retiens :** Un quickfix n'est pas une honte — c'est une nécessité quand la prod est down. Mais il faut TOUJOURS planifier le fix permanent dans la foulée. Le danger, c'est quand le quickfix devient la solution définitive et que tout le monde oublie qu'il y a un vrai problème en dessous."

</details>

<details>
<summary>Ce que le recruteur veut entendre</summary>

- Tu sais faire la différence entre **urgence** (remettre la prod debout) et **correction** (résoudre la cause racine)
- Tu ne méprises pas les quickfixes — tu comprends qu'ils sont nécessaires
- Tu ne t'arrêtes pas au quickfix — tu planifies toujours le vrai fix
- Tu sais **diagnostiquer** (profiling mémoire, vérification disque) et pas juste "redémarrer et prier"
- Tu connais les signaux d'alerte (code 137 = OOM, disque à 100%)

**Follow-ups possibles :**
- "Le quickfix a duré combien de temps avant le vrai fix ?" → La fuite mémoire : 1 semaine (le temps de profiler et corriger). Le disque : le cron a tenu 2 mois jusqu'à la migration ECS.
- "Comment vous savez que le vrai fix a marché ?" → Le monitoring (Grafana) : on surveille la courbe mémoire après le fix. Si elle est stable → c'est corrigé.

</details>

---

## Récap — Quelle question montre quoi

| Question | Ce que le recruteur évalue |
|----------|--------------------------|
| Plus gros problème en prod | Ta méthode de diagnostic + gestion de crise |
| Problèmes de performance | Ta capacité à mesurer, diagnostiquer, et résoudre |
| Mise en production | Ta connaissance du CI/CD concret |
| Si ça se passe mal | Ton plan de rollback + ta réactivité |
| Type de déploiement | Tes choix techniques justifiés par le contexte |
| Ce que tu aurais fait différemment | Ton recul + ta maturité |
| Gestion des secrets | Ta rigueur sécurité |
| Journée type | Ta vision du métier au quotidien |
| Fix temporaire en prod | Ta gestion de l'urgence + quickfix vs fix permanent |

---

## Derniers conseils

- **Structure tes réponses** : Contexte → Problème → Ce que tu as fait → Résultat. C'est la méthode STAR (Situation, Task, Action, Result).
- **Sois concret** : "J'ai ajouté un index sur la colonne `order_id`" est mieux que "J'ai optimisé la base de données".
- **Admets ce que tu ne sais pas** : "Je n'ai pas eu l'occasion d'utiliser Kubernetes en prod, mais j'ai pratiqué avec minikube et je comprends les concepts" → c'est une bonne réponse.
- **Adapte le contexte** : Si tu as une vraie expérience (même un projet perso), utilise-la. Le recruteur sentira que c'est authentique.
- **N'invente pas** : Si le recruteur creuse et que tu ne sais pas, dis-le. "Je ne sais pas, mais voilà comment je chercherais la réponse" est toujours mieux que d'inventer.
