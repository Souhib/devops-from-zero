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
- Quel budget ? (0€ ? 50€/mois ? 1000€/mois ?)
- Quelle équipe ? (1 dev, 10 devs ? Y a-t-il un DevOps ?)
- Quels sont les besoins de disponibilité ? (side project vs. app bancaire)
- Le frontend est-il statique (juste du HTML/JS buildé) ou a-t-il besoin de server-side rendering ?

Cette dernière question est clé, parce qu'elle change complètement l'architecture pour le frontend.

### Le frontend — 3 approches différentes

**Notre cas : React avec Vite = frontend statique.** Le build produit des static files (HTML/CSS/JS) qu'on peut servir depuis n'importe quel serveur web ou CDN.

**Approche 1 — CDN / Hébergement statique (le plus simple et le plus performant)**

Le frontend buildé est juste des static files. Pas besoin d'un serveur pour ça.

| Service | Ce que c'est | Coût | Complexité |
|---------|-------------|------|-----------|
| **S3 + CloudFront** | Bucket S3 (stockage) + CDN AWS (distribution mondiale) | ~0-5$/mois | Faible |
| **Vercel** | Hébergement spécialisé frontend, deployment auto depuis Git | Gratuit (hobby) | Très faible |
| **Netlify** | Même concept que Vercel | Gratuit (hobby) | Très faible |
| **AWS Amplify Hosting** | Service AWS pour héberger des apps frontend, deployment auto depuis Git | Gratuit (Free Tier) | Faible |

**Quand choisir :** Quasi toujours pour un frontend statique (React, Vue, Angular buildé). C'est plus rapide (CDN = serveurs proches des utilisateurs), moins cher, et tu n'as aucun serveur à gérer.

**Approche 2 — Nginx dans un container** (ce qu'on fait dans le projet fil rouge)

On build le frontend, puis on sert les fichiers avec nginx dans un container Docker. C'est ce qu'on fait dans le Module 3.

**Quand choisir :** Quand tu veux tout avoir dans le même docker-compose pour simplifier le deployment, ou quand tu as besoin d'un reverse proxy custom (règles de routage complexes).

**Approche 3 — Server-Side Rendering (Next.js, Nuxt, etc.)**

Si le frontend fait du SSR (le HTML est généré côté serveur), alors il a besoin d'un serveur Node.js qui tourne en permanence. Dans ce cas, on le traite comme un backend (EC2, ECS, App Runner, etc.).

**Quand choisir :** SEO critique (e-commerce, blog), contenu dynamique qui change souvent.

### Le backend + base de données — Du plus simple au plus robuste

**Option A : 1 serveur, Docker Compose (MVP / side project)**

```
1 EC2 (t3.small)
├── Frontend (nginx)
├── Backend (API container)
└── PostgreSQL (container avec volume)
```

**Avantages :** Rapide à mettre en place, pas cher (~15$/mois), une seule machine.
**Inconvénients :** Single point of failure. DB dans Docker = risqué (pas de backup automatique). Scaling impossible.
**Quand choisir :** MVP, side project, <100 utilisateurs, budget ~0€.

**Option B : EC2 + RDS (startup sérieuse)**

```
VPC
├── Subnet public
│   └── EC2 (backend en Docker)
└── Subnet privé
    └── RDS PostgreSQL (backups automatiques)
+ S3 + CloudFront (frontend statique)
```

**Avantages :** La DB est managée (backups, updates auto). Séparation réseau. Le frontend sur CDN est rapide et gratuit. On peut ajouter un 2ème EC2 + load balancer plus tard.
**Inconvénients :** Plus cher (~50-100$/mois). Tu gères les EC2 toi-même (updates OS, Docker, etc.).
**Quand choisir :** App en prod, vrais utilisateurs, besoin de fiabilité, équipe petite.

**Option C : ECS Fargate (scaling sans gérer de serveurs)**

```
VPC
├── Subnet public
│   └── Application Load Balancer
├── Subnet privé
│   ├── ECS Fargate (containers backend, auto-scaling)
│   └── RDS PostgreSQL Multi-AZ
+ S3 + CloudFront (frontend)
+ Route 53 (DNS)
```

ECS (Elastic Container Service) fait tourner tes containers Docker sans que tu gères de serveurs. Fargate = tu lui donnes une image Docker, tu définis CPU/RAM, il lance le container quelque part dans le cloud. Tu ne vois jamais de machine.

**Avantages :** Auto-scaling, pas de serveurs à gérer, high availability. Tu pousses une image Docker et c'est déployé.
**Inconvénients :** Plus cher que EC2 brut (~100-300$/mois). Configuration plus complexe (task definitions, services, target groups...).
**Quand choisir :** Traffic variable, besoin de scaling, pas envie de gérer des EC2.

**Option D : AWS App Runner (le plus simple pour des containers)**

```
App Runner (backend container)
+ RDS PostgreSQL
+ S3 + CloudFront (frontend)
```

App Runner est le service le plus simple d'AWS pour faire tourner un container web. Tu lui donnes ton image Docker (ou ton code source) et il gère tout : build, deployment, scaling, HTTPS, load balancing.

**Avantages :** Ultra simple. Aucune configuration réseau. Auto-scaling inclus. HTTPS automatique.
**Inconvénients :** Moins de contrôle que ECS. Pas de VPC par défaut (configurable). Plus cher à fort traffic.
**Quand choisir :** Tu veux déployer vite, tu ne veux pas configurer VPC/ALB/ECS, équipe petite sans DevOps dédié.

**Option E : AWS Amplify (frontend + backend intégré)**

Amplify est une plateforme complète qui peut héberger un frontend statique ET un backend (via des fonctions Lambda ou un API GraphQL).

**Avantages :** Tout-en-un : hébergement, auth, API, base de données. Déploiement auto depuis Git. Idéal pour les devs fullstack qui ne veulent pas toucher à l'infra.
**Inconvénients :** Vendor lock-in fort (tu es lié à la façon de faire Amplify). Moins de contrôle. Peut devenir limitant pour des architectures complexes.
**Quand choisir :** Petit projet fullstack, prototypage rapide, pas de DevOps dans l'équipe.

**Option F : Kubernetes / EKS (grosse échelle)**

```
EKS (Kubernetes managé)
├── Deployments backend (auto-scaling)
├── Deployments workers
├── Ingress Controller (routage HTTP)
+ RDS Multi-AZ
+ S3 + CloudFront (frontend)
+ Helm pour le packaging
```

**Avantages :** Scaling massif, portabilité (pas locked à AWS), orchestration fine.
**Inconvénients :** Complexe à opérer. EKS coûte ~75$/mois rien que pour le control plane. Over-engineering si tu n'as pas 10+ microservices.
**Quand choisir :** Beaucoup de microservices, grosse équipe DevOps, besoin de portabilité multi-cloud.

### Le tableau comparatif global

| Option | Complexité | Coût mensuel* | Scaling | Gestion serveur | Cas d'usage |
|--------|-----------|--------------|---------|----------------|-------------|
| **EC2 + Docker Compose** | Faible | ~15$ | Non | Oui | MVP |
| **EC2 + RDS** | Moyenne | ~50-100$ | Manuel | Oui | Startup sérieuse |
| **App Runner + RDS** | Faible | ~30-80$ | Auto | Non | Petite équipe, vite en prod |
| **ECS Fargate + RDS** | Élevée | ~100-300$ | Auto | Non | Traffic variable, scaling |
| **Amplify** | Faible | ~0-50$ | Auto | Non | Prototypage, fullstack solo |
| **EKS (K8s)** | Très élevée | ~200+$ | Auto | Partiellement | Microservices, grosse échelle |

*Coûts approximatifs pour une app de taille modeste.

### Hors AWS — les alternatives

| Service | Ce que c'est | Quand l'utiliser |
|---------|-------------|-----------------|
| **Railway / Render** | PaaS (Platform as a Service). Tu push ton code, ils déploient. | Side projects, petites apps, pas envie de toucher à AWS |
| **Fly.io** | Containers à la edge (proches des utilisateurs). | API globales, low latency |
| **DigitalOcean App Platform** | PaaS simple, moins cher qu'AWS. | PME, startups qui veulent du simple |
| **GCP Cloud Run** | Équivalent Google de App Runner. Containers serverless. | Déjà sur GCP |
| **Azure Container Apps** | Équivalent Microsoft de App Runner. | Déjà sur Azure |

En entretien, mentionner que des alternatives existent montre que tu ne connais pas qu'un seul fournisseur.

### Ce que le recruteur attend

Pas la réponse parfaite. Il veut voir que tu :
- **Poses des questions** avant de répondre (budget, scale, contraintes, équipe)
- **Connais plusieurs options** et sais les comparer (pas juste "EC2 et c'est tout")
- **Sépares les préoccupations** : le frontend statique n'a pas besoin d'un serveur, la DB doit être managée
- **Sais expliquer les trade-offs** : simplicité vs. contrôle vs. coût vs. scaling
- **Ne proposes pas Kubernetes pour 50 utilisateurs** — mais tu sais expliquer quand K8s fait sens

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
- Corriger le problème (redémarrer le service, libérer du disque, rollback du dernier deployment...)
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

Problèmes : aucun test avant deployment, pas de rollback possible, un seul dev sait faire la manip, ça casse souvent.

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
- **Impact :** deployment en 5 min au lieu de 30, aucune connexion SSH

### Pourquoi pas tout automatiser d'un coup ?

Parce que la confiance se construit progressivement. Si les tests ne couvrent pas assez de cas, un deployment 100% automatique en prod va déployer des bugs plus vite. Phase 1 → Phase 2 → Phase 3 permet à l'équipe de gagner confiance à chaque étape.

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

## Scénario 5 — Choisir la bonne infra pour chaque projet

> **"On a 4 projets à héberger. Comment tu choisis l'infra pour chacun ?"**

### Projet A : API REST interne avec 1000 requêtes/jour

**Contexte :** API utilisée par une app mobile interne. Peu de traffic, budget minimal, une seule personne pour maintenir.

**Meilleur choix : Lambda + API Gateway**

Pourquoi : très peu de traffic, pas besoin d'un serveur qui tourne 24/7. Lambda = tu paies uniquement quand une requête arrive. Coût : quasi 0€ (Free Tier). API Gateway gère le HTTPS, le rate limiting, et le routage.

**Alternatives possibles :**
- **App Runner** : si l'API est containerisée et que tu veux quelque chose de simple sans devoir adapter le code pour Lambda. Un poil plus cher mais zéro adaptation du code.
- **EC2** : over-kill. Tu paies un serveur 24/7 pour 1000 requêtes/jour, c'est du gaspillage.

### Projet B : SaaS web avec 10 000 utilisateurs/jour

**Contexte :** Application web (React + API + PostgreSQL). Traffic régulier en journée, peu la nuit. Équipe de 5 devs. Besoin de fiabilité.

**Meilleur choix : ECS Fargate + RDS + S3/CloudFront**

```
CloudFront (CDN) → S3 (frontend statique)
ALB → ECS Fargate (API containers, auto-scaling)
       └── RDS PostgreSQL (subnet privé)
```

Pourquoi : traffic régulier, l'app doit tourner en permanence, connexion persistante à la DB. ECS Fargate = pas de serveurs à gérer, auto-scaling pour gérer les pics. RDS = DB managée.

**Alternatives possibles :**
- **EC2 + RDS** : moins cher, mais tu gères les serveurs (updates, Docker, monitoring). Bon choix si le budget est serré et que quelqu'un dans l'équipe sait gérer des serveurs.
- **App Runner + RDS** : plus simple que ECS, mais moins de contrôle sur le réseau (VPC peering, security groups custom). Bon pour une v1 rapide.
- **Lambda** : possible techniquement, mais les cold starts dégradent l'expérience utilisateur, et les connexions DB sont compliquées à gérer (il faut RDS Proxy).

### Projet C : Traitement de fichiers uploadés (redimensionner des images)

**Contexte :** Les utilisateurs uploadent des photos. On doit les redimensionner en 3 tailles et les stocker. Volume variable : parfois 10 uploads/jour, parfois 10 000.

**Meilleur choix : Lambda + S3 (architecture événementielle)**

```
Utilisateur → upload → S3 bucket (originaux)
                         │
                         └── trigger Lambda → resize → S3 bucket (résultats)
```

Pourquoi : événementiel pur. Un fichier arrive dans S3 → Lambda se déclenche automatiquement → traite le fichier → remet le résultat dans S3. Pas besoin de serveur entre les uploads. Scaling automatique (100 uploads en même temps → 100 Lambdas en parallèle).

**Alternatives possibles :**
- **ECS avec une queue SQS** : si le traitement dure >15 min (limite de Lambda) ou nécessite beaucoup de mémoire (>10 Go). SQS = file d'attente, ECS = workers qui consomment la file.
- **Step Functions + Lambda** : si le traitement a plusieurs étapes (resize → watermark → optimise → notify). Step Functions orchestre les Lambdas.

### Projet D : Site vitrine / blog d'entreprise

**Contexte :** Site marketing avec du contenu statique. Pas de backend custom, juste du contenu qui change rarement. Budget quasi nul.

**Meilleur choix : Amplify Hosting (ou Vercel / Netlify)**

Pourquoi : c'est du contenu statique. Aucun besoin de serveur, de container, ou de quoi que ce soit de complexe. Tu push sur Git, le site est déployé automatiquement sur un CDN mondial.

```
Git push → Amplify Hosting → CDN mondial → utilisateurs
```

Coût : gratuit (Free Tier Amplify, ou plan gratuit Vercel/Netlify).

**Alternatives possibles :**
- **S3 + CloudFront** : même résultat, configuration manuelle. Mieux si tu veux tout contrôler côté AWS.
- **EC2 avec nginx** : over-kill absolu. Un serveur 24/7 pour servir des fichiers HTML, c'est du gaspillage d'argent et de temps.

### Le tableau de décision

| Critère | Lambda | App Runner | ECS Fargate | EC2 | Amplify / Vercel |
|---------|--------|-----------|-------------|-----|-----------------|
| Traffic | Sporadique | Constant faible | Variable / fort | Constant | Statique |
| Durée d'exécution | < 15 min | Illimitée | Illimitée | Illimitée | N/A |
| Stateful | Non | Non | Oui | Oui | Non |
| Connexion DB | Compliqué | Facile | Facile | Facile | Non (ou via API) |
| Scaling | Auto, instantané | Auto | Auto (configurable) | Manuel / ASG | Auto (CDN) |
| Gestion serveur | Aucune | Aucune | Aucune | Toi | Aucune |
| Coût faible traffic | ~0€ | ~5-15$/mois | ~20-50$/mois | ~15-30$/mois | ~0€ |
| Coût fort traffic | Peut exploser | Moyen | Prévisible | Prévisible | Faible (CDN) |
| Complexité config | Faible | Très faible | Élevée | Moyenne | Très faible |

### Ce que le recruteur attend

- Tu ne donnes pas la même réponse pour les 4 projets
- Tu justifies par des critères concrets (traffic, durée, coût, état, équipe)
- Tu connais les limites de chaque solution ET les alternatives
- Tu sais que "le meilleur choix" dépend du contexte — il n'y a pas de réponse universelle
- Tu sépares frontend statique / backend / traitements async : chacun a une solution différente

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
| **Errors** | Ça marche ? | Taux d'errors 5xx |
| **Saturation** | C'est plein ? | CPU, RAM, disque, connexions DB |

### Étape 2 — Instrumenter l'app

```
App → expose /metrics → Prometheus scrape → Grafana affiche
```

- Ajouter la librairie Prometheus à l'app (pour notre projet : `prometheus-fastapi-instrumentator`)
- Déployer Prometheus + Grafana (docker-compose, c'est le plus simple)

### Étape 3 — Créer les dashboards

Un dashboard par "audience" :
- **Dashboard technique :** latency, errors, CPU, RAM, slow queries DB
- **Dashboard business :** nombre d'utilisateurs actifs, nombre de tâches créées (pour le CTO)

### Étape 4 — Configurer les alertes

Bonnes alertes :
- "Le error rate 5xx dépasse 5% depuis 5 minutes" → **actionnable** (il y a un bug ou un service down)
- "Le response time p95 dépasse 2 secondes depuis 10 minutes" → **actionnable** (performance dégradée)

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
                    ┌─── Blue (v1.0 — actuelle) ◄── 100% du traffic
Load Balancer ──────┤
                    └─── Green (v1.1 — nouvelle) ◄── 0% du traffic
```

1. Tu déploies la v1.1 sur le Green (pendant que Blue sert toujours les users)
2. Tu testes Green (smoke tests, sanity check)
3. Tu bascules le load balancer : Green reçoit 100% du traffic
4. Si ça marche → tu supprimes Blue. Si ça casse → tu rebascules sur Blue en 10 secondes.

**Avantages :** Rollback instantané. Zéro downtime.
**Inconvénients :** Double infra pendant la transition (coût). Problème si la DB a changé de schéma entre v1.0 et v1.1.

### Option B — Canary

```
                    ┌─── v1.0 ◄── 95% du traffic
Load Balancer ──────┤
                    └─── v1.1 ◄── 5% du traffic (les "canaris")
```

1. Tu déploies la v1.1 sur quelques instances
2. Tu envoies 5% du traffic vers la v1.1
3. Tu surveilles les métriques (errors, latency)
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
| **Blue-Green** | Moyenne | Instantané | Apps critiques, peu de deployments |
| **Canary** | Élevée | Rapide | Apps à fort traffic, besoin de tester en conditions réelles |
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
- **.dockerignore** — Fichier qui dit à Docker quels fichiers ne pas copier dans l'image (`.git/`, `node_modules/`, `.env`). Comme `.gitignore` mais pour Docker.
- **Service discovery** — Dans Docker Compose, les containers se trouvent par le nom du service (DNS interne). `backend` résout vers l'IP du container backend.
- **Health check** — Endpoint (`/health`) qui retourne OK. Utilisé par Docker, K8s, et les load balancers pour vérifier que l'app répond.

## CI/CD

- **CI** — Vérification automatique à chaque push (lint, tests). CD — Déploiement automatique (ou semi-automatique).
- **Pipeline typique** — Lint → Tests → Build → Deploy. Fail fast.
- **Delivery vs Deployment** — Delivery = bouton manuel. Deployment = automatique.
- **Runner** — La machine qui exécute les jobs du pipeline.

## Outils du projet

- **Bun vs npm** — Bun est un runtime JS + package manager tout-en-un, plus rapide que Node.js + npm. `bun install` = `npm install`. `bunx` = `npx`. En entreprise, tu verras surtout npm, mais Bun gagne du terrain.
- **uv vs pip** — uv est un gestionnaire de dépendances Python ultra-rapide (écrit en Rust). `uv sync` = `pip install -r requirements.txt` + `python -m venv`. Même concept, outil plus moderne.

## AWS

- **EC2** — Serveur virtuel. Tu choisis puissance + OS, tu paies à l'heure.
- **VPC** — Réseau privé isolé dans AWS. Subnets publics/privés, routage, firewall.
- **IAM** — Système de permissions. Users, roles, policies. Moindre privilège.
- **Security Group** — Firewall virtuel par port et IP source. Stateful.
- **S3** — Stockage d'objets illimité. Backups, static files, logs.
- **RDS** — Base de données managée. Backups, updates, high availability par AWS.
- **Lambda** — Serverless. Code exécuté à la demande, facturation à l'exécution.
- **Cold start** — Première exécution Lambda plus lente (démarrage de l'environnement).
- **User Data** — Script bash exécuté automatiquement au premier démarrage d'un EC2. Sert à installer Docker, cloner le projet, lancer l'app sans connexion SSH manuelle.
- **NAT Gateway** — Permet aux instances dans un subnet privé d'accéder à Internet (pour les mises à jour) sans être accessibles depuis Internet. Comme une sortie de secours : tu peux sortir mais personne ne peut entrer.
- **Reverse Proxy vs Load Balancer** — Un reverse proxy reçoit les requêtes à la place de l'app (1 serveur derrière). Un load balancer répartit le traffic entre N serveurs. En pratique, souvent le même outil (nginx, ALB).

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

- **K8s** — Orchestrateur de containers. Déploiement, scaling, high availability sur un cluster.
- **Pod** — Unité de base. 1 pod ≈ 1 container.
- **Deployment** — Gère un groupe de pods. Maintient N replicas, rolling updates, self-healing.
- **Service** — Point d'accès réseau stable vers un groupe de pods.
- **Rolling Update** — Mise à jour progressive des pods : K8s remplace les pods un par un (crée v2, attend qu'il soit prêt, supprime v1). Zéro downtime.

## Monitoring

- **3 piliers** — Metrics (chiffres), Logs (texte), Traces (parcours des requêtes).
- **Prometheus** — Collecteur de métriques. Pull model, scrape /metrics.
- **Grafana** — Visualisation. Dashboards à partir de Prometheus et autres.
- **Bonne alerte** — Actionnable, basée sur les symptômes, pas trop fréquente.
- **Structured logs** — Logs en JSON au lieu de plain text. Parsables par les machines (Elasticsearch, Loki, Datadog). En prod, toujours du JSON structuré.
- **Golden Signals** — Les 4 métriques clés (Google SRE) : Latency, Traffic, Errors, Saturation. Commence par celles-là.
