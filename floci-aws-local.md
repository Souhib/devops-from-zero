# AWS en local — Pratiquer sans compte et sans carte bancaire

> **Prérequis :** [Module 3 (Docker)](03-docker.md) — Floci se lance avec Docker, il faut donc l'avoir installé et compris avant.
>
> **En résumé :** Tu installes un programme qui **imite AWS sur ta machine**. Tes commandes `aws`, ton code Python et ton Terraform lui parlent exactement comme ils parleraient au vrai AWS. Tu peux tout créer, tout casser, tout recommencer — gratuitement et sans risque.

## Le problème qu'on résout

Le [Module 5 (AWS)](05-aws.md) te fait découvrir le cloud. Mais pour toucher au vrai AWS, il faut :

- créer un compte,
- **donner un numéro de carte bancaire**,
- faire attention à ne pas dépasser le Free Tier,
- penser à tout supprimer après chaque exercice, sinon la facture tombe.

Résultat : beaucoup de gens n'osent rien essayer. Ils lisent le module, ils comprennent la théorie, mais ils ne **pratiquent** pas. Et en entretien, ça se voit tout de suite — savoir réciter "S3 c'est du stockage objet" n'impressionne personne. Savoir dire "j'ai créé un bucket, j'ai buté sur une erreur de permissions, voilà comment je l'ai résolue", ça change tout.

## C'est quoi un émulateur ?

**Un émulateur, c'est un programme qui fait semblant d'être un autre système, suffisamment bien pour que les programmes autour ne voient pas la différence.**

Une analogie : un **simulateur de vol**. Ce n'est pas un avion. Mais les commandes sont au même endroit, elles réagissent pareil, et les instruments affichent la même chose. Un pilote peut s'y entraîner des centaines d'heures, rater des atterrissages, recommencer — sans risque et sans brûler de kérosène. Il ne remplace pas les heures de vol réelles, mais sans lui, personne ne pourrait s'entraîner autant.

**Floci**, c'est le simulateur de vol d'AWS.

- C'est un logiciel **libre et gratuit** (licence MIT), qui tourne dans un container Docker sur ta machine.
- Il **parle le même langage** qu'AWS. Quand ton programme envoie une requête "crée-moi un bucket S3", Floci la reçoit, la comprend, et répond exactement comme AWS aurait répondu.
- Il n'a besoin **d'aucun compte, aucun mot de passe, aucune connexion à Internet** une fois installé.
- Il est **léger** : quelques dizaines de méga-octets de RAM.

> **Un peu de contexte utile en entretien.** Jusqu'en mars 2026, l'outil de référence pour ça s'appelait **LocalStack**. Son éditeur a arrêté la version gratuite (« community edition ») cette année-là. Floci est né juste avant, comme remplaçant libre : il utilise le même port, les mêmes conventions, et la plupart des projets ont migré de l'un à l'autre sans changer une ligne de code. Si un recruteur te parle de LocalStack, tu sais de quoi il s'agit.

## Ce que tu vas pouvoir faire

| Tu vas pratiquer pour de vrai | Là où avant tu ne faisais que lire |
|---|---|
| **S3** — créer un bucket, déposer et relire des fichiers | [Module 5](05-aws.md) |
| **SQS** — envoyer un message dans une file, le consommer | [Module 5](05-aws.md) |
| **DynamoDB** — créer une table, y écrire, y lire | [Module 5](05-aws.md) |
| **Lambda** — déployer une fonction et l'exécuter | [Module 5](05-aws.md) |
| **RDS** — créer une base PostgreSQL et s'y connecter | [Module 5](05-aws.md) |
| **VPC / Subnet / Security Group** — construire un réseau | [Module 5](05-aws.md) |
| **EC2** — lancer un serveur et s'y connecter en SSH | [Module 5](05-aws.md) |
| **CloudWatch Logs, Route 53, Secrets Manager** | [Module 5](05-aws.md) |
| **Terraform** — `apply` et `destroy` autant de fois que tu veux | [Module 6](06-terraform.md) |
| **Tests d'intégration en CI** — sans secret AWS dans GitHub | [Module 5](05-aws.md) |

---

## Installation

### 1. Vérifier les prérequis

```bash
# Docker doit être installé et démarré (Module 3)
docker --version
# Docker version 24.x.x ou plus

# L'AWS CLI doit être installée (Module 5)
aws --version
# aws-cli/2.x.x
```

> **Si `aws` n'est pas installé**, reviens à la section [AWS CLI du Module 5](05-aws.md). Tu n'as **pas** besoin de faire `aws configure` ni d'avoir des identifiants : on va s'en passer.

### 2. Démarrer Floci

Le projet fil rouge contient déjà tout ce qu'il faut, dans le dossier `floci/` :

```bash
cd ~/devops-project/floci
docker compose up -d
```

La première fois, Docker télécharge l'image (~350 Mo), ça prend une ou deux minutes. Les fois suivantes, le démarrage prend quelques secondes.

### 3. Vérifier que ça marche

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4566/health
# 200
```

**`200`, c'est le code HTTP qui veut dire "tout va bien"** (revois les codes de statut au [Module 2](02-networking.md)). Si tu obtiens `000` ou `Connection refused`, c'est que Floci n'est pas encore démarré — attends 10 secondes et réessaie.

Tu peux aussi voir la liste des services émulés :

```bash
curl -s http://localhost:4566/health | head -c 300
# {"version":"1.7.0","services":{"s3":"running","sqs":"running","ec2":"running",...
```

---

## Configurer l'AWS CLI — et le piège à éviter

### Le problème

Par défaut, la commande `aws` envoie **tout au vrai AWS**. Il faut lui dire d'envoyer vers Floci à la place. L'adresse de Floci, c'est `http://localhost:4566`.

En jargon AWS, cette adresse s'appelle un **endpoint** — littéralement "point de terminaison", c'est-à-dire l'adresse à laquelle on envoie les requêtes.

### ⚠️ Le piège dans lequel tout le monde tombe

Beaucoup de tutoriels te disent de faire ça :

```bash
export AWS_ENDPOINT_URL=http://localhost:4566   # ⚠️ ne marche pas partout
```

**Cette variable n'est comprise que par les versions récentes de l'AWS CLI (2.13 et plus).** Sur une version plus ancienne, elle est **ignorée en silence** : ta commande part vers le vrai AWS, et tu obtiens une erreur incompréhensible :

```
An error occurred (InvalidAccessKeyId) when calling the CreateBucket operation:
The AWS Access Key Id you provided does not exist in our records.
```

Tu cherches pendant une heure ce qui cloche dans Floci... alors que Floci n'a jamais été contacté.

### La solution : un alias

On va créer un **raccourci de commande** (un "alias") nommé `awslocal`, qui ajoute automatiquement l'adresse de Floci. Avantages :

- ça marche avec **toutes** les versions de l'AWS CLI ;
- tu **vois** dans ta commande que tu es en local (`awslocal` ≠ `aws`) ;
- impossible d'envoyer par erreur une commande au vrai AWS.

Ajoute ces lignes à la fin de ton fichier `~/.bashrc` :

```bash
# ─── AWS local (Floci) ───
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
alias awslocal='aws --endpoint-url=http://localhost:4566'
```

Puis recharge le fichier :

```bash
source ~/.bashrc
```

> **`~/.bashrc`, c'est quoi ?** C'est un fichier de configuration lu automatiquement à chaque ouverture d'un terminal. Tout ce que tu y mets est appliqué à chaque nouvelle session. `source` sert à l'appliquer tout de suite, sans rouvrir le terminal. (Voir les variables d'environnement au [Module 1](01-linux-basics.md).)

### Pourquoi des identifiants bidons ?

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

**Floci ne vérifie pas les identifiants.** Il accepte n'importe quoi. Mais l'AWS CLI, elle, refuse de partir si aucun identifiant n'est défini — elle s'arrête avant même d'envoyer la requête. On lui en donne donc de faux, juste pour la satisfaire.

**Et `us-east-1` ?** C'est une **région** — un endroit dans le monde où AWS a des data centers. Floci s'en moque (tout tourne sur ta machine), mais l'AWS CLI en exige une. On prend `us-east-1` parce que c'est la région par défaut de la plupart des outils, ce qui évite des surprises avec Terraform.

---

## Ton premier aller-retour

```bash
# 1. Créer un bucket (un espace de stockage de fichiers)
awslocal s3 mb s3://mon-premier-bucket
# make_bucket: mon-premier-bucket

# 2. Créer un fichier de test sur ta machine
echo "Mon premier fichier dans le cloud" > test.txt

# 3. L'envoyer dans le bucket
awslocal s3 cp test.txt s3://mon-premier-bucket/
# upload: ./test.txt to s3://mon-premier-bucket/test.txt

# 4. Vérifier qu'il y est
awslocal s3 ls s3://mon-premier-bucket/
# 2026-08-22 14:12:03         34 test.txt

# 5. Le retélécharger sous un autre nom
awslocal s3 cp s3://mon-premier-bucket/test.txt recu.txt
cat recu.txt
# Mon premier fichier dans le cloud
```

**Ces cinq commandes sont EXACTEMENT celles que tu taperais sur le vrai AWS.** La seule différence, c'est `awslocal` au lieu de `aws`. C'est tout l'intérêt : ce que tu apprends ici est directement transposable.

---

## Le cycle de vie au quotidien

```bash
cd ~/devops-project/floci

# Démarrer
docker compose up -d

# Voir si c'est en bonne santé
docker compose ps
# STATUS doit afficher "Up (healthy)"

# Lire les logs (indispensable quand quelque chose ne marche pas)
docker compose logs -f floci
#   Ctrl+C pour sortir

# Arrêter (et TOUT effacer — voir ci-dessous)
docker compose down
```

### Remettre à zéro

Floci est configuré en mode **`memory`** : tout ce que tu crées vit dans la RAM. Un `docker compose down` efface donc tout, et le prochain `up` te rend un AWS **vierge**.

C'est volontaire, et c'est une bonne chose pour apprendre : tu peux tout casser, il te suffit de 10 secondes pour repartir propre.

```bash
docker compose down && docker compose up -d
# → AWS tout neuf
```

> **Si tu veux garder tes données** entre deux sessions, change `FLOCI_STORAGE_MODE: memory` en `FLOCI_STORAGE_MODE: persistent` dans `floci/docker-compose.yml`.

### Les ressources créées automatiquement

Au démarrage, Floci exécute les scripts du dossier `floci/init/ready.d/`. Le projet en fournit un qui crée d'avance :

| Ressource | À quoi elle sert |
|---|---|
| Bucket `taskflow-pieces-jointes` | Les pièces jointes des tâches (S3) |
| File `taskflow-traitements` | Les traitements longs (SQS) |
| Bucket `taskflow-tfstate` | Le state Terraform ([Module 6](06-terraform.md)) |

C'est un principe DevOps important : **tout ce que tu fais à la main plus de deux fois doit être scripté.**

---

## Ce que Floci fait vraiment (et ce qu'il ne fait pas)

C'est la partie la plus importante de cette page. Un émulateur n'est pas magique, et savoir exactement où sont ses limites t'évitera des heures de confusion.

### ✅ Ce qui fonctionne comme sur le vrai AWS

| Service | Ce que tu peux faire |
|---|---|
| **S3** | Créer des buckets, déposer/lire/supprimer des fichiers, générer des URL présignées |
| **SQS** | Créer des files, envoyer et recevoir des messages |
| **DynamoDB** | Créer des tables, écrire et lire des items |
| **Lambda** | Déployer du vrai code Python et l'exécuter réellement |
| **RDS** | Créer une base : Floci démarre un **vrai PostgreSQL**, auquel tu te connectes avec `psql` |
| **EC2** | Lancer une instance : Floci démarre un **vrai container Ubuntu**, dans lequel tu entres en **SSH** |
| **VPC / Subnet / Security Group / Elastic IP** | Construire un réseau complet |
| **IAM** | Créer des users, des policies, des rôles |
| **CloudWatch Logs**, **Route 53**, **Secrets Manager**, **ECR**, **CloudFormation** | Les opérations courantes |
| **Terraform / OpenTofu** | `init`, `plan`, `apply`, `destroy`, et même le **state distant sur S3** |

### ❌ Ce qui ne fonctionne pas — et pourquoi

| Limite | Explication | Conséquence pour toi |
|---|---|---|
| **Les permissions IAM ne sont pas appliquées** | Floci accepte **n'importe quels** identifiants et n'a aucun moteur d'autorisation. Tu peux créer une policy très restrictive, elle ne bloquera rien. | Tu apprends la **syntaxe** IAM, pas son **effet**. Les vraies erreurs `AccessDenied`, tu ne les rencontreras que sur le vrai AWS. |
| **Pas de console web** | AWS a un site avec des boutons ; Floci n'a qu'une API. | Tu ne t'entraînes qu'en ligne de commande. C'est un manque réel : en entretien on te demandera parfois de décrire la console. |
| **Pas de facturation, pas de quotas** | Rien n'est compté ni limité. | Tu n'apprends pas à raisonner en coûts — et c'est une vraie compétence DevOps. |
| **Pas d'accès depuis Internet** | Ton "EC2" n'a pas d'IP publique joignable de l'extérieur. Son "IP publique" est `127.0.0.1`, ta propre machine. | Tu ne peux pas montrer ton app à quelqu'un d'autre. |
| **Docker ne tourne pas *dans* une instance EC2 émulée** | L'instance émulée est déjà un container. Y installer Docker fonctionne, mais y **lancer** un container échoue (limitation technique du stockage imbriqué). | ⚠️ **Le déploiement final du projet (`docker compose up` sur le serveur) doit se faire sur le vrai AWS.** |
| **La couverture varie selon les services** | Floci est un projet jeune (première version publique en mars 2026). Les services principaux sont solides, les plus exotiques le sont moins. | Si une commande rare ne marche pas, ce n'est pas forcément toi. Vérifie sur [le dépôt du projet](https://github.com/floci-io/floci). |

### La règle à retenir

> **Floci sert à apprendre et à répéter. Le vrai AWS sert à valider.**
>
> Fais tous tes essais sur Floci — autant de fois que tu veux, gratuitement. Puis fais **une fois** le déploiement final sur le vrai AWS, pour l'avoir fait pour de vrai et pouvoir en parler en entretien.

---

## Résoudre les problèmes

### `Could not connect to the endpoint URL: "http://localhost:4566/"`

Floci n'est pas démarré, ou pas encore prêt.

```bash
cd ~/devops-project/floci
docker compose ps          # STATUS doit être "Up (healthy)"
docker compose up -d       # s'il n'est pas lancé
docker compose logs floci  # pour voir ce qui coince
```

### `InvalidAccessKeyId ... does not exist in our records`

**Ta commande est partie vers le VRAI AWS.** C'est le piège de l'endpoint décrit plus haut.

- Tu as tapé `aws` au lieu de `awslocal` ?
- L'alias est-il bien chargé ? Vérifie avec `alias awslocal` — ça doit afficher la définition. Sinon, `source ~/.bashrc`.

### `Unable to locate credentials`

Les variables `AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY` ne sont pas définies.

```bash
echo $AWS_ACCESS_KEY_ID   # doit afficher "test"
source ~/.bashrc          # si c'est vide
```

### `Bind for 0.0.0.0:4566 failed: port is already allocated`

Un autre programme occupe déjà le port 4566 — le plus souvent, un ancien Floci resté en route.

```bash
docker ps | grep 4566           # voir qui occupe le port
cd ~/devops-project/floci
docker compose down             # arrêter proprement
```

### Une instance EC2 ou une base RDS passe directement en `terminated` / échoue

Floci n'arrive pas à joindre Docker. Regarde les logs :

```bash
docker compose logs floci | grep -i "BindException\|Failed to launch"
```

Si tu vois `java.net.BindException: Permission denied`, c'est que le service `dockerproxy` du `docker-compose.yml` n'a pas démarré. Vérifie :

```bash
docker compose ps    # les DEUX services doivent tourner
docker compose up -d
```

### Je me connecte en SSH à mon EC2 et j'ai `Connection closed`

Deux causes possibles, dans cet ordre :

1. **L'instance n'a pas fini de démarrer.** L'image Ubuntu n'a pas de serveur SSH : Floci l'installe au lancement, ce qui prend une bonne minute. `running` ne veut pas dire "prêt". Attends et réessaie — c'est exactement le même comportement que sur le vrai AWS.
2. **Le serveur SSH n'a pas pu démarrer.** Il lui manque un dossier. La solution est dans le UserData du [Module 5](05-aws.md) — vérifie que tu l'as bien passé avec `--user-data`.

### Je n'arrive pas à me connecter à ma base RDS

L'adresse renvoyée par `describe-db-instances` est une adresse **interne à Docker** (du type `172.x.x.x`), qui ne veut rien dire depuis ta machine. Utilise `localhost` avec **le même port** :

```bash
awslocal rds describe-db-instances \
  --db-instance-identifier ma-base \
  --query 'DBInstances[0].Endpoint' --output table
# Address: 172.25.0.3   Port: 7001
#          ^^^^^^^^^^ ignore l'adresse, garde le PORT

psql -h localhost -p 7001 -U postgres
#       ^^^^^^^^^ toujours localhost depuis ta machine
```

---

## Récapitulatif

```bash
# Démarrer                cd ~/devops-project/floci && docker compose up -d
# Vérifier                curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4566/health
# Utiliser                awslocal s3 ls
# Remettre à zéro         docker compose down && docker compose up -d
# Arrêter                 docker compose down
```

| Ce qu'il faut retenir | |
|---|---|
| L'adresse de Floci | `http://localhost:4566` |
| Depuis un autre container | `http://floci:4566` (jamais `localhost`) |
| Les identifiants | N'importe lesquels — on met `test` / `test` |
| La commande | `awslocal` (= `aws --endpoint-url=http://localhost:4566`) |
| Les données | Perdues à chaque `docker compose down` (c'est voulu) |
| Ce qu'il ne remplace pas | Le vrai déploiement final, la console, les permissions, les coûts |

## Pour aller plus loin

- [Le dépôt officiel de Floci](https://github.com/floci-io/floci) — la liste complète des services et leur niveau de support
- [La documentation de Floci](https://floci.io/) — il existe aussi des émulateurs pour Azure, Google Cloud et Oracle Cloud
- [Testcontainers](https://testcontainers.com/) — la même idée poussée plus loin : démarrer automatiquement les services dont tes tests ont besoin, depuis le code du test lui-même
