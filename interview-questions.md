# Questions d'entretien DevOps

Ce fichier est en deux parties :
1. **Mises en situation** — des vrais problèmes qu'on te pose en entretien pour voir comment tu réfléchis
2. **Définitions rapides** — les classiques "c'est quoi X", pour ne pas sécher sur les bases

Les mises en situation sont plus importantes. Un recruteur veut voir comment tu **raisonnes**, pas si tu sais réciter une définition.

---

# Partie 1 : Mises en situation

## Scénario 1 — Déployer une app web en production

> **"Tu rejoins une startup. Ils ont une app web (frontend React + backend API + base PostgreSQL). Tout tourne sur le laptop du CTO. Comment tu mets ça en production ?"**

### Comment approcher la question

Ne plonge pas directement dans les outils. Pose des questions d'abord :
- Combien d'utilisateurs ? (10 ? 10 000 ? 1 million ?)
- Quel budget ?
- Quelle équipe ? (1 dev, 10 devs ?)
- Quels sont les besoins de disponibilité ? (site vitrine vs. application bancaire)

### Option A : Simple et rapide (petite startup, peu de trafic)

```
1 EC2 (t3.small) avec Docker Compose
├── Frontend (nginx + build React)
├── Backend (API container)
└── PostgreSQL (container avec volume)
```

**Avantages :** Rapide à mettre en place, pas cher (~15$/mois), une seule machine à gérer.
**Inconvénients :** Un seul serveur = single point of failure. Si l'EC2 tombe, tout tombe. La base de données dans Docker est risquée (données = volume, pas de backup automatique).

**Quand choisir :** MVP, side project, <100 utilisateurs, budget serré.

### Option B : Sérieuse (startup en croissance)

```
VPC
├── Subnet public
│   ├── EC2 (backend + frontend en Docker)
│   └── Load Balancer (optionnel, pour scaler plus tard)
└── Subnet privé
    └── RDS PostgreSQL (backups automatiques)
```

**Avantages :** La base est managée (backups, haute disponibilité). Séparation réseau (la DB n'est pas exposée à Internet). On peut ajouter un 2ème EC2 derrière un load balancer sans tout refaire.
**Inconvénients :** Plus cher (~50-100$/mois). Plus complexe à mettre en place.

**Quand choisir :** Application en prod avec de vrais utilisateurs, besoin de fiabilité.

### Option C : Scale (entreprise établie)

```
VPC
├── Subnet public
│   └── Application Load Balancer
├── Subnet privé
│   ├── ECS Fargate (containers managés, auto-scaling)
│   └── RDS PostgreSQL Multi-AZ
└── S3 (fichiers statiques, backups)
+ CloudFront (CDN pour le frontend)
+ Route 53 (DNS)
```

**Avantages :** Scaling automatique, haute disponibilité, zéro gestion de serveurs.
**Inconvénients :** Coûteux, complexe, over-engineering pour un petit projet.

**Quand choisir :** Beaucoup de trafic, SLA strict, équipe DevOps dédiée.

### Ce que le recruteur attend

Pas la réponse parfaite. Il veut voir que tu :
- Poses des questions avant de répondre (budget, scale, contraintes)
- Connais plusieurs options et sais les comparer
- Sais expliquer les trade-offs (simplicité vs. fiabilité vs. coût)
- Ne proposes pas Kubernetes pour 50 utilisateurs

---

## Scénario 2 — Le site est down en prod

> **"Il est 14h, tu reçois une alerte : le site ne répond plus. Les utilisateurs se plaignent. Qu'est-ce que tu fais ?"**

### La méthode (du plus large au plus précis)

**Étape 1 — Confirmer et délimiter le problème (30 secondes)**
```bash
# Le site répond ?
curl -I https://monsite.com
# Si timeout → problème réseau/DNS/serveur down
# Si 502 → le serveur proxy tourne mais l'app derrière est down
# Si 500 → l'app tourne mais crashe

# C'est juste moi ou tout le monde ?
# Tester depuis un autre réseau / un collègue
```

**Étape 2 — Vérifier l'infra (2 minutes)**
```bash
# Le serveur est up ?
ssh user@serveur
# Si "Connection refused" → le serveur est down ou le port SSH est bloqué
# → Vérifier sur la console AWS : instance running ? Security Group OK ?

# Les ressources sont OK ?
top              # CPU, RAM
df -h            # Disque plein ?
```

**Étape 3 — Vérifier les services (2 minutes)**
```bash
docker ps                        # Les containers tournent ?
docker logs backend --tail 100   # Erreurs récentes ?
systemctl status nginx           # Le reverse proxy tourne ?
```

**Étape 4 — Vérifier les dépendances**
```bash
# La base de données répond ?
docker exec -it db psql -U user -c "SELECT 1;"

# Les services externes répondent ?
curl https://api-externe-quon-utilise.com/health
```

**Étape 5 — Corriger et communiquer**
- Corriger le problème (redémarrer le service, libérer du disque, rollback du dernier déploiement...)
- **Communiquer** : prévenir l'équipe, mettre à jour le status page
- Après l'incident : écrire un post-mortem (qu'est-ce qui s'est passé, pourquoi, comment éviter que ça se reproduise)

### Les causes les plus fréquentes

| Symptôme | Cause probable | Fix rapide |
|----------|---------------|-----------|
| Timeout total | Serveur down ou Security Group | Redémarrer l'instance, vérifier les règles réseau |
| 502 Bad Gateway | L'app a crashé derrière le proxy | `docker restart backend`, vérifier les logs |
| 500 Internal Error | Bug dans le code ou DB inaccessible | Logs de l'app, vérifier la connexion DB |
| Site très lent | CPU/RAM saturé, requêtes DB lentes | `top`, vérifier les slow queries |
| Disque plein | Logs qui s'accumulent, images Docker | `df -h`, `docker system prune`, rotation des logs |

### Ce que le recruteur attend

- Une méthode structurée, pas du panique
- Tu commences par vérifier, pas par modifier
- Tu communiques avec l'équipe pendant le debugging
- Tu parles de post-mortem (apprentissage après l'incident)

---

## Scénario 3 — Mettre en place un pipeline CI/CD

> **"L'équipe de 5 devs déploie manuellement en SSH. Ça prend 30 min et ça casse une fois sur trois. Comment tu améliores ça ?"**

### Le problème concret

Aujourd'hui :
1. Un dev finit son code
2. Il se connecte en SSH au serveur
3. Il fait `git pull` sur le serveur
4. Il relance l'app manuellement
5. Il croise les doigts

Problèmes : aucun test avant déploiement, pas de rollback possible, un seul dev sait faire la manip, ça casse souvent.

### La solution progressive

**Phase 1 — CI (1-2 jours à mettre en place)**
```yaml
# À chaque push sur main :
Lint → Tests → Build image Docker → Push sur registry
```
- Les devs ont un feedback immédiat : "ton code casse les tests"
- On ne déploie jamais du code qui ne compile pas ou qui ne passe pas les tests
- **Impact :** on arrête de déployer du code cassé

**Phase 2 — CD vers un environnement de staging (3-5 jours)**
```yaml
# Après le CI :
Deploy automatique sur un serveur de staging
```
- Les devs et le product owner testent sur staging avant la prod
- Staging est une copie de la prod (même config, même infra)
- **Impact :** on teste dans des conditions réelles avant la prod

**Phase 3 — CD vers la prod (quand l'équipe est confiante)**
```yaml
# Si staging est OK (tests passent, QA validée) :
Approbation manuelle → Deploy en prod
```
- Un humain valide avant la prod (Continuous Delivery, pas Deployment)
- Rollback automatique si le health check échoue
- **Impact :** déploiement en 5 min au lieu de 30, aucune connexion SSH

### Pourquoi pas tout automatiser d'un coup ?

Parce que la confiance se construit progressivement. Si les tests ne couvrent pas assez de cas, un déploiement 100% automatique en prod va déployer des bugs plus vite. Phase 1 → Phase 2 → Phase 3 permet à l'équipe de gagner confiance à chaque étape.

### Ce que le recruteur attend

- Tu ne proposes pas "on met Kubernetes" d'emblée
- Tu penses progressif (quick wins d'abord)
- Tu parles de staging (jamais directement en prod)
- Tu mentionnes le rollback

---

## Scénario 4 — Gérer les secrets

> **"Un dev a committé un mot de passe de base de données dans le repo Git. Qu'est-ce que tu fais ?"**

### Réaction immédiate (urgence)

1. **Changer le mot de passe immédiatement** — la priorité absolue. Même si "personne ne l'a vu", on considère qu'il est compromis.
2. **Vérifier l'accès** — quelqu'un a-t-il utilisé ce mot de passe depuis le commit ?
3. **Supprimer du Git** — attention, un simple `git rm` ne suffit PAS. Le mot de passe reste dans l'historique. Il faut réécrire l'historique (`git filter-branch` ou `bfg`), mais c'est lourd. Le plus important reste le point 1 : changer le mot de passe.

### Mettre en place des protections

| Mesure | Ce que ça fait |
|--------|---------------|
| **`.gitignore`** | Ignorer les fichiers `.env`, `credentials.json`, etc. |
| **Pre-commit hook** | Scanner les commits AVANT qu'ils soient poussés (outils : `gitleaks`, `detect-secrets`) |
| **GitHub Secret Scanning** | GitHub détecte automatiquement les secrets committés et te prévient |
| **Variables d'environnement** | Les secrets vivent dans l'env du serveur, pas dans le code |
| **Secrets manager** | AWS Secrets Manager, HashiCorp Vault — stockage sécurisé et centralisé |

### La règle

Le code est **public par défaut** (même un repo privé peut fuiter). Les secrets ne doivent **jamais** être dans le code. Point.

---

## Scénario 5 — Choisir entre EC2, Lambda et containers managés

> **"On a 3 projets à héberger. Comment tu choisis l'infra pour chacun ?"**

### Projet A : API REST avec 1000 requêtes/jour

**Meilleur choix : Lambda + API Gateway**

Pourquoi : très peu de trafic, pas besoin d'un serveur qui tourne 24/7. Lambda = tu paies uniquement quand une requête arrive. Coût : quasi 0€ (Free Tier).

Si l'API est en Python/Node.js et que chaque requête dure <10 secondes, Lambda est parfait.

### Projet B : Application web avec base de données, 10 000 utilisateurs/jour

**Meilleur choix : EC2 (ou ECS Fargate) + RDS**

Pourquoi : trafic régulier, l'app doit tourner en permanence, connexion persistante à la DB. Lambda serait possible mais les cold starts + la gestion des connexions DB rendraient ça compliqué.

Avec Docker sur EC2, tu as le contrôle total. RDS pour la base = pas de gestion de backups. Si le trafic varie beaucoup → ECS Fargate avec auto-scaling.

### Projet C : Traitement de fichiers uploadés (redimensionner des images)

**Meilleur choix : Lambda + S3**

Pourquoi : événementiel. Un fichier arrive dans S3 → Lambda se déclenche → traite le fichier → remet le résultat dans S3. Pas besoin de serveur entre les uploads. Scaling automatique (100 uploads en même temps → 100 Lambdas en parallèle).

### Le tableau de décision

| Critère | Lambda | EC2 / ECS | ECS Fargate |
|---------|--------|-----------|-------------|
| Trafic | Sporadique, imprévisible | Constant | Variable |
| Durée d'exécution | < 15 min | Illimitée | Illimitée |
| État (stateful) | Non (stateless) | Oui | Oui |
| Connexion DB | Compliqué (pool de connexions) | Facile | Facile |
| Scaling | Automatique, instantané | Manuel ou Auto Scaling | Automatique |
| Coût à faible trafic | ~0€ | ~15-30$/mois | ~10-20$/mois |
| Coût à fort trafic | Peut devenir cher | Prévisible | Moyen |

### Ce que le recruteur attend

- Tu ne donnes pas la même réponse pour les 3 projets
- Tu justifies par des critères concrets (trafic, durée, coût, état)
- Tu connais les limites de chaque solution

---

## Scénario 6 — Infrastructure as Code : un collègue a modifié l'infra à la main

> **"Ton équipe utilise Terraform. Tu fais `terraform plan` et tu vois des changements que personne n'a fait dans le code. Que se passe-t-il et comment tu gères ?"**

### Ce qui s'est passé

Quelqu'un a modifié l'infra directement dans la console AWS (ajouté un Security Group rule, changé une instance type, etc.) sans passer par Terraform. Le state file de Terraform ne correspond plus à la réalité.

C'est ce qu'on appelle du **drift** (dérive).

### Comment résoudre

**Option A — Importer le changement dans Terraform (si le changement est voulu)**
```bash
# 1. Identifier ce qui a changé
terraform plan
# ~ aws_security_group.web will be updated in-place
#   - ingress rule for port 3306 (added manually)

# 2. Ajouter la règle dans le code Terraform pour qu'elle corresponde à la réalité
# 3. Re-plan → pas de changement → le code et la réalité sont synchronisés
terraform plan
# No changes.
```

**Option B — Forcer le retour au code (si le changement est une erreur)**
```bash
# terraform apply va remettre l'infra dans l'état décrit par le code
terraform apply
# Le changement manuel sera écrasé
```

### Prévenir le problème

- **Règle d'équipe :** on ne touche JAMAIS à la console pour modifier l'infra. Tout passe par le code + pull request.
- **IAM restrictif :** limiter les permissions de modification en console pour les environnements de prod.
- **Drift detection :** lancer `terraform plan` régulièrement (en CI) pour détecter les dérives.

---

## Scénario 7 — Monitoring et alerting

> **"Ton app tourne en prod depuis 3 mois. Le CTO te dit : 'On a des utilisateurs qui se plaignent que c'est lent mais on ne sait pas pourquoi.' Comment tu mets en place du monitoring ?"**

### Étape 1 — Définir ce qu'on veut mesurer

Les 4 signaux dorés (les "Golden Signals" de Google SRE) :

| Signal | Question | Exemple de métrique |
|--------|----------|-------------------|
| **Latency** | C'est rapide ? | Temps de réponse au 95e percentile |
| **Traffic** | Combien de monde ? | Requêtes par seconde |
| **Errors** | Ça marche ? | Taux d'erreurs 5xx |
| **Saturation** | C'est plein ? | CPU, RAM, disque, connexions DB |

### Étape 2 — Instrumenter l'app

```
App → expose /metrics → Prometheus scrape → Grafana affiche
```

- Ajouter la librairie Prometheus à l'app (pour notre projet : `prometheus-fastapi-instrumentator`)
- Déployer Prometheus + Grafana (docker-compose, c'est le plus simple)

### Étape 3 — Créer les dashboards

Un dashboard par "audience" :
- **Dashboard technique :** latence, erreurs, CPU, RAM, requêtes DB lentes
- **Dashboard business :** nombre d'utilisateurs actifs, nombre de tâches créées (pour le CTO)

### Étape 4 — Configurer les alertes

Bonnes alertes :
- "Le taux d'erreur 5xx dépasse 5% depuis 5 minutes" → **actionnable** (il y a un bug ou un service down)
- "Le temps de réponse p95 dépasse 2 secondes depuis 10 minutes" → **actionnable** (performance dégradée)

Mauvaises alertes :
- "CPU à 80%" → **pas actionnable seul** (80% de CPU c'est peut-être normal si l'app tourne bien)
- "1 erreur 404" → **bruit** (un utilisateur a tapé une mauvaise URL, c'est normal)

### Ce que le recruteur attend

- Tu connais les Golden Signals ou un framework similaire
- Tu distingues métriques techniques et business
- Tu sais qu'une alerte doit être actionnable
- Tu ne proposes pas de monitorer 200 métriques d'un coup

---

## Scénario 8 — Blue-green / Canary deployment

> **"Comment tu déploies en prod sans downtime et sans risquer de casser pour tous les utilisateurs ?"**

### Option A — Blue-Green

```
                    ┌─── Blue (v1.0 — actuelle) ◄── 100% du trafic
Load Balancer ──────┤
                    └─── Green (v1.1 — nouvelle) ◄── 0% du trafic
```

1. Tu déploies la v1.1 sur le Green (pendant que Blue sert toujours les users)
2. Tu testes Green (smoke tests, sanity check)
3. Tu bascules le load balancer : Green reçoit 100% du trafic
4. Si ça marche → tu supprimes Blue. Si ça casse → tu rebascules sur Blue en 10 secondes.

**Avantages :** Rollback instantané. Zéro downtime.
**Inconvénients :** Double infra pendant la transition (coût). Problème si la DB a changé de schéma entre v1.0 et v1.1.

### Option B — Canary

```
                    ┌─── v1.0 ◄── 95% du trafic
Load Balancer ──────┤
                    └─── v1.1 ◄── 5% du trafic (les "canaris")
```

1. Tu déploies la v1.1 sur quelques instances
2. Tu envoies 5% du trafic vers la v1.1
3. Tu surveilles les métriques (erreurs, latence)
4. Si tout va bien → 25% → 50% → 100%. Si ça casse → 0% et rollback.

**Avantages :** Tu détectes les bugs avec un impact limité (5% des utilisateurs).
**Inconvénients :** Plus complexe à mettre en place. Nécessite un bon monitoring pour détecter les problèmes.

### Option C — Rolling Update

C'est ce que fait Kubernetes par défaut. On remplace les instances une par une :

```
Début:    [v1.0] [v1.0] [v1.0] [v1.0]
Étape 1:  [v1.1] [v1.0] [v1.0] [v1.0]
Étape 2:  [v1.1] [v1.1] [v1.0] [v1.0]
Étape 3:  [v1.1] [v1.1] [v1.1] [v1.0]
Fin:      [v1.1] [v1.1] [v1.1] [v1.1]
```

**Avantages :** Simple, natif dans K8s, pas de double infra.
**Inconvénients :** Rollback plus lent. Pendant la transition, deux versions coexistent.

### Lequel choisir ?

| Stratégie | Complexité | Rollback | Cas d'usage |
|-----------|-----------|----------|-------------|
| **Blue-Green** | Moyenne | Instantané | Apps critiques, peu de déploiements |
| **Canary** | Élevée | Rapide | Apps à fort trafic, besoin de tester en conditions réelles |
| **Rolling** | Faible | Moyen | La plupart des cas, défaut K8s |

---

# Partie 2 : Définitions rapides

Pour chaque module, les questions "c'est quoi X" qu'on te posera aussi. Réponses courtes.

## Git

- **Git** — Système de versioning distribué. Historique du code, branches, collaboration.
- **Merge vs Rebase** — Merge préserve l'historique (commit de fusion). Rebase le réécrit (linéaire, plus propre, plus dangereux).
- **Pull vs Fetch** — Fetch télécharge sans appliquer. Pull = fetch + merge.

## Linux

- **Permissions (755)** — 3 blocs (owner/group/others). read=4, write=2, execute=1. 755 = rwxr-xr-x.
- **Processus** — Programme en cours d'exécution. `ps aux`, `kill PID`, `kill -9 PID`.
- **Pipe (`|`)** — Envoie la sortie d'une commande comme entrée de la suivante.

## Réseau

- **IP** — Identifiant d'une machine. Publique (Internet) ou privée (réseau local).
- **Port** — Numéro (1-65535) identifiant un service. 22=SSH, 80=HTTP, 443=HTTPS.
- **DNS** — Traduit noms de domaine en adresses IP.
- **TCP vs UDP** — TCP fiable (vérifie l'arrivée). UDP rapide (pas de vérification).
- **CIDR /24** — Sous-réseau de 256 adresses.
- **Code 502** — Bad Gateway. Le proxy ne joint pas l'app derrière.

## Docker

- **Image vs Container** — Image = template (recette). Container = instance en cours (plat cuisiné).
- **Dockerfile** — Fichier qui décrit comment construire une image. FROM, COPY, RUN, CMD.
- **Docker Compose** — Gère plusieurs containers ensemble via un YAML.
- **Volume** — Stockage persistant. Sans volume, les données disparaissent à la suppression du container.
- **Multi-stage build** — Plusieurs FROM dans un Dockerfile. Build dans une image lourde, copie du résultat dans une image légère.

## CI/CD

- **CI** — Vérification automatique à chaque push (lint, tests). CD — Déploiement automatique (ou semi-automatique).
- **Pipeline typique** — Lint → Tests → Build → Deploy. Fail fast.
- **Delivery vs Deployment** — Delivery = bouton manuel. Deployment = automatique.
- **Runner** — La machine qui exécute les jobs du pipeline.

## AWS

- **EC2** — Serveur virtuel. Tu choisis puissance + OS, tu paies à l'heure.
- **VPC** — Réseau privé isolé dans AWS. Subnets publics/privés, routage, firewall.
- **IAM** — Système de permissions. Users, roles, policies. Moindre privilège.
- **Security Group** — Firewall virtuel par port et IP source. Stateful.
- **S3** — Stockage d'objets illimité. Backups, fichiers statiques, logs.
- **RDS** — Base de données managée. Backups, mises à jour, haute disponibilité par AWS.
- **Lambda** — Serverless. Code exécuté à la demande, facturation à l'exécution.
- **Cold start** — Première exécution Lambda plus lente (démarrage de l'environnement).

## Terraform

- **IaC** — Infra décrite en code. Reproductible, versionné, auditable.
- **Plan / Apply / Destroy** — Prévisualiser / Exécuter / Supprimer.
- **State file** — Fichier JSON de l'état réel de l'infra. Ne jamais modifier à la main, ne jamais committer.
- **Terraform vs CloudFormation** — Terraform = multi-cloud. CloudFormation = AWS only.

## Ansible

- **Ansible** — Gestion de configuration. Configure des serveurs de manière automatisée, agentless (SSH).
- **Ansible vs Terraform** — Terraform crée l'infra. Ansible configure ce qui tourne dessus.
- **Idempotence** — Exécuter plusieurs fois = même résultat.

## Kubernetes

- **K8s** — Orchestrateur de containers. Déploiement, scaling, haute disponibilité sur un cluster.
- **Pod** — Unité de base. 1 pod ≈ 1 container.
- **Deployment** — Gère un groupe de pods. Maintient N replicas, rolling updates, self-healing.
- **Service** — Point d'accès réseau stable vers un groupe de pods.

## Monitoring

- **3 piliers** — Metrics (chiffres), Logs (texte), Traces (parcours des requêtes).
- **Prometheus** — Collecteur de métriques. Pull model, scrape /metrics.
- **Grafana** — Visualisation. Dashboards à partir de Prometheus et autres.
- **Bonne alerte** — Actionnable, basée sur les symptômes, pas trop fréquente.
