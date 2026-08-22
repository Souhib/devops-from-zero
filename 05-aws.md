# Module 5 : AWS

> **Prérequis :** [Module 2](02-networking.md) (Réseau — IP, ports, subnets), [Module 3](03-docker.md) (Docker — pour déployer l'app)

> **En résumé :** Tu découvres le cloud en construisant une infrastructure AWS (VPC + EC2 + IAM) et en **pratiquant** les grands services (S3, SQS, RDS, DynamoDB, Lambda...). Tout se fait d'abord **en local et gratuitement**, sur un émulateur AWS — puis tu déploies **une fois** sur un vrai compte AWS, pour l'avoir fait en vrai et pouvoir en parler en entretien.

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

## Comment on va travailler : deux pistes

Il y a un vrai obstacle quand on apprend AWS : **pour créer un compte, il faut donner une carte bancaire.** Et une fois le compte créé, on n'ose plus rien essayer de peur de la facture. Résultat : on lit, on ne pratique pas.

On contourne le problème avec **deux pistes complémentaires**.

| | **Piste A — En local** | **Piste B — Le vrai AWS** |
|---|---|---|
| **Avec quoi** | Un émulateur AWS sur ta machine ([Floci](floci-aws-local.md)) | Un vrai compte sur [aws.amazon.com](https://aws.amazon.com) |
| **Carte bancaire** | Non | Oui |
| **Coût** | 0 € | 0 € si tu restes dans le Free Tier |
| **Tu peux te tromper ?** | Autant de fois que tu veux | Il faut faire attention |
| **Quand** | Pendant tout le module, pour **tous** les exercices | **Une seule fois**, à la fin, pour le déploiement final |
| **Ce que ça t'apporte** | La pratique, les réflexes, les commandes | L'expérience réelle, la console, une vraie app en ligne |

**Concrètement :** tu fais tous les exercices de ce module en Piste A, tranquillement. Puis, à la fin, tu refais **une fois** le déploiement complet en Piste B.

> **Pourquoi ne pas rester en local tout du long ?** Parce qu'un émulateur ne t'apprend ni la console web, ni les vraies erreurs de permissions, ni le raisonnement sur les coûts. Et parce qu'en entretien, « j'ai déployé une app sur AWS » et « j'ai déployé une app sur un émulateur » ne pèsent pas pareil. Les deux pistes se complètent, aucune ne remplace l'autre.

### Piste A — Mettre en place l'AWS local

Une seule commande, et tu peux commencer :

```bash
cd ~/devops-project/floci
docker compose up -d

# Vérifier (doit afficher 200)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4566/health
```

Puis configure le raccourci `awslocal` en suivant **[le guide AWS en local](floci-aws-local.md)**. C'est une manipulation à faire **une seule fois** — prends les 10 minutes, tout le reste du module en dépend.

Dans la suite de ce module, chaque fois que tu vois un encadré **🧪 Pratique**, c'est un exercice à faire en Piste A.

### Piste B — Créer ton compte AWS

À faire quand tu arriveras au [projet pratique](#projet-pratique--déployer-le-projet-sur-aws), pas avant.

1. Va sur [aws.amazon.com](https://aws.amazon.com) et crée un compte
2. Tu auras besoin d'une carte bancaire (mais le Free Tier est gratuit pendant 12 mois)

⚠️ **IMPORTANT — Les limites du Free Tier :**
- **EC2** : 750h/mois de t3.micro (1 instance 24/7 = OK)
- **S3** : 5 Go de stockage
- **RDS** : 750h/mois de db.t3.micro
- **Lambda** : 1 million de requêtes/mois gratuites (largement suffisant pour apprendre)
- Pour le projet de ce cursus, tu n'utilises que **EC2** (750h/mois = 1 instance 24/7).
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

### 🧪 Pratique : créer un user et une policy

> Piste A — [Floci démarré](floci-aws-local.md) et alias `awslocal` configuré.

```bash
# Créer un utilisateur
awslocal iam create-user --user-name stagiaire

# Écrire une policy : "le droit de LIRE dans S3, rien d'autre"
cat > lecture-s3.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": "*"
    }
  ]
}
EOF

# Créer la policy à partir de ce fichier
awslocal iam create-policy --policy-name LectureSeuleS3 --policy-document file://lecture-s3.json

# L'attacher à l'utilisateur
awslocal iam attach-user-policy \
  --user-name stagiaire \
  --policy-arn arn:aws:iam::000000000000:policy/LectureSeuleS3

# Vérifier
awslocal iam list-attached-user-policies --user-name stagiaire
```

**Lis le JSON, c'est là que tout se joue :**

| Champ | Ce qu'il veut dire |
|---|---|
| `Effect` | `Allow` (autoriser) ou `Deny` (interdire) |
| `Action` | Les opérations concernées. `s3:GetObject` = télécharger un fichier. Le `*` marche aussi : `s3:*` = toutes les actions S3 |
| `Resource` | Sur QUOI ça s'applique. `*` = tout. En vrai on met un ARN précis, ex. `arn:aws:s3:::mon-bucket/*` |

**Un ARN**, c'est l'identifiant unique d'une ressource AWS. Structure : `arn:aws:service:région:compte:ressource`. Ici `000000000000` est le numéro de compte factice utilisé par l'émulateur.

> ⚠️ **Limite importante à connaître.** L'émulateur **crée** les users et les policies, mais il ne les **applique pas** : il accepte n'importe quels identifiants et n'interdit jamais rien. Tu apprends donc la *syntaxe* IAM, pas son *effet*. Les vraies erreurs `AccessDenied`, tu ne les verras qu'en Piste B. C'est la limite la plus importante de la Piste A — ne l'oublie pas.

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

> 🧪 **L'exercice EC2 arrive un peu plus bas**, après la section VPC — parce qu'un serveur doit être posé dans un réseau. Lis d'abord cette section et celle du VPC, puis va faire [l'exercice complet](#-pratique--construire-un-réseau-et-y-lancer-un-serveur).

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

### 🧪 Pratique : S3 pour de vrai

> Piste A. Remplace simplement `aws` par `awslocal` dans les commandes ci-dessus.

```bash
# Créer un bucket
awslocal s3 mb s3://mon-bucket-perso

# Y déposer un fichier
echo "Bonjour depuis le cloud" > note.txt
awslocal s3 cp note.txt s3://mon-bucket-perso/

# Lister le contenu
awslocal s3 ls s3://mon-bucket-perso/

# Le retélécharger
awslocal s3 cp s3://mon-bucket-perso/note.txt recu.txt && cat recu.txt

# Générer une URL de téléchargement temporaire (valable 1h)
awslocal s3 presign s3://mon-bucket-perso/note.txt --expires-in 3600
```

**L'URL présignée, c'est quoi et pourquoi c'est utile ?** Ton bucket est privé : personne ne peut y accéder. Mais tu veux parfois laisser **un** utilisateur télécharger **un** fichier précis, pendant **un temps limité** — par exemple sa facture PDF. Plutôt que de rendre le bucket public (dangereux) ou de faire transiter le fichier par ton serveur (lent et coûteux), tu génères une URL signée qui expire toute seule.

```bash
# Teste-la : elle marche sans aucun identifiant
curl "$(awslocal s3 presign s3://mon-bucket-perso/note.txt)"
# Bonjour depuis le cloud
```

C'est un pattern qu'on te demandera en entretien : *« comment tu permets à un utilisateur de télécharger un fichier privé ? »*

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

> Les concepts de subnets et CIDR viennent du [Module 2](02-networking.md) (Réseau). Les Security Groups fonctionnent comme les firewalls vus au [Module 2](02-networking.md) (`ufw`).

**Ce qu'il faut retenir :**
- L'EC2 est dans le subnet **public** → il a une IP publique, accessible depuis Internet
- La base RDS est dans le subnet **privé** → pas d'IP publique, accessible uniquement depuis le VPC
- Les Security Groups filtrent le traffic : le RDS n'accepte que le port 5432 venant de l'EC2
- L'Internet Gateway connecte le subnet public à Internet

**Pour le projet de ce cursus : un VPC avec un seul subnet public suffit.** Le schéma ci-dessus avec un subnet privé + RDS, c'est pour te montrer comment ça fonctionne en production — tu n'as pas besoin de le créer.

### 🧪 Pratique : construire un réseau et y lancer un serveur

> Piste A. C'est l'exercice le plus complet du module : tu vas créer un réseau, un pare-feu, puis un serveur, et **entrer dedans en SSH**. Compte 15 minutes.

#### 1. Le réseau

```bash
# Créer le VPC et garder son identifiant dans une variable
VPC=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
echo "Mon VPC : $VPC"

# Un subnet dedans
SUBNET=$(awslocal ec2 create-subnet --vpc-id $VPC --cidr-block 10.0.1.0/24 --query 'Subnet.SubnetId' --output text)
echo "Mon subnet : $SUBNET"
```

> **`VPC=$(...)`, c'est quoi ?** C'est du bash : `$( )` exécute la commande et **récupère son résultat** dans une variable, au lieu de l'afficher. Ça évite de recopier à la main des identifiants comme `vpc-909faca6`. `--query` et `--output text` servent à ne garder que l'identifiant, sans le JSON autour.

#### 2. Le pare-feu (Security Group)

```bash
SG=$(awslocal ec2 create-security-group \
  --group-name mon-serveur-sg \
  --description "Pare-feu de mon serveur" \
  --vpc-id $VPC \
  --query 'GroupId' --output text)

# Autoriser le SSH (port 22) depuis n'importe où
awslocal ec2 authorize-security-group-ingress \
  --group-id $SG --protocol tcp --port 22 --cidr 0.0.0.0/0
```

**`--cidr 0.0.0.0/0` veut dire « depuis n'importe quelle adresse IP au monde ».** Pratique pour apprendre, mais en production on restreint à son IP (`--cidr 82.65.12.34/32`). C'est un classique en entretien : *« pourquoi c'est risqué d'ouvrir le SSH à 0.0.0.0/0 ? »* — parce que ton serveur se fait alors scanner et attaquer en continu par des robots.

#### 3. La clé SSH

```bash
# Générer une paire de clés sur ta machine
ssh-keygen -t rsa -b 2048 -f ~/devops-key -N ""

# Donner la clé PUBLIQUE à AWS
awslocal ec2 import-key-pair \
  --key-name devops-key \
  --public-key-material fileb://~/devops-key.pub

chmod 400 ~/devops-key
```

> ⚠️ **`import-key-pair`, pas `create-key-pair`.** `create-key-pair` demande à AWS de générer la clé — mais l'émulateur renvoie alors une fausse clé privée avec laquelle tu ne pourras pas te connecter. On génère donc la clé nous-même et on donne la partie publique. (Rappel du [Module 1](01-linux-basics.md) : la clé **privée** ne quitte jamais ta machine, la clé **publique** se distribue.)

#### 4. Le serveur

```bash
# Un script exécuté automatiquement au premier démarrage du serveur
cat > userdata.sh <<'EOF'
#!/bin/bash
mkdir -p /run/sshd
/usr/sbin/sshd
EOF

INSTANCE=$(awslocal ec2 run-instances \
  --image-id ami-ubuntu2404-amd64 \
  --instance-type t3.micro \
  --key-name devops-key \
  --subnet-id $SUBNET \
  --security-group-ids $SG \
  --user-data file://userdata.sh \
  --count 1 \
  --query 'Instances[0].InstanceId' --output text)

echo "Mon serveur : $INSTANCE"
```

> **Sur un Mac Apple Silicon (M1/M2/M3/M4)**, remplace par `--image-id ami-ubuntu2404-arm64 --instance-type t4g.micro`. Les types `t3` sont des processeurs Intel, les `t4g` des processeurs ARM (Graviton) — et une image doit correspondre au processeur. L'émulateur refuse le mélange, **exactement comme le vrai AWS**.

**Le `--user-data`, c'est quoi ?** Un script que le serveur exécute tout seul à son tout premier démarrage. C'est LA façon standard d'automatiser l'installation d'un serveur neuf. Ici il crée un dossier dont le serveur SSH a besoin pour démarrer (l'image Ubuntu de l'émulateur ne le fournit pas).

#### 5. Attendre, puis se connecter

```bash
# Suivre l'état
awslocal ec2 describe-instances --instance-ids $INSTANCE \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]' --output table
```

⚠️ **`running` ne veut PAS dire « prêt ».** Le serveur est allumé, mais il installe encore son serveur SSH — ça prend une bonne minute. C'est le même comportement que sur le vrai AWS : entre l'état `running` et le moment où le SSH répond, il s'écoule toujours un moment.

```bash
# Trouver sur quel port de ta machine le SSH du serveur est accessible
PORT=$(docker ps --filter "name=floci-ec2-$INSTANCE" --format '{{.Ports}}' \
       | sed -n 's/.*:\([0-9]*\)->22\/tcp.*/\1/p')
echo "Port SSH : $PORT"     # 2200 pour la première instance, 2201 pour la suivante...

# Se connecter (réessaie si ça dit "Connection closed", c'est que ce n'est pas encore prêt)
ssh -i ~/devops-key -p $PORT root@127.0.0.1
```

> **Deux différences avec le vrai AWS, à bien avoir en tête :**
>
> | | Piste A (émulateur) | Piste B (vrai AWS) |
> |---|---|---|
> | Utilisateur | `root` | `ubuntu` (sur une AMI Ubuntu) |
> | Adresse et port | `127.0.0.1` sur le port 2200+ | l'IP publique, sur le port 22 |
>
> Pourquoi ? Parce que ton « serveur » est en réalité un container sur ta machine. Il n'a pas d'IP publique sur Internet : l'émulateur redirige un port local vers son port 22.

#### 6. Une fois connecté

```bash
# Tu es sur le serveur. Vérifie :
hostname
cat /etc/os-release | head -2

# L'IMDS : le service qui permet à une instance de savoir "qui suis-je"
curl -s http://169.254.169.254/latest/meta-data/instance-id
# i-040d1ec4b5bb76c6a
```

**L'adresse `169.254.169.254` est à connaître par cœur.** C'est une adresse spéciale, identique sur toutes les instances EC2 du monde, qui répond depuis l'intérieur de l'instance. Elle sert surtout à une chose essentielle : **fournir automatiquement les identifiants du rôle IAM de l'instance**. C'est comme ça qu'une application sur EC2 accède à S3 sans qu'aucun mot de passe ne soit écrit nulle part. C'est la bonne réponse à la question d'entretien *« comment tu gères les secrets AWS sur un serveur ? »*.

#### 7. Nettoyer

```bash
exit   # sortir du serveur

awslocal ec2 terminate-instances --instance-ids $INSTANCE
```

> **Prends l'habitude de nettoyer, même en local.** En Piste B, oublier une instance allumée, c'est une facture à la fin du mois.

## RDS — Base de données managée

> **Tu n'as PAS besoin de créer un RDS pour le projet.** Le backend utilise PostgreSQL dans un container Docker sur l'EC2 (comme dans le [Module 3](03-docker.md)). Cette section est là pour comprendre ce que c'est et quand l'utiliser en production.

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

### 🧪 Pratique : créer une base et s'y connecter

> Piste A. L'émulateur démarre un **vrai PostgreSQL** — ce n'est pas une imitation.

```bash
awslocal rds create-db-instance \
  --db-instance-identifier ma-base \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password MonMotDePasse123 \
  --allocated-storage 20

# Attendre que le statut passe à "available" (quelques secondes)
awslocal rds describe-db-instances --db-instance-identifier ma-base \
  --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address,Endpoint.Port]' --output table
```

**L'endpoint**, c'est l'adresse de la base. Sur le vrai AWS ça ressemble à `ma-base.c9x.eu-west-3.rds.amazonaws.com`, et c'est ce que tu mets dans ton `DATABASE_URL`.

```bash
# Se connecter (installe psql si besoin : sudo apt install -y postgresql-client)
psql -h localhost -p 7001 -U postgres
# Password: MonMotDePasse123

# Une fois dedans :
#   SELECT version();
#   CREATE TABLE test (id SERIAL PRIMARY KEY, nom TEXT);
#   INSERT INTO test (nom) VALUES ('ça marche');
#   SELECT * FROM test;
#   \q     ← pour quitter
```

> ⚠️ **Le piège de l'adresse.** `describe-db-instances` renvoie une adresse du type `172.25.0.3` : c'est une adresse **interne à Docker**, qui ne veut rien dire depuis ta machine. Depuis ton terminal, connecte-toi toujours à **`localhost`**, en gardant **le port** indiqué (7001, 7002...).

**Nettoyer :**

```bash
awslocal rds delete-db-instance --db-instance-identifier ma-base --skip-final-snapshot
```

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

### 🧪 Pratique : ta première Lambda

> Piste A. L'émulateur exécute **vraiment** ton code Python.

```bash
mkdir -p ma-lambda && cd ma-lambda

# 1. Le code de la fonction
cat > lambda_function.py <<'EOF'
def lambda_handler(event, context):
    # "event"   = les données reçues (ce qui déclenche la fonction)
    # "context" = des infos sur l'exécution (temps restant, mémoire...)
    nom = event.get("nom", "inconnu")
    return {"statusCode": 200, "message": f"Bonjour {nom} !"}
EOF

# 2. AWS attend le code dans un fichier .zip
zip fonction.zip lambda_function.py

# 3. Créer la fonction
awslocal lambda create-function \
  --function-name ma-fonction \
  --runtime python3.12 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://fonction.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 4. L'exécuter
awslocal lambda invoke \
  --function-name ma-fonction \
  --payload '{"nom":"Souhib"}' \
  --cli-binary-format raw-in-base64-out \
  reponse.json

cat reponse.json
# {"statusCode": 200, "message": "Bonjour Souhib !"}
```

**Le `--handler`, c'est quoi ?** C'est le point d'entrée : `fichier.fonction`. Ici `lambda_function.lambda_handler` veut dire « dans le fichier `lambda_function.py`, appelle la fonction `lambda_handler` ». Si tu te trompes, tu obtiens une erreur `Unable to import module` — c'est l'erreur numéro 1 sur Lambda.

**Ce que tu viens de vivre :** tu as déployé et exécuté du code **sans jamais parler d'un serveur**. Pas de machine à choisir, pas d'OS à mettre à jour, pas de port à ouvrir. C'est exactement ça, le « serverless ».

Documentation complète : [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html).

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

#### 🧪 Pratique : une file d'attente

> Piste A. Tu vas jouer les deux rôles : celui qui dépose le ticket, et le cuisinier qui le prend.

```bash
# Créer la file
awslocal sqs create-queue --queue-name ma-file
# {"QueueUrl": "http://localhost:4566/000000000000/ma-file"}

Q=http://localhost:4566/000000000000/ma-file

# Le serveur dépose un ticket
awslocal sqs send-message --queue-url $Q --message-body "Envoyer la facture 1042"

# Le cuisinier vient chercher un ticket
awslocal sqs receive-message --queue-url $Q
```

Regarde bien la réponse : il y a un champ **`ReceiptHandle`**. C'est le mécanisme le plus important de SQS, et il vaut un point en entretien.

**Recevoir un message ne le supprime pas.** Il devient seulement *invisible* pour les autres consommateurs pendant un certain temps (le *visibility timeout*, 30 secondes par défaut). Tu dois le supprimer **explicitement** une fois le travail terminé :

```bash
RECEIPT=$(awslocal sqs receive-message --queue-url $Q --query 'Messages[0].ReceiptHandle' --output text)
awslocal sqs delete-message --queue-url $Q --receipt-handle "$RECEIPT"
```

**Pourquoi ce fonctionnement bizarre ?** Parce qu'il rend le système résistant aux pannes. Si ton programme crashe **pendant** le traitement, il ne supprime jamais le message : au bout de 30 secondes celui-ci redevient visible, et un autre programme le reprend. **Aucun travail n'est perdu.**

Refais l'expérience : reçois un message, ne le supprime pas, attends 30 secondes, et redemande — il est revenu.

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

#### 🧪 Pratique : une table NoSQL

> Piste A. Compare avec le SQL que tu as fait plus haut sur RDS.

```bash
# Créer une table. On ne déclare QUE la clé — pas les autres colonnes.
awslocal dynamodb create-table \
  --table-name Taches \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Écrire un item
awslocal dynamodb put-item --table-name Taches \
  --item '{"id":{"S":"1"},"titre":{"S":"Apprendre DynamoDB"},"done":{"BOOL":false}}'

# En écrire un autre, avec des champs DIFFÉRENTS — et ça passe !
awslocal dynamodb put-item --table-name Taches \
  --item '{"id":{"S":"2"},"titre":{"S":"Autre tâche"},"priorite":{"N":"3"}}'

# Relire
awslocal dynamodb get-item --table-name Taches --key '{"id":{"S":"1"}}'
```

**Ce que cet exercice te montre, et qu'un tableau ne montrera jamais :**

| | RDS (SQL) | DynamoDB (NoSQL) |
|---|---|---|
| Avant d'écrire | Il faut créer la table **avec toutes ses colonnes** | On déclare **seulement la clé** |
| Deux lignes différentes | Impossible : la structure est imposée | Normal : chaque item a les champs qu'il veut |
| Pour lire | `SELECT ... WHERE ...` sur n'importe quelle colonne | Par la **clé**, principalement |

**`{"S": "1"}`, c'est quoi ce format ?** DynamoDB exige que tu précises le **type** de chaque valeur : `S` = String (texte), `N` = Number, `BOOL` = booléen. C'est verbeux en ligne de commande, mais dans du vrai code les librairies le font pour toi.

**Le vrai piège de DynamoDB, à connaître :** comme on ne peut interroger efficacement que par la clé, **le choix de la clé au départ détermine ce que tu pourras faire ensuite**. Se tromper de clé, c'est devoir tout migrer. Avec SQL, tu ajoutes un index et c'est réglé. C'est la raison principale du conseil « dans le doute, prends du SQL ».

### ECS — Containers managés sur AWS

Dans le [Module 3](03-docker.md), tu as lancé tes containers Docker sur un EC2 avec `docker compose`. Ça marche, mais **c'est toi qui gères le serveur** : les mises à jour, le monitoring, le scaling. Si ton EC2 tombe, ton app tombe.

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

Si tu as fait le [Module 9](09-kubernetes.md) (Kubernetes), tu connais déjà K8s avec minikube en local. **EKS** (Elastic Kubernetes Service) = la même chose, mais sur AWS. AWS gère le control plane (le cerveau du cluster K8s), toi tu gères les workers (les machines qui font tourner tes pods).

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

Tu as vu le DNS dans le [Module 2](02-networking.md) (Réseau) : c'est le système qui traduit un nom de domaine (`monapp.com`) en adresse IP (`13.38.42.100`). **Route 53** c'est le service DNS d'AWS.

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

#### 🧪 Pratique : une zone DNS

> Piste A.

```bash
# Créer la "fiche" du domaine
awslocal route53 create-hosted-zone --name monapp.local --caller-reference $(date +%s)

# Récupérer son identifiant
ZONE=$(awslocal route53 list-hosted-zones --query 'HostedZones[0].Id' --output text)

# Y ajouter un enregistrement A : "monapp.local pointe vers cette IP"
awslocal route53 change-resource-record-sets --hosted-zone-id $ZONE --change-batch '{
  "Changes": [{
    "Action": "CREATE",
    "ResourceRecordSet": {
      "Name": "monapp.local",
      "Type": "A",
      "TTL": 300,
      "ResourceRecords": [{"Value": "13.38.42.100"}]
    }
  }]
}'

# Relire ce qui est enregistré
awslocal route53 list-resource-record-sets --hosted-zone-id $ZONE \
  --query 'ResourceRecordSets[].[Name,Type,ResourceRecords[0].Value]' --output table
```

**`--caller-reference $(date +%s)`** : AWS exige une valeur unique à chaque création, pour éviter de créer deux fois la même zone si tu relances la commande par accident. `date +%s` donne l'heure actuelle en secondes — donc une valeur différente à chaque fois. Ce mécanisme s'appelle l'**idempotence**, et tu le retrouveras partout (voir [Module 7](07-ansible.md)).

### CloudWatch — Le monitoring intégré d'AWS

Dans le [Module 8](08-monitoring.md), tu verras Prometheus + Grafana pour le monitoring. **CloudWatch** c'est l'équivalent natif d'AWS — il est déjà activé par défaut sur tous tes services AWS, sans rien installer.

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

#### 🧪 Pratique : centraliser des logs

> Piste A.

```bash
# Un "log group" = un dossier de logs (en général : une application)
awslocal logs create-log-group --log-group-name /mon-app/backend

# Un "log stream" = une source dans ce dossier (en général : une instance)
awslocal logs create-log-stream \
  --log-group-name /mon-app/backend --log-stream-name serveur-1

# Envoyer une ligne de log
awslocal logs put-log-events \
  --log-group-name /mon-app/backend \
  --log-stream-name serveur-1 \
  --log-events timestamp=$(($(date +%s) * 1000)),message="Démarrage de l'API"

# Relire
awslocal logs get-log-events \
  --log-group-name /mon-app/backend --log-stream-name serveur-1 \
  --query 'events[].message' --output text
```

**Pourquoi centraliser les logs ?** Avec un seul serveur, `docker logs` suffit. Avec dix serveurs, chercher une erreur devient impossible : il faudrait se connecter partout. En centralisant, tous les logs arrivent au même endroit et deviennent **cherchables**. Et surtout : quand un serveur meurt, ses logs locaux disparaissent avec lui — pas ceux qui ont été envoyés.

C'est le pilier « logs » de l'observabilité, que tu retrouveras au [Module 8](08-monitoring.md).

## Compléter ton pipeline CI avec l'AWS local

> **Prérequis :** [Module 4 (CI/CD)](04-cicd.md). Cette section reprend le pipeline que tu y as construit.

Au [Module 4](04-cicd.md), tu as ajouté un job `integration-test` qui démarre un vrai PostgreSQL le temps des tests. Tu avais alors laissé de côté un troisième job, `aws-test`, en attendant de savoir ce qu'était AWS. C'est le moment.

### Le problème

Ton application a du code qui parle à S3 et à SQS (`backend/aws_client.py`). Comment le tester automatiquement à chaque push ?

| Mauvaise idée | Pourquoi c'est mauvais |
|---|---|
| « On utilise un vrai compte AWS de test » | Il faut mettre de **vraies clés AWS** dans les secrets GitHub — elles deviennent une cible. Ça coûte de l'argent à chaque exécution. Et deux pipelines lancés en même temps se marchent dessus : même nom de bucket, même file |
| « On simule AWS avec des mocks » | On teste alors sa propre imitation d'AWS, pas AWS. Une faute de frappe dans un nom de paramètre passe au travers sans être vue |
| « On ne teste pas ce code » | Le choix par défaut de beaucoup d'équipes… et la raison de beaucoup d'incidents |

**La bonne réponse : le même émulateur que tu utilises depuis le début de ce module, mais dans la CI.** Exactement comme PostgreSQL au [Module 4](04-cicd.md) — un service container, démarré le temps du job, jeté ensuite.

### Le job

Le fichier `.github/workflows/ci.yml` du projet le contient déjà :

```yaml
  aws-test:
    name: AWS Test
    runs-on: ubuntu-latest
    needs: lint

    services:
      floci:
        image: floci/floci:1.7.0
        ports:
          - 4566:4566
        options: >-
          --health-cmd "curl -f http://localhost:4566/health"
          --health-interval 5s
          --health-timeout 3s
          --health-retries 10

    steps:
      - uses: actions/checkout@v4
      - name: Setup uv
        uses: astral-sh/setup-uv@v4

      - name: Tests d'intégration AWS (Floci)
        env:
          AWS_ENDPOINT_URL: http://localhost:4566
          AWS_DEFAULT_REGION: us-east-1
          AWS_ACCESS_KEY_ID: test
          AWS_SECRET_ACCESS_KEY: test
        run: |
          cd backend
          uv run pytest -m integration
```

### Les trois choses à retenir

**1. Aucun secret AWS n'est nécessaire.** Écrire `AWS_ACCESS_KEY_ID: test` en clair dans le fichier ne pose aucun problème : ce sont des identifiants bidons pour un émulateur local. Compare avec le job `push` du [Module 4](04-cicd.md), qui a besoin, lui, de vrais secrets Docker Hub via `${{ secrets.* }}`. **La meilleure façon de protéger un secret, c'est de ne pas en avoir besoin.**

**2. Ici on utilise `AWS_ENDPOINT_URL`, pas l'alias `awslocal`.** Sur ta machine, tu tapes `awslocal` parce que ton AWS CLI est peut-être ancienne. Dans la CI, ce n'est pas l'AWS CLI qui parle à AWS, c'est **boto3** (la librairie Python) — et `aws_client.py` lit cette variable lui-même. Le code n'est pas modifié pour les tests : il est simplement **configuré** différemment.

**3. Le job est indépendant des deux autres.** `test`, `integration-test` et `aws-test` dépendent tous de `lint` mais pas les uns des autres : GitHub les exécute **en parallèle**.

```
                 ┌──▶ Test ─────────────┐
   Lint ─────────┼──▶ Integration Test ─┼──▶ Build ──▶ Push
                 └──▶ AWS Test ─────────┘
```

### Vérifie-le en local d'abord

```bash
cd ~/devops-project/floci && docker compose up -d && cd ../backend

AWS_ENDPOINT_URL=http://localhost:4566 uv run pytest -m integration
# ===== 4 passed, 7 deselected =====
```

Si ça passe chez toi, ça passera dans la CI : c'est la même image, la même version, les mêmes variables.

> **En entretien**, la question *« comment tu testes du code qui parle à AWS ? »* revient souvent. La réponse complète tient en trois points : des **tests unitaires** pour la logique métier, un **émulateur** (Floci, LocalStack, Testcontainers) pour l'intégration en CI, et une **validation sur un vrai environnement de staging** avant la prod — parce qu'un émulateur n'applique ni les permissions IAM ni les quotas.

## Projet pratique : Déployer le projet sur AWS

> **C'est ici que tu passes en Piste B — le vrai AWS.** C'est le seul exercice du module qui l'exige.

### Pourquoi celui-ci ne se fait pas en local

Tous les exercices précédents tournaient sur l'émulateur. Pour le déploiement final, non — et il vaut mieux comprendre pourquoi que de le subir :

| Ce qu'il faut ici | Pourquoi l'émulateur ne peut pas |
|---|---|
| **Lancer des containers sur le serveur** | Ton « serveur » émulé est lui-même un container. On peut y installer Docker, mais pas y lancer de containers (limitation du stockage imbriqué). Or tout le projet repose sur `docker compose up`. |
| **Une adresse joignable depuis Internet** | L'IP « publique » d'une instance émulée est `127.0.0.1` — ta propre machine. Personne d'autre ne peut ouvrir ton app. |
| **L'expérience réelle** | La console web, la vraie latence, les vraies erreurs de permissions, la facturation. Rien de tout ça n'existe en local. |

Et surtout : en entretien, tu veux pouvoir dire **« j'ai déployé une application sur AWS »**, pas « sur un émulateur ».

### Ce que tu as déjà fait

Bonne nouvelle : tu as **déjà** construit un VPC, un subnet, un security group, une clé SSH et une instance EC2 dans les exercices précédents, en ligne de commande. Tu vas refaire la même chose, mais dans la console web et pour de vrai. Les concepts sont identiques — seule l'interface change.

### 0. Avant de commencer

- [ ] Ton compte AWS est créé (voir [Piste B](#piste-b--créer-ton-compte-aws) plus haut)
- [ ] Ton **alerte de facturation** est en place — ne saute pas cette étape
- [ ] Ton user IAM `admin-dev` est créé, tu as ses clés d'accès
- [ ] Ton code est poussé sur GitHub

⚠️ **À partir d'ici, chaque ressource que tu crées peut coûter de l'argent si tu l'oublies.** Note quelque part ce que tu crées, et fais le nettoyage de l'étape 6 à la fin.

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

### 6. Nettoyer — ne saute pas cette étape

C'est l'étape que tout le monde oublie, et c'est celle qui coûte de l'argent.

```bash
# 1. Terminer l'instance (c'est elle qui coûte le plus cher)
aws ec2 terminate-instances --instance-ids i-TON_INSTANCE_ID

# 2. Vérifier qu'il ne reste rien qui tourne
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name!=`terminated`].[InstanceId,State.Name]' \
  --output table
```

Puis, dans la console : **VPC** → supprime le VPC `devops-vpc` (ça supprime aussi le subnet, l'internet gateway et les route tables associés).

> **Le réflexe à prendre :** avant de fermer ton ordinateur, va sur la page **Billing → Bills** de la console AWS. Elle te montre ce qui est facturé en ce moment. Cinq secondes de vérification valent mieux qu'une facture surprise.

### 7. Bonus — User Data (automatiser l'installation)

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

Avec ça, tu lances l'EC2 et l'app tourne toute seule en 2-3 minutes — sans te connecter en SSH. C'est exactement ce qu'on automatisera avec Terraform dans le [Module 6](06-terraform.md).

> **Tu n'es pas obligé de refaire l'exercice avec User Data.** C'est juste pour comprendre le concept. Le [Module 6](06-terraform.md) (Terraform) l'utilise automatiquement.

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

**Q : C'est quoi une Policy IAM ?**
R : Un document JSON qui définit des permissions : quelles actions (ex: `s3:GetObject`) sont autorisées ou refusées, sur quelles ressources (ex: un bucket précis). On l'attache à un User, un Group ou un Role pour lui donner ces droits.

**Q : C'est quoi le principe du moindre privilège ?**
R : Ne donner que les permissions strictement nécessaires pour faire le job, et rien de plus. Si une Lambda a juste besoin de lire un bucket S3, on lui donne uniquement `s3:GetObject` sur ce bucket précis — pas `AdministratorAccess`. Ça limite les dégâts si les credentials sont compromises.

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
- **[AWS en local avec Floci](floci-aws-local.md)** : le guide complet de l'émulateur, ses limites et son dépannage. Il existe aussi des émulateurs pour Azure et GCP
- **Testcontainers** : la même idée que Floci, mais démarrée automatiquement depuis le code de tes tests

## Tu peux passer au module suivant si...

**Piste A — la pratique en local**

- [ ] Tu sais démarrer Floci et vérifier qu'il répond
- [ ] Tu sais ce que fait `awslocal` et pourquoi on ne tape pas juste `aws`
- [ ] Tu as créé un bucket S3, déposé un fichier et généré une URL présignée
- [ ] Tu as construit un VPC + subnet + security group en ligne de commande
- [ ] Tu as lancé une instance EC2 et tu t'y es connecté en SSH
- [ ] Tu as créé une base RDS et tu t'y es connecté avec `psql`
- [ ] Tu as envoyé et reçu un message dans une file SQS, et tu sais expliquer le `ReceiptHandle`
- [ ] Tu as déployé et exécuté une Lambda
- [ ] Tu sais citer **deux** choses que l'émulateur ne sait pas faire
- [ ] Tu as complété ton pipeline CI avec le job `aws-test`
- [ ] Tu sais répondre à « comment tu testes du code qui parle à AWS ? »

**Les concepts**

- [ ] Tu sais ce que sont EC2, S3, VPC, RDS, IAM, DynamoDB, ECS et EKS (en une phrase chacun)
- [ ] Tu comprends la différence entre subnet public et privé
- [ ] Tu sais ce qu'est un Security Group (firewall AWS)
- [ ] Tu sais à quoi sert l'adresse `169.254.169.254`

**Piste B — le vrai AWS**

- [ ] Tu as un compte AWS avec une alerte de facturation configurée
- [ ] Le projet fil rouge tourne sur un EC2 accessible depuis ton navigateur
- [ ] Tu as bien terminé/supprimé toutes les ressources AWS pour éviter les coûts
