# Module 6 : Terraform

## C'est quoi Terraform et pourquoi ça existe ?

**Le problème :** Tu viens de créer ton infra AWS en cliquant partout dans la console. Ça a pris 30 minutes. Maintenant imagine : ton chef te dit "refais la même chose pour l'environnement de staging". Et aussi pour la préprod. Et documente ce que tu as créé pour ton collègue. Et si tu te trompes, reviens en arrière.

Avec des clics, c'est impossible à reproduire, impossible à versionner, impossible à partager. **Terraform résout ça** : tu décris ton infra dans du code. Un fichier texte, versionné dans Git, que n'importe qui peut lire et exécuter.

**L'analogie :** Terraform, c'est le **plan d'architecte** de ton infrastructure.
- `terraform plan` = revue du plan avec le client ("voilà ce qu'on va construire")
- `terraform apply` = envoyer l'équipe de construction
- `terraform destroy` = démolition
- Le **state file** = le plan "tel que construit" (as-built)

**En une phrase :** Infrastructure as Code (IaC) — ton infra est du code, pas des clics.

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

Terraform utilise HCL (HashiCorp Configuration Language). Ce n'est pas un langage de programmation — c'est du déclaratif : tu décris CE QUE TU VEUX, Terraform s'occupe du COMMENT.

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
  ami           = "ami-0a89a7563fc68be84"  # Ubuntu 24.04 eu-west-3
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

Le fichier `terraform.tfstate` enregistre l'état actuel de ton infra. Terraform le compare à ton code pour savoir quoi créer/modifier/supprimer.

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

# --- EC2 ---
resource "aws_instance" "web" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_name

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

variable "ami_id" {
  description = "AMI Ubuntu 24.04 pour eu-west-3"
  default     = "ami-0a89a7563fc68be84"
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

### 5. Lancer !

```bash
terraform init
# Terraform has been successfully initialized!

terraform plan -var="key_name=devops-key" -var="github_user=TON_USER"
# Plan: 6 to add, 0 to change, 0 to destroy.

terraform apply -var="key_name=devops-key" -var="github_user=TON_USER"
# Apply complete! Resources: 6 added
# Outputs:
#   app_url    = "http://13.38.x.x"
#   public_ip  = "13.38.x.x"
#   ssh_command = "ssh -i ~/devops-key.pem ubuntu@13.38.x.x"
```

Attends 2-3 minutes (le user_data installe Docker et lance l'app), puis ouvre l'URL.

**Ce que tu viens de faire à la main en 30 min, Terraform l'a fait en 2 min.** Et tu peux le refaire à l'identique avec un seul `terraform apply`.

### 6. Nettoyer

```bash
terraform destroy -var="key_name=devops-key" -var="github_user=TON_USER"
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

## Erreurs courantes

- **Oublier `terraform init`** → "Provider not found". Il faut init à chaque nouveau projet ou après avoir ajouté un provider.
- **Modifier le state file à la main** → Ça casse tout. Utilise `terraform state` si besoin.
- **Committer `terraform.tfstate`** → Ajoute `*.tfstate` à `.gitignore`.
- **Oublier de destroy après les tests** → Coût AWS inattendu.
- **Hardcoder des valeurs** → Utilise des variables pour tout ce qui change entre environnements.

## Pour aller plus loin

- **OpenTofu** : fork open-source de Terraform (suite au changement de licence de HashiCorp)
- **Pulumi** : IaC en vrai langage de programmation (Python, TypeScript, Go)
- **Terragrunt** : wrapper pour gérer Terraform à grande échelle
- **Terraform Cloud** : gestion du state et collaboration en équipe
- **Workspaces** : gérer plusieurs environnements (dev, staging, prod) avec le même code
- **Import** : `terraform import` pour importer des ressources existantes dans le state
