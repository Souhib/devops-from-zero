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

**Q : C'est quoi RDS ?**
R : Relational Database Service — une base de données managée par AWS. Tu choisis le moteur (PostgreSQL, MySQL...), AWS gère les backups, updates, et high availability.

**Q : Pourquoi utiliser RDS plutôt qu'installer PostgreSQL sur un EC2 ?**
R : RDS gère les backups, security updates, replication, et high availability automatiquement. Moins de travail opérationnel. En contrepartie, c'est un peu plus cher et tu as moins de contrôle.

**Q : C'est quoi Lambda ?**
R : Du serverless — tu envoies ton code, AWS l'exécute quand il faut, tu paies à l'exécution. Pas de serveur à gérer. Idéal pour des tâches courtes et ponctuelles.

**Q : Quand utiliser Lambda vs EC2 ?**
R : Lambda pour les tâches courtes (<15 min), ponctuelles, avec du scaling automatique. EC2 pour les applications longues, les serveurs web qui tournent 24/7, ou quand tu as besoin de contrôle total.

**Q : C'est quoi un cold start ?**
R : La première exécution d'une Lambda est plus lente parce qu'AWS doit démarrer un environnement. Les exécutions suivantes (warm start) sont plus rapides.

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
- **ECS / Fargate** : faire tourner des containers Docker sur AWS sans gérer de serveurs (entre EC2 et Lambda)
- **API Gateway** : créer des APIs complètes devant Lambda (auth, rate limiting, versioning)
- **CloudFormation** : IaC natif AWS (comme Terraform mais spécifique AWS)
- **Les autres clouds** : GCP (Google), Azure (Microsoft) — mêmes concepts, noms différents
- **AWS Well-Architected Framework** : les bonnes pratiques d'architecture cloud

## Tu peux passer au module suivant si...

- [ ] Tu as un compte AWS avec une alerte de facturation configurée
- [ ] Tu sais ce que sont EC2, S3, VPC, RDS et IAM (en une phrase chacun)
- [ ] Tu sais lancer une instance EC2 et t'y connecter en SSH
- [ ] Tu comprends la différence entre subnet public et privé
- [ ] Tu sais ce qu'est un Security Group (firewall AWS)
- [ ] Le projet fil rouge tourne sur un EC2 accessible depuis ton navigateur
- [ ] Tu as bien terminé/supprimé toutes les ressources AWS pour éviter les coûts
