# Module 5 : AWS

> **Prérequis :** Module 2 (Réseau — IP, ports, subnets), Module 3 (Docker — pour déployer l'app)

> **En résumé :** Tu découvres le cloud en déployant ton application sur un vrai serveur AWS (EC2 + VPC + IAM). Tu découvres aussi les autres services (S3, RDS, Lambda, ECS, etc.) pour les comprendre — mais pour le projet, tu n'as besoin que d'un EC2 avec Docker Compose.

## C'est quoi AWS et pourquoi ça existe ?

**Le problème :** Avant le cloud, pour mettre un site en ligne, il fallait acheter un serveur physique (cher), le brancher quelque part (data center), le configurer, le maintenir, et prier pour qu'il ne tombe pas en panne. Si ton site explose en traffic → tu es coincé. Si personne ne vient → tu paies quand même.

**AWS** (Amazon Web Services) te permet de louer des serveurs, du stockage, des bases de données — exactement ce dont tu as besoin, quand tu en as besoin, en quelques clics. C'est comme **louer un appartement** au lieu de construire une maison.

**Les analogies :**
- **AWS** = grande surface de matériel informatique
- **EC2** = louer un ordinateur
- **S3** = louer un casier de stockage
- **VPC** = ta pièce privée dans l'immeuble AWS
- **IAM** = le système de badges (qui a le droit de faire quoi)
- **RDS** = embaucher quelqu'un pour gérer ta base de données
- **Lambda** = un cuisinier freelance qui vient, cuisine un plat, et repart (tu paies uniquement le plat)

## Création de compte + Free Tier

1. Va sur [aws.amazon.com](https://aws.amazon.com) et crée un compte
2. Tu auras besoin d'une carte bancaire (mais le Free Tier est gratuit pendant 12 mois)

⚠️ **IMPORTANT — Les limites du Free Tier :**
- **EC2** : 750h/mois de t3.micro (1 instance 24/7 = OK)
- **S3** : 5 Go de stockage
- **RDS** : 750h/mois de db.t3.micro
- **Lambda** : 1 million de requêtes/mois gratuites (largement suffisant pour apprendre)
- Pour le projet de ce cursus, tu n'utilises que **EC2** (750h/mois = 1 instance 24/7). Les autres services sont expliqués pour ta culture mais pas nécessaires.
- Au-delà → tu paies. **Mets une alerte de facturation :**
  - AWS Console → Billing → Budgets → Create Budget → 5$ threshold

## IAM — Le système de permissions

IAM (Identity and Access Management) contrôle qui peut faire quoi sur ton compte AWS.

| Concept | C'est quoi |
|---------|-----------|
| **User** | Un compte utilisateur (une personne ou un programme) |
| **Role** | Un ensemble de permissions qu'on peut "enfiler" temporairement |
| **Policy** | Un document JSON qui dit "autorisé à faire X sur Y" |

**Bonne pratique :** Ne jamais utiliser le compte root pour travailler. Crée un user IAM avec les droits nécessaires.

**Comment créer un user IAM (étape par étape dans le navigateur) :**

1. Connecte-toi à la [console AWS](https://console.aws.amazon.com) (c'est le site web d'AWS, pas un terminal)
2. Dans la barre de recherche en haut, tape **"IAM"** et clique dessus
3. Dans le menu à gauche, clique sur **"Users"** (c'est bien dans la section Users, pas ailleurs)
4. Clique sur **"Create user"**
5. Nom : `admin-dev` → **Next**
6. Clique **"Attach policies directly"** → cherche et coche **"AdministratorAccess"** → **Next** → **Create user**
7. Clique sur le user `admin-dev` que tu viens de créer
8. Onglet **"Security credentials"** → descends jusqu'à **"Access keys"** → **"Create access key"**
9. Choisis **"Command Line Interface (CLI)"** → coche la confirmation → **Next** → **Create access key**
10. **Note l'Access Key ID et le Secret Access Key** (tu ne les reverras plus après avoir fermé cette page)

> **"AdministratorAccess" c'est pour le cours uniquement.** En production, on donne le minimum de droits nécessaires (principe du moindre privilège).

## AWS CLI

```bash
# Installation
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install -y unzip
unzip awscliv2.zip
sudo ./aws/install

aws --version
# aws-cli/2.x.x

# Configuration
aws configure
# AWS Access Key ID: ta_clé
# AWS Secret Access Key: ton_secret
# Default region name: eu-west-3  (Paris)
# Default output format: json
```

## EC2 — Louer un serveur

EC2 (Elastic Compute Cloud) = un serveur virtuel dans le cloud.

### Vocabulaire

| Terme | C'est quoi |
|-------|-----------|
| **Instance** | Un serveur EC2 en cours d'exécution |
| **AMI** | L'image du système d'exploitation (Ubuntu, Amazon Linux...) |
| **Instance type** | La puissance (t3.micro = gratuit, petit) |
| **Key pair** | Clé SSH pour te connecter |
| **Security group** | Firewall de l'instance |

### Lancer une instance (console)

1. **EC2** → **Launch Instance**
2. Name: `devops-server`
3. AMI: **Ubuntu Server 24.04 LTS**
4. Instance type: **t3.micro** (Free Tier)
5. Key pair: **Create new** → `devops-key` → Download `.pem`
6. Security group: autoriser **SSH (22)**, **HTTP (80)**, **port 8000** (le port de l'API backend dans notre Docker Compose)
7. **Launch**

### Se connecter

```bash
# Rendre la clé utilisable
chmod 400 ~/devops-key.pem

# Se connecter
ssh -i ~/devops-key.pem ubuntu@IP_PUBLIQUE_DE_TON_INSTANCE
# Welcome to Ubuntu...
```

### Avec AWS CLI

```bash
# Lister tes instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]' --output table

# Arrêter une instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Démarrer une instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

## S3 — Stockage

> **Pas nécessaire pour le projet**, mais bon à connaître — S3 est l'un des services les plus utilisés d'AWS.

S3 (Simple Storage Service) = un espace de stockage illimité dans le cloud.

| Terme | C'est quoi |
|-------|-----------|
| **Bucket** | Un conteneur de fichiers (comme un dossier racine) |
| **Object** | Un fichier dans un bucket |

```bash
# Créer un bucket
aws s3 mb s3://mon-bucket-unique-12345

# Uploader un fichier
aws s3 cp fichier.txt s3://mon-bucket-unique-12345/

# Lister le contenu
aws s3 ls s3://mon-bucket-unique-12345/

# Télécharger
aws s3 cp s3://mon-bucket-unique-12345/fichier.txt ./
```

## VPC — Ton réseau privé

Un VPC (Virtual Private Cloud) isole tes ressources AWS dans ton propre réseau.

| Concept | C'est quoi | Analogie |
|---------|-----------|----------|
| **VPC** | Ton réseau privé | Ton immeuble |
| **Subnet public** | Accessible depuis Internet | Rez-de-chaussée avec porte sur la rue |
| **Subnet privé** | Pas accessible depuis Internet | Étages sans accès direct |
| **Internet Gateway** | La porte vers Internet | La porte d'entrée de l'immeuble |
| **Route Table** | Les règles de routage | Le plan d'évacuation |
| **NAT Gateway** | Permet au subnet privé d'accéder à Internet (mais pas l'inverse) | Sortie de secours |

### Comment ça s'assemble

```
         Internet
            │
     ┌──────┴──────┐
     │ Internet     │
     │ Gateway      │
     └──────┬──────┘
            │
┌───────────┴──────────────────────────────────────┐
│  VPC (10.0.0.0/16)                               │
│                                                   │
│  ┌─────────────────────┐  ┌────────────────────┐ │
│  │ Subnet PUBLIC        │  │ Subnet PRIVATE      │ │
│  │ 10.0.1.0/24         │  │ 10.0.2.0/24        │ │
│  │                     │  │                     │ │
│  │  ┌──────────────┐   │  │  ┌──────────────┐  │ │
│  │  │ EC2          │   │  │  │ RDS          │  │ │
│  │  │ (backend)    │──────▶│  │ (PostgreSQL) │  │ │
│  │  │ IP publique  │   │  │  │ Pas d'IP pub │  │ │
│  │  └──────────────┘   │  │  └──────────────┘  │ │
│  │                     │  │                     │ │
│  │  Security Group:    │  │  Security Group:    │ │
│  │  SSH(22), HTTP(80)  │  │  PostgreSQL(5432)   │ │
│  │  depuis Internet    │  │  depuis EC2 seul.   │ │
│  └─────────────────────┘  └────────────────────┘ │
│                                                   │
└──────────────────────────────────────────────────┘
```

> Les concepts de subnets et CIDR viennent du Module 2 (Réseau). Les Security Groups fonctionnent comme les firewalls vus au Module 2 (`ufw`).

**Ce qu'il faut retenir :**
- L'EC2 est dans le subnet **public** → il a une IP publique, accessible depuis Internet
- La base RDS est dans le subnet **privé** → pas d'IP publique, accessible uniquement depuis le VPC
- Les Security Groups filtrent le traffic : le RDS n'accepte que le port 5432 venant de l'EC2
- L'Internet Gateway connecte le subnet public à Internet

**Pour le projet de ce cursus : un VPC avec un seul subnet public suffit.** Le schéma ci-dessus avec un subnet privé + RDS, c'est pour te montrer comment ça fonctionne en production — tu n'as pas besoin de le créer.

## RDS — Base de données managée

> **Tu n'as PAS besoin de créer un RDS pour le projet.** Le backend utilise PostgreSQL dans un container Docker sur l'EC2 (comme dans le Module 3). Cette section est là pour comprendre ce que c'est et quand l'utiliser en production.

**Le problème :** Tu peux installer PostgreSQL sur un EC2 toi-même. Mais qui fait les backups ? Qui met à jour la base ? Qui redémarre si ça crash à 3h du matin ? Toi. Tout seul. Tout le temps.

**RDS** (Relational Database Service) = tu choisis ton moteur (PostgreSQL, MySQL, etc.), AWS gère tout le reste : automated backups, security updates, high availability, replication.

**Analogie :** Au lieu de faire toi-même ton pain tous les jours (installer et maintenir PostgreSQL sur EC2), tu vas chez le boulanger (RDS). Le pain est le même, mais tu n'as pas à t'occuper du four.

### Les concepts clés

| Concept | C'est quoi |
|---------|-----------|
| **Instance RDS** | Un serveur de base de données managé |
| **Engine** | Le type de base : PostgreSQL, MySQL, MariaDB, etc. |
| **Multi-AZ** | Ta base est copiée automatiquement dans un 2ème datacenter. Si le premier tombe, le 2ème prend le relais. C'est ça la "haute disponibilité" (high availability). |
| **Read Replica** | Une copie de ta base en lecture seule. Les requêtes de lecture vont sur la copie, ça soulage la base principale. |
| **Automated Backups** | AWS fait une sauvegarde complète de ta base tous les jours automatiquement. Si tu casses tout, tu peux revenir à la sauvegarde d'hier. |

### Créer une instance RDS (console) — Exemple pour référence

> **Tu n'es pas obligé de suivre ces étapes.** C'est un exemple pour te montrer comment on crée un RDS si tu en as besoin un jour en production. Pour le projet du cursus, PostgreSQL tourne dans un container Docker sur ton EC2 — c'est suffisant.

1. **RDS** → **Create database**
2. Engine: **PostgreSQL**
3. Template: **Free Tier**
4. Instance type: **db.t3.micro**
5. Master username: `admin`
6. Master password: choisis un mot de passe solide
7. VPC: `devops-vpc`
8. Public access: **No** (bonne pratique : la DB ne doit pas être exposée à Internet)
9. Security group: crées-en un qui autorise le port **5432** uniquement depuis le Security Group de ton EC2
10. **Create**

### Se connecter depuis EC2 (si tu avais créé un RDS)

```bash
# (Exemple pour référence — tu n'as pas besoin de faire ça pour le projet)
# Depuis ton instance EC2 (pas depuis ta machine locale !) :
sudo apt install -y postgresql-client
psql -h MON-INSTANCE.rds.amazonaws.com -U admin -d postgres
# Password: ton_mot_de_passe
# postgres=>
```

Le point important : la base RDS est dans un **subnet privé** (pas d'accès Internet direct). Ton EC2 dans le même VPC peut y accéder via le réseau interne AWS.

### Avec AWS CLI

```bash
# Lister tes instances RDS
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,Engine,DBInstanceStatus,Endpoint.Address]' --output table

# Supprimer (attention !)
aws rds delete-db-instance --db-instance-identifier mon-instance --skip-final-snapshot
```

⚠️ **Si tu as créé un RDS (pas nécessaire pour le projet), n'oublie pas de le supprimer** — même en Free Tier, si tu dépasses 750h/mois, ça coûte.

### Quand utiliser RDS vs PostgreSQL sur EC2 ?

| | RDS | PostgreSQL sur EC2 |
|--|-----|-------------------|
| Backups | Automatiques | À toi de les configurer |
| Updates | Gérées par AWS | À toi de les faire |
| High availability | Multi-AZ en un clic | À toi de monter la replication |
| Prix | Plus cher | Moins cher |
| Contrôle | Limité (pas d'accès SSH à la machine) | Total |

**En résumé :** En prod, utilise RDS. Le surcoût est largement compensé par le temps que tu ne passes pas à gérer la base.

## Lambda — Le serverless (optionnel)

> Cette section est optionnelle. Lambda n'est pas utilisé dans le projet fil rouge. Si tu découvres AWS, concentre-toi d'abord sur EC2 + VPC + RDS et reviens ici plus tard.

**Le concept en 30 secondes :** Lambda exécute ton code sans serveur à gérer (d'où le nom "serverless"). Tu envoies une fonction Python/JS, AWS l'exécute quand un événement arrive (requête HTTP, upload S3, timer), et tu paies uniquement le temps d'exécution. **Scaling automatique** = si 1 000 personnes appellent ta fonction en même temps, AWS lance 1 000 copies automatiquement. Pas besoin de configurer quoi que ce soit.

**Analogie :** Un cuisinier freelance. Tu l'appelles quand tu as une commande, il cuisine, il repart. 0 commande = 0€.

| | Lambda | EC2 |
|--|--------|-----|
| Durée d'exécution | Courte (<15 min) | Illimitée |
| Scaling | Automatique | Manuel |
| Prix | À l'exécution | À l'heure (même au repos) |
| Cas d'usage | Webhooks (voir ci-dessous), tâches ponctuelles | Apps qui tournent 24/7 |

**C'est quoi un webhook ?** C'est un message automatique envoyé par un service externe vers ton API quand quelque chose se passe de leur côté. Par exemple : quand un client paie sur Stripe, Stripe envoie un message HTTP à ton API pour dire "le paiement X a été confirmé". Tu n'as pas besoin de demander à Stripe toutes les 5 secondes "est-ce que quelqu'un a payé ?" — c'est Stripe qui te prévient automatiquement. C'est ça un webhook : un "appel inversé" — au lieu que TOI tu appelles le service, c'est LE SERVICE qui t'appelle.

Pour créer et tester une Lambda, voir la [documentation AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html).

## Autres services AWS à connaître

> **Aucun de ces services n'est nécessaire pour le projet.** Ton app tourne sur un EC2 avec Docker Compose, et c'est suffisant. Ces sections sont là pour ta culture et pour les entretiens — on te demandera souvent "c'est quoi ECS ?" ou "RDS vs DynamoDB ?".

### SQS — Les files d'attente (et pourquoi c'est important)

Avant de parler de SQS, il faut comprendre un problème fondamental.

**Le problème du traitement direct (synchrone) :**

Imagine un restaurant où le serveur prend ta commande et reste planté devant toi pendant que le cuisinier prépare ton plat. Pendant ce temps, il ne peut pas prendre d'autres commandes. Si 50 clients arrivent en même temps, 49 attendent debout. Et si le cuisinier fait tomber ton plat ? Le serveur ne sait pas quoi faire, ta commande est perdue.

C'est ce qui se passe quand ton API traite tout **directement** (de manière **synchrone**) : chaque requête bloque un processus en attendant la fin du traitement. Si le traitement est long (envoyer un email, générer un PDF, traiter un paiement) ou que beaucoup de requêtes arrivent en même temps, tout ralentit ou crash.

**La solution : la file d'attente (asynchrone)**

Maintenant imagine que le serveur prend ta commande, l'écrit sur un ticket et l'accroche sur un rail en cuisine. Il est libre immédiatement pour prendre la commande suivante. Le cuisinier prend les tickets un par un, à son rythme. Si le cuisinier fait tomber le plat, le ticket est toujours là — il peut refaire le plat.

C'est exactement ce que fait **SQS** (Simple Queue Service) : une file d'attente dans le cloud.

```
SANS file d'attente (synchrone) :
  Requête → API traite directement → si ça crash, c'est perdu
  Requête → API traite directement → si 1000 requêtes arrivent, l'API crash

AVEC file d'attente (asynchrone) :
  Requête → API met un message dans SQS → répond "OK, reçu" (instantané)
                                              │
                                    Lambda/Worker consomme la queue
                                    et traite à son rythme
                                              │
                                    Si ça échoue → le message reste
                                    dans la queue, on réessaie
```

**SQS** = une file d'attente managée par AWS. Tu y mets des messages, un autre programme les consomme. Les messages ne sont jamais perdus — si le consommateur crash, le message retourne dans la file et sera re-traité.

**Quand utiliser une file d'attente :**
- Le traitement est **long** (>1 seconde) — envoyer un email, générer un rapport, traiter une image
- L'utilisateur **n'a pas besoin du résultat immédiatement** — "votre commande est en cours de traitement"
- Tu as des **pics de traffic** — 1000 requêtes arrivent d'un coup, la file absorbe le pic
- Le traitement **ne doit pas être perdu** — webhooks de paiement, commandes

**Quand NE PAS utiliser une file d'attente :**
- L'utilisateur a besoin du résultat **tout de suite** — afficher une page, lire une liste de tâches
- Le traitement est **rapide** (<100ms) — pas besoin de découpler

| | Traitement direct (synchrone) | File d'attente (asynchrone) |
|--|------|------|
| Vitesse de réponse | Le client attend la fin du traitement | Le client reçoit "OK, reçu" instantanément |
| Si ça crash | Le message est perdu | Le message reste dans la queue |
| Pics de traffic | L'API sature | La queue absorbe, le worker traite à son rythme |
| Complexité | Simple | Plus de composants à gérer |

Tu retrouveras SQS dans les [exercices system design](system-design-exercises.md) — c'est un pattern qu'on utilise très souvent en entretien.

### DynamoDB — Base de données NoSQL

**RDS** te donne une base relationnelle classique (tableaux avec colonnes, SQL, relations entre tables). **DynamoDB** c'est une base **NoSQL** (Not Only SQL) — au lieu de tableaux rigides, tu stockes des documents JSON flexibles.

| | RDS (PostgreSQL) | DynamoDB |
|--|-------------------|----------|
| Structure | Tableaux avec colonnes fixes | Documents JSON flexibles |
| Langage | SQL | API AWS (pas de SQL) |
| Scaling | Vertical (machine plus grosse) | Horizontal automatique (AWS gère) |
| Prix | À l'heure (même au repos) | À la requête (0 requête = 0€) |
| Cas d'usage | Relations complexes (users + commandes + produits) | Données simples à très fort traffic (sessions, panier, logs) |

**Analogie :** RDS c'est un classeur avec des fiches bien rangées dans des catégories. DynamoDB c'est un tas de post-its — chaque post-it peut avoir des infos différentes, mais c'est ultra rapide pour en ajouter ou en retrouver un.

**Quand utiliser quoi ?**
- Ton app a des relations entre les données (un utilisateur a des commandes, une commande a des produits) → **RDS**
- Tu as besoin de lire/écrire très vite des données simples (sessions utilisateur, cache, compteurs en temps réel) → **DynamoDB**
- Tu ne sais pas → **RDS**. Le SQL est universel, tu peux toujours migrer plus tard

### ECS — Containers managés sur AWS

Dans le Module 3, tu as lancé tes containers Docker sur un EC2 avec `docker compose`. Ça marche, mais **c'est toi qui gères le serveur** : les mises à jour, le monitoring, le scaling. Si ton EC2 tombe, ton app tombe.

**ECS** (Elastic Container Service) = tu donnes tes images Docker à AWS, et AWS les lance, les surveille, les redémarre si elles crash, et les scale automatiquement. Tu ne gères plus le serveur.

| | Docker sur EC2 | ECS |
|--|----------------|-----|
| Qui gère le serveur ? | Toi | AWS (avec Fargate) |
| Scaling | Manuel (`docker compose up`) | Automatique |
| Monitoring | À toi de le configurer | Intégré (CloudWatch) |
| Prix | Tu paies l'EC2 | Tu paies le CPU/RAM utilisé (Fargate) |
| Complexité | Simple | Plus de configuration initiale |

ECS a deux modes :
- **EC2 mode** — tes containers tournent sur des EC2 que tu gères (tu contrôles, mais plus de travail)
- **Fargate mode** — tes containers tournent sans serveur du tout (AWS gère tout, tu paies à l'usage). C'est le mode recommandé pour commencer

**Analogie :** Docker sur EC2 c'est cuisiner chez toi — tu gères les courses, le four, le ménage. ECS Fargate c'est une cuisine fantôme (dark kitchen) — tu envoies la recette (ton image Docker), quelqu'un d'autre cuisine et livre.

### EKS — Kubernetes managé sur AWS

Si tu as fait le Module 9 (Kubernetes), tu connais déjà K8s avec minikube en local. **EKS** (Elastic Kubernetes Service) = la même chose, mais sur AWS. AWS gère le control plane (le cerveau du cluster K8s), toi tu gères les workers (les machines qui font tourner tes pods).

| | ECS | EKS |
|--|-----|-----|
| Outil | Spécifique AWS | Kubernetes (standard, tourne partout) |
| Portabilité | Bloqué sur AWS | Migratable (GKE sur Google, AKS sur Azure) |
| Complexité | Plus simple | Plus complexe, mais plus flexible |
| Communauté | AWS uniquement | Énorme communauté open-source |
| Prix | Moins cher (pas de frais de control plane) | ~75$/mois pour le control plane + les workers |

**Quand utiliser quoi ?**
- Tu débutes et tu restes sur AWS → **ECS Fargate** (le plus simple)
- Tu veux de la portabilité multi-cloud ou tu connais déjà K8s → **EKS**
- Tu as un petit projet avec peu de traffic → **Docker sur EC2** (comme dans ce cursus)
- Tu as des fonctions courtes et ponctuelles → **Lambda**

```
Petit projet         ──→ Docker sur EC2
App web classique    ──→ ECS Fargate
Multi-cloud / K8s    ──→ EKS
Tâches ponctuelles   ──→ Lambda
```

### Route 53 — Le DNS d'AWS

Tu as vu le DNS dans le Module 2 (Réseau) : c'est le système qui traduit un nom de domaine (`monapp.com`) en adresse IP (`13.38.42.100`). **Route 53** c'est le service DNS d'AWS.

Sans Route 53, tes utilisateurs doivent taper `http://13.38.42.100` pour accéder à ton app. Avec Route 53, ils tapent `monapp.com`.

**Ce que Route 53 fait concrètement :**
- **Acheter un nom de domaine** directement sur AWS (ou en importer un acheté ailleurs)
- **Faire pointer le domaine** vers ton EC2, ton Load Balancer, ton CloudFront, etc.
- **Health checks** : si ton serveur tombe, Route 53 peut rediriger automatiquement vers un serveur de secours
- **Routage géographique** : envoyer les utilisateurs européens vers un serveur en Europe et les américains vers un serveur aux US

**Analogie :** C'est les Pages Jaunes d'AWS. Tu y enregistres "mon entreprise s'appelle monapp.com et elle se trouve à cette adresse IP". Si tu déménages (tu changes de serveur), tu mets à jour l'adresse dans Route 53.

| Concept | C'est quoi |
|---------|-----------|
| **Hosted Zone** | La fiche de ton domaine — toutes les règles DNS pour `monapp.com` |
| **Record A** | Fait pointer un nom vers une IP (`monapp.com → 13.38.42.100`) |
| **Record CNAME** | Fait pointer un nom vers un autre nom (`www.monapp.com → monapp.com`) |
| **TTL** | Time To Live — combien de temps les navigateurs gardent l'adresse en cache avant de re-vérifier |

En pratique, Route 53 est un des derniers services que tu configures — d'abord tu fais tourner ton app, ensuite tu lui donnes un joli nom de domaine.

### CloudWatch — Le monitoring intégré d'AWS

Dans le Module 8, tu verras Prometheus + Grafana pour le monitoring. **CloudWatch** c'est l'équivalent natif d'AWS — il est déjà activé par défaut sur tous tes services AWS, sans rien installer.

**Ce que CloudWatch fait :**
- **Métriques** : CPU, RAM, réseau de tes EC2, nombre de requêtes sur ton Load Balancer, erreurs Lambda... tout est collecté automatiquement
- **Logs** : centralise les logs de tes containers ECS, de tes Lambdas, de tes applications — au lieu de se connecter en SSH pour faire `docker logs`
- **Alarmes** : "si le CPU de mon EC2 dépasse 80% pendant 5 minutes, envoie-moi un email"

**Analogie :** CloudWatch c'est le tableau de bord de ta voiture — vitesse, niveau d'essence, température moteur. Tu ne l'installes pas, il est là de base. Prometheus + Grafana c'est comme installer un tableau de bord custom plus avancé.

| | CloudWatch | Prometheus + Grafana |
|--|------------|---------------------|
| Installation | Rien à faire, déjà activé | À installer et configurer toi-même |
| Métriques AWS | Automatiques (EC2, RDS, Lambda...) | Il faut les exporter manuellement |
| Métriques applicatives | Possible mais plus complexe | Très simple (`/metrics` endpoint) |
| Coût | Payant au-delà du Free Tier | Gratuit (open-source) |
| Dashboards | Basiques | Très puissants et personnalisables |

En pratique, on utilise souvent **les deux** : CloudWatch pour les métriques d'infrastructure AWS (CPU EC2, erreurs Lambda), et Prometheus + Grafana pour les métriques applicatives (temps de réponse de l'API, nombre de tâches créées).

## Projet pratique : Déployer le projet sur AWS

### 1. Créer un VPC (console AWS)

- **VPC** → **Create VPC**
- VPC and more → Name: `devops-vpc`
- CIDR: `10.0.0.0/16`
- 1 subnet public, 0 subnet privé
- Laisser les autres options par défaut → **Create**

### 2. Lancer une instance EC2

- **EC2** → **Launch Instance**
- Name: `devops-server`
- AMI: Ubuntu 24.04 LTS
- Type: t3.micro
- Key pair: `devops-key`
- Network: choisis `devops-vpc` et le subnet public
- Auto-assign public IP: **Enable**
- Security group: SSH (22), HTTP (80), Custom TCP (8000)
- **Launch**

### 3. Se connecter et installer Docker

```bash
ssh -i ~/devops-key.pem ubuntu@IP_PUBLIQUE

# Sur le serveur :
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker ubuntu
# Déconnecte et reconnecte
exit
ssh -i ~/devops-key.pem ubuntu@IP_PUBLIQUE
```

### 4. Lancer l'application

```bash
# Sur le serveur :
mkdir devops-project && cd devops-project

# Créer le docker-compose.yml (copie celui du Module 3)
# Ou clone ton repo GitHub :
git clone https://github.com/TON_USER/devops-project.git .

docker compose up -d --build
```

### 5. Tester

Ouvre ton navigateur et va sur `http://IP_PUBLIQUE` — tu devrais voir la Task List.

```bash
curl http://IP_PUBLIQUE:8000/api/tasks
# [{"id":1,"title":"Apprendre Docker","done":false}]
```

💡 **Si ça ne marche pas :** vérifie le Security Group (port 80 et 8000 ouverts) et que l'instance a une IP publique.

⚠️ **N'oublie pas de stopper/terminer ton instance quand tu as fini** pour éviter les coûts :
```bash
aws ec2 terminate-instances --instance-ids i-TON_INSTANCE_ID
```

### 6. Bonus — User Data (automatiser l'installation)

Tu viens de faire les étapes 3 et 4 à la main (SSH, installer Docker, cloner, lancer). **User Data** permet d'automatiser tout ça : c'est un script bash que tu donnes à l'EC2 au moment de sa création, et il s'exécute automatiquement au premier démarrage.

C'est comme laisser une note au livreur : "quand tu arrives, installe Docker et lance l'app."

Pour l'utiliser, au moment de créer l'EC2 (étape 2), clique sur **"Advanced details"** en bas de la page, et dans le champ **"User data"**, colle ce script :

```bash
#!/bin/bash
apt-get update
apt-get install -y docker.io docker-compose-v2 git
usermod -aG docker ubuntu
systemctl enable docker
systemctl start docker

mkdir -p /home/ubuntu/devops-project
cd /home/ubuntu/devops-project
git clone https://github.com/TON_USER/devops-project.git .
docker compose up -d --build
```

Avec ça, tu lances l'EC2 et l'app tourne toute seule en 2-3 minutes — sans te connecter en SSH. C'est exactement ce qu'on automatisera avec Terraform dans le Module 6.

> **Tu n'es pas obligé de refaire l'exercice avec User Data.** C'est juste pour comprendre le concept. Le Module 6 (Terraform) l'utilise automatiquement.

## Coin entretien

### Questions fondamentales

**Q : C'est quoi AWS ?**
R : Un fournisseur de cloud computing. Tu loues des serveurs (EC2), du stockage (S3), des bases de données (RDS) et plein d'autres services, à la demande.

**Q : C'est quoi EC2 ?**
R : Elastic Compute Cloud — un serveur virtuel dans le cloud. Tu choisis la puissance, l'OS, et tu paies à l'heure.

**Q : C'est quoi un VPC ?**
R : Virtual Private Cloud — un réseau isolé dans AWS. Tu y mets tes ressources (EC2, RDS). Tu contrôles les subnets, le routage, et les accès.

**Q : Différence entre subnet public et privé ?**
R : Public = accessible depuis Internet (via Internet Gateway). Privé = pas d'accès direct depuis Internet. On met les serveurs web en public, les bases de données en privé.

**Q : C'est quoi IAM ?**
R : Identity and Access Management — le système de permissions d'AWS. Users, roles, policies. Principe du moindre privilège : on ne donne que les droits nécessaires.

**Q : C'est quoi un Security Group ?**
R : Un firewall virtuel pour les instances EC2. Il contrôle le traffic entrant et sortant par port et par IP source.

**Q : C'est quoi S3 ?**
R : Simple Storage Service — stockage d'objets (fichiers) illimité, haute durabilité. Utilisé pour les backups, static files, logs, etc.

### Questions bases de données

**Q : C'est quoi RDS ?**
R : Relational Database Service — une base de données managée par AWS. Tu choisis le moteur (PostgreSQL, MySQL...), AWS gère les backups, updates, et high availability.

**Q : Pourquoi utiliser RDS plutôt qu'installer PostgreSQL sur un EC2 ?**
R : RDS gère les backups, security updates, replication, et high availability automatiquement. Moins de travail opérationnel. En contrepartie, c'est un peu plus cher et tu as moins de contrôle.

**Q : C'est quoi DynamoDB ?**
R : Une base de données NoSQL managée par AWS. Au lieu de tableaux SQL avec des colonnes fixes, tu stockes des documents JSON flexibles. Le scaling est automatique et le prix est à la requête.

**Q : Quand utiliser RDS vs DynamoDB ?**
R : RDS quand tes données ont des relations entre elles (users → commandes → produits) et que tu as besoin de requêtes SQL complexes. DynamoDB quand tu as des données simples à très fort traffic (sessions, cache, compteurs). En cas de doute, RDS — c'est plus polyvalent.

### Questions containers et compute

**Q : C'est quoi ECS ?**
R : Elastic Container Service — tu donnes tes images Docker à AWS, et il les lance, les surveille et les scale. Avec Fargate, tu n'as même pas de serveur à gérer — tu paies uniquement le CPU et la RAM utilisés.

**Q : C'est quoi EKS ?**
R : Elastic Kubernetes Service — Kubernetes managé sur AWS. AWS gère le control plane, toi tu gères les workers. L'avantage par rapport à ECS : K8s est un standard, ton setup est portable sur n'importe quel cloud (GKE, AKS).

**Q : ECS vs EKS, tu choisirais quoi ?**
R : ECS si je reste sur AWS et que je veux quelque chose de simple et pas cher. EKS si j'ai besoin de portabilité multi-cloud ou que l'équipe connaît déjà Kubernetes. EKS a un coût fixe pour le control plane (~75$/mois), ECS non.

**Q : C'est quoi Lambda ?**
R : Du serverless — tu envoies ton code, AWS l'exécute quand il faut, tu paies à l'exécution. Pas de serveur à gérer. Idéal pour des tâches courtes et ponctuelles.

**Q : Quand utiliser Lambda vs EC2 vs ECS ?**
R : Lambda pour les tâches courtes (<15 min) et ponctuelles. ECS/EKS pour des apps containerisées qui tournent en continu avec du scaling automatique. EC2 quand tu as besoin de contrôle total sur le serveur ou pour des petits projets simples.

**Q : C'est quoi un cold start ?**
R : La première exécution d'une Lambda est plus lente parce qu'AWS doit démarrer un environnement. Les exécutions suivantes (warm start) sont plus rapides.

**Q : Différence entre scaling horizontal et vertical ?**
R : Vertical = augmenter la puissance d'une machine (plus de CPU, plus de RAM). Horizontal = ajouter plus de machines. Le vertical a une limite physique, le horizontal est quasi illimité. En cloud, on privilégie le scaling horizontal.

**Q : C'est quoi le modèle de responsabilité partagée ?**
R : AWS gère la sécurité **du** cloud (datacenters, réseau physique, hyperviseurs). Toi tu gères la sécurité **dans** le cloud (tes données, tes Security Groups, tes IAM policies, ton code). Si ton Security Group est ouvert à tout le monde, c'est ta faute, pas celle d'AWS.

> **Exercices system design :** Pour t'entraîner à répondre aux questions de type "comment tu déploierais cette app ?", va voir les [5 exercices de system design](system-design-exercises.md). C'est le genre de question qu'on te posera en entretien DevOps.

## Bonnes pratiques

- **Moindre privilège (IAM).** Ne donne jamais `AdministratorAccess` en prod. Crée des policies qui autorisent uniquement ce dont l'user/role a besoin. C'est contraignant mais c'est ce qui empêche un hack de devenir une catastrophe.
- **Jamais le compte root.** Le compte root peut tout faire, y compris supprimer le compte AWS. Crée un user IAM pour ton usage quotidien. Active le MFA (authentification multi-facteurs) sur le root.
- **DB en subnet privé.** Toujours. Une base de données exposée sur Internet, c'est un ransomware qui attend d'arriver.
- **Alerte de facturation.** Configure une alerte Budget dès le jour 1. Des gens ont eu des factures de 10 000€ pour un NAT Gateway oublié.
- **Tague tes ressources.** `Name`, `Environment` (dev/staging/prod), `Project`. Quand tu as 50 ressources, c'est la seule façon de savoir à quoi elles servent et si tu peux les supprimer.
- **Une région, un choix.** Choisis ta région (eu-west-3 = Paris) et restes-y. Les ressources ne sont pas visibles entre régions, ça crée de la confusion.

## Erreurs courantes

- **Laisser des instances tourner** → Coût inattendu. Toujours `terminate` quand tu as fini.
- **Utiliser le compte root** → Mauvaise pratique. Crée un user IAM.
- **Security Group trop ouvert (0.0.0.0/0 sur tout)** → N'importe qui peut accéder. N'ouvre que les ports nécessaires.
- **Oublier de mettre une IP publique** → Tu ne pourras pas accéder à ton instance depuis Internet.
- **Choisir la mauvaise région** → Tes ressources sont dans une région. Si tu cherches et ne trouves pas → vérifie la région en haut à droite.
- **RDS en accès public** → Ne jamais exposer une base de données sur Internet. Toujours en subnet privé, accessible uniquement depuis ton EC2/VPC.
- **Oublier de supprimer l'instance RDS** → Même en Free Tier, ça coûte si tu dépasses 750h/mois.
- **Lambda timeout trop court** → Par défaut 3s. Si ta fonction fait un appel API externe, augmente le timeout.

## Pour aller plus loin

- **CloudWatch** : monitoring et logs centralisés sur AWS — tu l'utiliseras dès ton premier déploiement
- **SQS / SNS** : files d'attente et notifications — pattern très courant pour découpler les services
- **API Gateway** : créer des APIs complètes devant Lambda (auth, rate limiting, versioning)
- **AWS Well-Architected Framework** : les bonnes pratiques d'architecture cloud — utile pour les entretiens system design
- **Les autres clouds** : GCP (Google), Azure (Microsoft) — mêmes concepts, noms différents

## Tu peux passer au module suivant si...

- [ ] Tu as un compte AWS avec une alerte de facturation configurée
- [ ] Tu sais ce que sont EC2, S3, VPC, RDS, IAM, DynamoDB, ECS et EKS (en une phrase chacun)
- [ ] Tu sais lancer une instance EC2 et t'y connecter en SSH
- [ ] Tu comprends la différence entre subnet public et privé
- [ ] Tu sais ce qu'est un Security Group (firewall AWS)
- [ ] Le projet fil rouge tourne sur un EC2 accessible depuis ton navigateur
- [ ] Tu as bien terminé/supprimé toutes les ressources AWS pour éviter les coûts
