# Module 5 : AWS

> **Prérequis :** Module 2 (Réseau — IP, ports, subnets), Module 3 (Docker — pour déployer l'app)

> **En résumé :** Tu découvres le cloud en déployant ton application sur un vrai serveur AWS. Tu apprends les services fondamentaux (EC2, S3, VPC, RDS, IAM) que tu automatiseras ensuite avec Terraform dans le module suivant.

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
- **EC2** : 750h/mois de t2.micro (1 instance 24/7 = OK)
- **S3** : 5 Go de stockage
- **RDS** : 750h/mois de db.t3.micro
- **Lambda** : 1 million de requêtes/mois gratuites (largement suffisant pour apprendre)
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

```bash
# Dans la console AWS :
# IAM → Users → Create User → Nom: "admin-dev"
# Attach policy: "AdministratorAccess" (pour le cours, pas pour la prod !)
# Security credentials → Create access key → CLI
# Note l'Access Key ID et le Secret Access Key
```

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
| **Instance type** | La puissance (t2.micro = gratuit, petit) |
| **Key pair** | Clé SSH pour te connecter |
| **Security group** | Firewall de l'instance |

### Lancer une instance (console)

1. **EC2** → **Launch Instance**
2. Name: `devops-server`
3. AMI: **Ubuntu Server 24.04 LTS**
4. Instance type: **t2.micro** (Free Tier)
5. Key pair: **Create new** → `devops-key` → Download `.pem`
6. Security group: autoriser **SSH (22)**, **HTTP (80)**, **port 8000**
7. **Launch**

### Se connecter

```bash
# Rendre la clé utilisable
chmod 400 ~/devops-key.pem

# Se connecter
ssh -i ~/devops-key.pem ubuntu@IP_PUBLIQUE_DE_TON_INSTANCE
# Welcome to Ubuntu...
```

### User Data — Script de démarrage automatique

Quand tu lances un EC2, tu peux lui donner un **user_data** : un script bash qui s'exécute automatiquement au premier démarrage du serveur. C'est comme laisser une note au livreur : "quand tu arrives, installe Docker et lance l'app".

```bash
#!/bin/bash
apt-get update
apt-get install -y docker.io
systemctl start docker
```

Tu peux le coller dans le champ **User data** (étape "Advanced details" lors du lancement EC2). On l'utilisera dans le Module 6 (Terraform) pour automatiser complètement le setup du serveur.

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

En pratique pour le cours : un VPC avec un subnet public suffit (on ajoutera un subnet privé pour RDS si besoin).

## RDS — Base de données managée

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

### Créer une instance RDS (console)

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

### Se connecter depuis EC2

```bash
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

⚠️ **N'oublie pas de supprimer l'instance RDS quand tu as fini** — même en Free Tier, si tu dépasses 750h/mois, ça coûte.

> **Note :** Dans le projet pratique ci-dessous, on n'utilise pas RDS — le backend utilise PostgreSQL dans un container Docker sur l'EC2 (comme dans le Module 3). En production, on utiliserait RDS pour les backups automatiques et la haute disponibilité, mais pour apprendre, Docker Compose sur un EC2 suffit largement.

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
| Cas d'usage | Webhooks, tâches ponctuelles | Apps qui tournent 24/7 |

Pour créer et tester une Lambda, voir la [documentation AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html).

## Autres services AWS à connaître

Ces services ne sont pas utilisés dans le projet fil rouge, mais tu les croiseras en entretien et en entreprise. Comprendre ce qu'ils font et **quand les utiliser** est essentiel.

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

Si tu as fait le Module 8 (Kubernetes), tu connais déjà K8s avec minikube en local. **EKS** (Elastic Kubernetes Service) = la même chose, mais sur AWS. AWS gère le control plane (le cerveau du cluster K8s), toi tu gères les workers (les machines qui font tourner tes pods).

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
- Type: t2.micro
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

### Exercice system design : "Déploie-moi cette app"

> Ce type de question est **très courant en entretien DevOps**. On te donne un projet et on te demande comment tu le déploierais. Il n'y a pas de réponse parfaite — ce qui compte c'est ta façon de raisonner.

**L'énoncé :**

> « Une startup lance une app de livraison de repas. Ils ont un frontend React, une API backend en Python, et une base PostgreSQL. Aujourd'hui ils ont 500 utilisateurs, mais ils espèrent passer à 50 000 dans 6 mois. L'API reçoit aussi des webhooks de paiement Stripe qui ne doivent jamais être perdus. Comment tu déploierais ça sur AWS ? »

---

**Étape 1 — Comment aborder le problème (ta méthode)**

En entretien, ne fonce pas directement sur la solution. Pose des questions et structure ta réflexion :

1. **Clarifie les contraintes** — Quel budget ? Quelle taille d'équipe DevOps ? Y a-t-il déjà de l'infra existante ? Quel est le SLA attendu (99.9% ? 99.99%) ?
2. **Identifie les composants** — Frontend, backend API, base de données, webhooks Stripe
3. **Identifie les points critiques** — Scaling de 500 à 50 000 users, les webhooks qui ne doivent pas être perdus
4. **Propose une solution simple d'abord**, puis fais évoluer

---

**Étape 2 — La solution proposée**

```
                    ┌─────────────────────┐
                    │     CloudFront       │  ← CDN (cache le frontend partout dans le monde)
                    │     + S3 bucket      │  ← Le frontend React (fichiers statiques)
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │   Load Balancer      │  ← Répartit le traffic entre les containers
                    │   (ALB)              │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │   ECS Fargate        │  ← Backend API (auto-scaling)
                    │   2 → N containers   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                 │
    ┌─────────┴───────┐ ┌─────┴──────┐  ┌──────┴──────┐
    │  RDS PostgreSQL  │ │  SQS Queue │  │  Lambda     │
    │  (Multi-AZ)      │ │  (webhooks)│  │  (traite    │
    │  subnet privé    │ │            │──│  les webhooks)│
    └─────────────────┘ └────────────┘  └─────────────┘
```

**Pourquoi ces choix :**

| Composant | Choix | Pourquoi |
|-----------|-------|----------|
| Frontend | **S3 + CloudFront** | Le frontend React = des fichiers statiques (HTML/JS/CSS). Pas besoin d'un serveur pour ça. S3 héberge les fichiers, CloudFront les distribue partout dans le monde rapidement (CDN) |
| Backend API | **ECS Fargate** | L'API doit scaler de 500 à 50 000 users. Fargate scale automatiquement les containers sans gérer de serveurs. On démarre avec 2 containers et ça monte tout seul |
| Base de données | **RDS Multi-AZ** | Les données de commandes/users sont relationnelles → PostgreSQL. Multi-AZ pour que la base ne tombe pas si un datacenter a un problème |
| Webhooks Stripe | **SQS + Lambda** | Les webhooks ne doivent **jamais** être perdus. Si l'API plante au moment du webhook, c'est perdu. Avec SQS (une file d'attente), le webhook est stocké dans la file, et une Lambda le traite ensuite. Si la Lambda échoue, le message reste dans la file et est re-traité |
| Load Balancer | **ALB** | Répartit le traffic entre les containers ECS. Fait aussi health check — si un container crash, le traffic va sur les autres |

---

**Étape 3 — Les alternatives et pourquoi on ne les a pas choisies**

| Alternative | Pourquoi on ne l'a pas choisie |
|-------------|-------------------------------|
| **Docker sur un EC2** | Marche pour 500 users mais ne scale pas automatiquement. À 50 000 users, il faudrait tout refaire |
| **EKS au lieu d'ECS** | Plus flexible et portable, mais plus complexe et plus cher (~75$/mois de base). La startup n'a pas besoin de portabilité multi-cloud pour l'instant |
| **Lambda pour l'API** (tout serverless) | Possible mais les cold starts ajoutent de la latence. Pour une API qui tourne en continu avec beaucoup de traffic, ECS est plus prévisible |
| **DynamoDB au lieu de RDS** | Les données de l'app (users, commandes, restaurants, menus) sont très relationnelles. DynamoDB serait plus dur à requêter pour ces cas |
| **Frontend sur un EC2/ECS avec nginx** | Surcoût inutile — des fichiers statiques n'ont pas besoin d'un serveur. S3 + CloudFront coûte quasiment rien et scale à l'infini |

---

**Étape 4 — Comment présenter ça en entretien**

1. **Commence simple** : "Pour 500 users, honnêtement un EC2 avec Docker Compose suffirait"
2. **Montre que tu penses au futur** : "Mais comme ils visent 50 000, je partirais directement sur ECS Fargate pour ne pas avoir à tout refaire"
3. **Justifie chaque choix** par rapport au besoin, pas par rapport à la techno
4. **Mentionne ce que tu n'as pas choisi** et pourquoi — ça montre que tu connais les alternatives
5. **Parle des risques** : "Le point critique c'est les webhooks Stripe — je mettrais une SQS devant pour ne jamais en perdre"

> **Le piège à éviter :** ne pas sur-engineer. Si l'interviewer te dit "startup de 3 personnes, budget serré", ne propose pas EKS + multi-region + DynamoDB. La bonne réponse est celle qui **colle au besoin**, pas celle qui utilise le plus de services.

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

- **Certifications AWS** : Solutions Architect Associate (SAA-C03), la plus demandée
- **API Gateway** : créer des APIs complètes devant Lambda (auth, rate limiting, versioning)
- **CloudFormation** : IaC natif AWS (comme Terraform mais spécifique AWS)
- **SQS / SNS** : files d'attente et notifications — essentiels pour les architectures découplées
- **CloudWatch** : monitoring et logs centralisés sur AWS
- **Les autres clouds** : GCP (Google), Azure (Microsoft) — mêmes concepts, noms différents
- **AWS Well-Architected Framework** : les bonnes pratiques d'architecture cloud

## Tu peux passer au module suivant si...

- [ ] Tu as un compte AWS avec une alerte de facturation configurée
- [ ] Tu sais ce que sont EC2, S3, VPC, RDS, IAM, DynamoDB, ECS et EKS (en une phrase chacun)
- [ ] Tu sais lancer une instance EC2 et t'y connecter en SSH
- [ ] Tu comprends la différence entre subnet public et privé
- [ ] Tu sais ce qu'est un Security Group (firewall AWS)
- [ ] Le projet fil rouge tourne sur un EC2 accessible depuis ton navigateur
- [ ] Tu as bien terminé/supprimé toutes les ressources AWS pour éviter les coûts
