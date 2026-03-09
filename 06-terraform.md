# Module 6 : Terraform

> **Prérequis :** Module 5 (AWS — comprendre EC2, VPC, Security Groups avant de les automatiser)

> **En résumé :** Tu remplaces les clics manuels dans la console AWS par du code. Terraform te permet de décrire ton infrastructure dans des fichiers, versionnés dans Git, reproductibles et partageables. Ce que tu as fait en 30 min à la main, Terraform le fait en 2 min.

## C'est quoi Terraform et pourquoi ça existe ?

**Le problème :** Tu viens de créer ton infra AWS en cliquant partout dans la console. Ça a pris 30 minutes. Maintenant imagine : ton chef te dit "refais la même chose pour l'environnement de staging". Et aussi pour la préprod. Et documente ce que tu as créé pour ton collègue. Et si tu te trompes, reviens en arrière.

Avec des clics, c'est impossible à reproduire, impossible à versionner, impossible à partager. **Terraform résout ça** : tu décris ton infra dans du code. Un fichier texte, versionné dans Git, que n'importe qui peut lire et exécuter.

**L'analogie :** Terraform, c'est le **plan d'architecte** de ton infrastructure.
- `terraform plan` = revue du plan avec le client ("voilà ce qu'on va construire")
- `terraform apply` = envoyer l'équipe de construction
- `terraform destroy` = démolition
- Le **state file** = le plan "tel que construit" (as-built)

**En une phrase :** Infrastructure as Code (IaC) — ton infra est du code, pas des clics.

> Tu as créé cette infra manuellement dans le Module 5 (AWS). Terraform automatise exactement les mêmes étapes.

## Installation

```bash
# Ajouter le repo HashiCorp
sudo apt update && sudo apt install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform

terraform --version
# Terraform v1.x.x
```

## IaC — Avant vs Après

| | Avant (clics) | Après (Terraform) |
|--|--------------|-------------------|
| Reproductible ? | Non | Oui, `terraform apply` |
| Documenté ? | Non (qui se souvient des clics ?) | Oui, c'est du code |
| Versionné ? | Non | Oui, dans Git |
| Revue possible ? | Non | Oui, pull request |
| Rollback ? | Non (tu cliques en sens inverse...) | Oui, commit précédent |

## HCL — Le langage de Terraform

Terraform utilise HCL (HashiCorp Configuration Language). Ce n'est pas un langage de programmation classique — c'est du **déclaratif** : tu décris CE QUE TU VEUX ("je veux un serveur avec 2 Go de RAM dans telle région"), et Terraform s'occupe du COMMENT (quelles API appeler, dans quel ordre, etc.). C'est l'opposé de l'**impératif** où tu décris chaque étape toi-même ("d'abord crée le réseau, puis crée le serveur, puis attache-le au réseau...").

### Provider

Un provider connecte Terraform à un service (AWS, GCP, Azure...).

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"  # Paris
}
```

### Resource

Une resource = quelque chose que Terraform crée/gère.

```hcl
resource "aws_instance" "mon_serveur" {
  ami           = data.aws_ami.ubuntu.id  # Récupéré automatiquement (voir data source)
  instance_type = "t2.micro"

  tags = {
    Name = "devops-server"
  }
}
```

La syntaxe : `resource "TYPE" "NOM_LOCAL" { ... }`. Le type vient du provider. Le nom local est ton choix (pour y faire référence dans le code).

### Variables

```hcl
# variables.tf
variable "instance_type" {
  description = "Type d'instance EC2"
  default     = "t2.micro"
}

variable "project_name" {
  description = "Nom du projet"
  default     = "devops"
}
```

Utilisation : `var.instance_type`, `var.project_name`.

### Outputs

Affiche des infos après `apply` (IP publique, URL, etc.).

```hcl
# outputs.tf
output "public_ip" {
  value       = aws_instance.mon_serveur.public_ip
  description = "IP publique du serveur"
}
```

## Les 4 commandes

```bash
# 1. Initialiser (télécharge le provider)
terraform init
# Initializing provider plugins...
# Terraform has been successfully initialized!

# 2. Prévisualiser les changements
terraform plan
# Plan: 3 to add, 0 to change, 0 to destroy.
# (montre ce qui va être créé/modifié/supprimé)

# 3. Appliquer
terraform apply
# Do you want to perform these actions? yes
# Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

# 4. Détruire tout
terraform destroy
# Do you really want to destroy all resources? yes
# Destroy complete! Resources: 3 destroyed.
```

## Le State File

Le fichier `terraform.tfstate` enregistre l'état actuel de ton infra — c'est la mémoire de Terraform. Il sait "j'ai créé un serveur avec l'ID i-abc123, un VPC avec l'ID vpc-def456, etc.". Quand tu relances `terraform apply`, il compare ce fichier avec ton code pour savoir quoi créer, modifier ou supprimer.

⚠️ **Ne modifie JAMAIS le state file à la main.**
⚠️ **Ne committe JAMAIS le state file dans Git** (il peut contenir des secrets).

En équipe, on stocke le state sur un backend distant (S3 par exemple) pour que tout le monde travaille sur le même état.

## Modules (concept)

Un module = un bloc réutilisable de code Terraform. Comme une fonction en programmation. Si tu crées souvent un VPC + EC2 + Security Group, tu mets ça dans un module et tu l'appelles avec des paramètres différents.

On n'en crée pas dans ce cours, mais sache que ça existe.

## Projet pratique : Recréer l'infra AWS avec Terraform

On va recréer exactement ce qu'on a fait à la main dans le Module 5, mais en code.

### 1. Créer la structure

```bash
mkdir -p ~/devops-terraform
cd ~/devops-terraform
```

### 2. Le fichier principal

Crée `main.tf` :

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- VPC ---
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = { Name = "${var.project_name}-public" }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "${var.project_name}-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = { Name = "${var.project_name}-rt" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# --- Security Group ---
resource "aws_security_group" "web" {
  name   = "${var.project_name}-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Backend"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-sg" }
}

# --- AMI (récupère automatiquement la dernière Ubuntu 24.04) ---
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical (éditeur d'Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}

# --- EC2 ---
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_name

  # user_data = un script qui s'exécute automatiquement au premier démarrage du serveur
  # C'est comme ça qu'on automatise l'installation de Docker sans se connecter en SSH
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose-v2
    usermod -aG docker ubuntu
    systemctl enable docker
    systemctl start docker

    mkdir -p /home/ubuntu/devops-project
    cd /home/ubuntu/devops-project
    git clone https://github.com/${var.github_user}/devops-project.git .
    # ⚠️ Si ton repo est privé, le git clone échouera.
    # Solution : rends-le public ou utilise un token GitHub dans l'URL :
    # git clone https://TOKEN@github.com/user/repo.git .
    docker compose up -d --build
  EOF

  tags = { Name = "${var.project_name}-server" }
}
```

### 3. Variables

Crée `variables.tf` :

```hcl
variable "aws_region" {
  default = "eu-west-3"
}

variable "project_name" {
  default = "devops"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "Nom de la key pair EC2"
}

variable "github_user" {
  description = "Ton nom d'utilisateur GitHub"
}
```

### 4. Outputs

Crée `outputs.tf` :

```hcl
output "public_ip" {
  value = aws_instance.web.public_ip
}

output "ssh_command" {
  value = "ssh -i ~/devops-key.pem ubuntu@${aws_instance.web.public_ip}"
}

output "app_url" {
  value = "http://${aws_instance.web.public_ip}"
}
```

### 5. Fichier de variables (`terraform.tfvars`)

Passer les variables en `-var="..."` dans la ligne de commande, c'est pénible et ça ne se versionne pas facilement. En pratique, on utilise un fichier `.tfvars` :

Crée `terraform.tfvars` :
```hcl
key_name    = "devops-key"
github_user = "TON_USER"
```

Terraform charge automatiquement `terraform.tfvars` s'il existe. Sinon, tu peux spécifier un fichier :
```bash
terraform apply -var-file="production.tfvars"
```

C'est comme ça qu'on gère plusieurs environnements : un `dev.tfvars`, un `staging.tfvars`, un `prod.tfvars`, chacun avec des valeurs différentes (taille d'instance, nom du projet, etc.).

⚠️ **Ne committe pas les `.tfvars` qui contiennent des secrets.** Ajoute `*.tfvars` à `.gitignore` si besoin. Les variables non sensibles (région, instance type) peuvent être committées.

### 6. Lancer !

```bash
terraform init
# Terraform has been successfully initialized!

terraform plan
# Plan: 6 to add, 0 to change, 0 to destroy.

terraform apply
# Apply complete! Resources: 6 added
# Outputs:
#   app_url    = "http://13.38.x.x"
#   public_ip  = "13.38.x.x"
#   ssh_command = "ssh -i ~/devops-key.pem ubuntu@13.38.x.x"
```

Attends 2-3 minutes (le user_data installe Docker et lance l'app), puis ouvre l'URL.

**Ce que tu viens de faire à la main en 30 min, Terraform l'a fait en 2 min.** Et tu peux le refaire à l'identique avec un seul `terraform apply`.

### 7. Nettoyer

```bash
terraform destroy
# Destroy complete! Resources: 6 destroyed.
```

## Coin entretien

**Q : C'est quoi Terraform ?**
R : Un outil d'Infrastructure as Code. Tu décris ton infra dans des fichiers HCL, Terraform la crée/modifie/supprime. Versionnable, reproductible, collaboratif.

**Q : C'est quoi Infrastructure as Code ?**
R : Gérer l'infrastructure (serveurs, réseaux, bases de données) via du code au lieu de clics manuels. Avantages : reproductible, versionné, auditable.

**Q : Expliquer plan, apply, destroy.**
R : `plan` montre ce qui va changer sans rien faire. `apply` exécute les changements. `destroy` supprime tout. On fait toujours plan avant apply pour vérifier.

**Q : C'est quoi le state file ?**
R : Un fichier JSON qui enregistre l'état actuel de l'infra gérée par Terraform. Il permet de comparer l'état réel avec le code pour savoir quoi créer/modifier/supprimer.

**Q : Pourquoi ne pas committer le state file ?**
R : Il peut contenir des secrets (mots de passe, clés). On le stocke dans un backend distant (S3 + DynamoDB pour le lock).

**Q : Terraform vs CloudFormation ?**
R : Terraform est multi-cloud (AWS, GCP, Azure). CloudFormation est spécifique AWS. Terraform a une communauté plus large et une syntaxe plus lisible.

## Bonnes pratiques

- **Toujours `plan` avant `apply`.** Relis le plan. Vérifie ce qui va être détruit. Un `destroy` accidentel d'une base de données en prod, ça arrive.
- **State distant dès le jour 1.** En équipe, le state local est un cauchemar (conflits, perte de données). Utilise un backend S3 + DynamoDB pour le locking.
- **Un `.tfvars` par environnement.** `dev.tfvars`, `staging.tfvars`, `prod.tfvars`. Même code, valeurs différentes.
- **Ne committe pas le state ni les secrets.** `.gitignore` doit contenir `*.tfstate`, `*.tfstate.backup`, `.terraform/`. Les `.tfvars` avec des secrets aussi.
- **Formate ton code.** `terraform fmt` avant chaque commit. C'est l'équivalent d'un linter pour Terraform.
- **Nomme tes ressources de façon cohérente.** `${var.project_name}-${var.environment}-resource`. Exemple : `devops-prod-sg`. Quand tu as 100 ressources dans la console AWS, les noms sont la seule façon de s'y retrouver.
- **Pas de modification manuelle.** Si quelqu'un modifie l'infra dans la console AWS, le prochain `terraform apply` va écraser ses changements. Tout passe par le code.

## Erreurs courantes

- **Oublier `terraform init`** → "Provider not found". Il faut init à chaque nouveau projet ou après avoir ajouté un provider.
- **Modifier le state file à la main** → Ça casse tout. Utilise `terraform state` si besoin.
- **Committer `terraform.tfstate`** → Ajoute `*.tfstate` à `.gitignore`.
- **Oublier de destroy après les tests** → Coût AWS inattendu.
- **Hardcoder des valeurs** → Utilise des variables pour tout ce qui change entre environnements.
- **Passer les variables en `-var` à chaque commande** → Utilise un fichier `.tfvars`, c'est plus propre et reproductible.

## Pour aller plus loin

- **OpenTofu** : fork open-source de Terraform (suite au changement de licence de HashiCorp)
- **Pulumi** : IaC en vrai langage de programmation (Python, TypeScript, Go)
- **Terragrunt** : wrapper pour gérer Terraform à grande échelle
- **Terraform Cloud** : gestion du state et collaboration en équipe
- **Workspaces** : gérer plusieurs environnements (dev, staging, prod) avec le même code
- **Import** : `terraform import` pour importer des ressources existantes dans le state

## Tu peux passer au module suivant si...

- [ ] Tu sais expliquer Infrastructure as Code en une phrase
- [ ] Tu connais les 4 commandes : `init`, `plan`, `apply`, `destroy`
- [ ] Tu sais écrire une resource HCL basique (provider, resource, variable, output)
- [ ] Tu comprends le rôle du state file (et pourquoi ne pas le committer)
- [ ] Tu as recréé l'infra AWS du Module 5 avec `terraform apply`
- [ ] Tu as nettoyé avec `terraform destroy`
