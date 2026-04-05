# Troubleshooting — Lire et comprendre les erreurs

> Un DevOps passe environ 50% de son temps à lire des logs et résoudre des problèmes. Ce fichier te montre les erreurs les plus courantes que tu vas rencontrer, ce qu'elles veulent dire, et comment les résoudre.

## La méthode — Toujours la même

Peu importe l'erreur, la démarche est toujours la même :

1. **Lire le message d'erreur** — la réponse est souvent dedans, mot pour mot
2. **Identifier QUEL composant a le problème** — c'est Docker ? L'app ? La DB ? Le réseau ?
3. **Vérifier les logs** — `docker logs`, `kubectl logs`, le output du terminal
4. **Chercher le message sur Google / IA** — si tu ne comprends pas, copie-colle le message

Ne fais **jamais** ça : ignorer l'erreur et retenter la même commande en espérant que ça passe.

---

## Linux

### `No space left on device`

```
write /var/lib/docker/...: no space left on device
```

**Ce que ça veut dire :** Le disque est plein. C'est une des causes de crash les plus fréquentes en prod. Souvent causé par les images Docker qui s'accumulent, les logs qui grossissent, ou les backups qui s'empilent.

**Comment résoudre :**
```bash
# Voir l'espace disque
df -h
# Filesystem      Size  Used Avail Use%
# /dev/sda1        30G   29G  1.0G  97%   ← presque plein !

# Si c'est Docker qui prend la place (cas le plus courant)
docker system df                  # voir l'espace utilisé par Docker
docker system prune -a            # supprimer tout ce qui n'est pas utilisé

# Si ce sont les logs
du -sh /var/log/*                 # voir quels logs prennent le plus de place
sudo truncate -s 0 /var/log/syslog  # vider un fichier de log sans le supprimer
```

---

### `command not found`

```
bash: terraform: command not found
```

**Ce que ça veut dire :** Le programme n'est pas installé, ou il est installé mais pas dans le PATH (la liste des dossiers où Linux cherche les programmes).

**Comment résoudre :**
```bash
# Est-ce que c'est installé ?
which terraform
# Si rien ne s'affiche → pas installé. Installe-le.

# Si c'est installé mais pas trouvé → problème de PATH
echo $PATH
# Vérifie que le dossier contenant le programme est dans la liste

# Cas fréquent après une installation : relancer le terminal
# ou faire :
source ~/.bashrc
```

---

### `Permission denied` quand tu édites un fichier

```
bash: /etc/nginx/nginx.conf: Permission denied
```

**Ce que ça veut dire :** Tu essaies de modifier un fichier système sans les droits administrateur.

**Comment résoudre :**
```bash
# Ajouter sudo devant la commande
sudo nano /etc/nginx/nginx.conf
```

---

## Docker

### `Error response from daemon: port is already allocated`

```
Error response from daemon: driver failed programming external connectivity:
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Ce que ça veut dire :** Un autre programme utilise déjà le port 8000 sur ta machine. Deux programmes ne peuvent pas écouter sur le même port.

**Comment résoudre :**
```bash
# Trouver qui utilise le port 8000
ss -tlnp | grep 8000

# Si c'est un ancien container Docker
docker ps -a | grep 8000
docker stop <nom_du_container>
docker rm <nom_du_container>

# Si c'est un processus local (uvicorn lancé manuellement par exemple)
kill <PID>
```

---

### `Exited (1)` — L'application a crashé

```
CONTAINER ID  IMAGE       STATUS                     NAMES
abc123        mon-app     Exited (1) 30 seconds ago  backend
```

**Ce que ça veut dire :** Exit code `1` = l'application elle-même a crashé (bug, dépendance manquante, variable d'environnement absente, erreur de syntaxe...). C'est un problème dans le code ou la config, pas dans Docker.

**Comment résoudre :**
```bash
# TOUJOURS commencer par les logs
docker logs backend
# L'erreur est dans les dernières lignes :
# - "ModuleNotFoundError" → dépendance pas installée (vérifier le Dockerfile)
# - "KeyError: 'DATABASE_URL'" → variable d'environnement manquante
# - "SyntaxError" → erreur de syntaxe dans le code
# - "FileNotFoundError" → un fichier attendu n'existe pas dans le container
```

---

### `Exited (137)` — Container tué par le système

```
CONTAINER ID  IMAGE       STATUS                      NAMES
abc123        mon-app     Exited (137) 2 minutes ago  backend
```

**Ce que ça veut dire :** Le code `137` = le process a reçu un SIGKILL (128+9=137). C'est quelque chose **d'extérieur** qui a tué le container, pas l'application elle-même.

| Cause | Comment vérifier |
|-------|-----------------|
| **OOM Kill** (trop de mémoire) — le plus courant | `docker stats` → la mémoire est proche de la limite |
| **`docker stop` timeout** (le container ne s'arrête pas en 10s) | Regarde si tu as fait un `docker stop` juste avant |
| **Limite de ressources dépassée** (Docker Compose ou K8s) | Vérifie les `resources.limits` dans ta config |

**Comment résoudre (cas OOM) :**
```bash
docker stats
# CONTAINER  CPU %  MEM USAGE / LIMIT
# backend    2%     450MiB / 512MiB     ← presque à la limite !

# Augmenter la limite mémoire dans docker-compose.yml :
#   deploy:
#     resources:
#       limits:
#         memory: 1024M

# Si la mémoire monte sans s'arrêter → fuite mémoire
# → remonter aux devs avec les métriques Grafana
```

---

### `COPY failed: file not found in build context`

```
COPY failed: file not found in build context or excluded by .dockerignore
```

**Ce que ça veut dire :** Le Dockerfile essaie de copier un fichier qui n'existe pas dans le dossier de build, ou qui est exclu par le `.dockerignore`.

**Comment résoudre :**
```bash
# Vérifier que le fichier existe dans le bon dossier
ls -la
# Le "contexte" de build c'est le dossier après le "." dans "docker build -t mon-app ."

# Vérifier le .dockerignore — peut-être que le fichier est exclu
cat .dockerignore

# Erreur fréquente : être dans le mauvais dossier quand tu lances docker build
pwd
# Tu dois être dans le dossier qui contient le Dockerfile
```

---

### `no matching manifest for linux/arm64` (Mac M1/M2/M3)

```
no matching manifest for linux/arm64/v8 in the manifest list entries
```

**Ce que ça veut dire :** L'image Docker est faite pour les processeurs Intel (x86), mais ton Mac a un processeur ARM. L'image n'est pas compatible.

**Comment résoudre :**
```bash
# Forcer le build pour la plateforme Intel
docker build --platform linux/amd64 -t mon-app .

# Ou dans docker-compose.yml :
#   services:
#     backend:
#       platform: linux/amd64
```

> Ce problème n'arrive pas sur WSL/Linux. Tu le croiseras si tu travailles sur Mac.

---

## CI/CD (GitHub Actions)

### `Error: Process completed with exit code 1`

```
Error: Process completed with exit code 1
```

**Ce que ça veut dire :** Une commande dans le pipeline a échoué. Le `exit code 1` veut dire "erreur générique". Le vrai message est **au-dessus** dans les logs.

**Comment résoudre :**
```
# Remonte dans les logs du job GitHub Actions
# L'erreur est dans les lignes AVANT "Process completed with exit code 1"
# Exemples :
# "ruff check failed" → le linter a trouvé des erreurs de style → fixe le code
# "FAILED tests/test_main.py" → un test a échoué → regarde lequel et pourquoi
# "docker build failed" → erreur dans le Dockerfile → regarde le message Docker
```

---

### `Permission denied` lors du push Docker Hub

```
denied: requested access to the resource is denied
```

**Ce que ça veut dire :** GitHub Actions essaie de push une image sur Docker Hub mais n'a pas les droits.

**Comment résoudre :**
```
# Vérifier les secrets dans GitHub :
# Settings → Secrets and variables → Actions
# - DOCKERHUB_USERNAME → ton username Docker Hub
# - DOCKERHUB_TOKEN → un Access Token (pas ton mot de passe !)
#   Créé sur https://hub.docker.com/settings/security

# Erreur courante : le secret est mal nommé
# Dans le YAML : ${{ secrets.DOCKERHUB_TOKEN }}
# Dans GitHub : le secret doit s'appeler EXACTEMENT "DOCKERHUB_TOKEN"
```

---

### Le pipeline passe mais l'app est cassée en prod

**Ce que ça veut dire :** Les tests ne couvrent pas le cas qui casse. Le pipeline fait son travail (il exécute les tests), mais les tests ne vérifient pas tout.

**Comment résoudre :**
```
# Ce n'est pas un bug du pipeline — c'est un test manquant
# 1. Identifier ce qui a cassé en prod (les logs de l'app)
# 2. Écrire un test qui reproduit le bug (ticket pour les devs)
# 3. Le pipeline attrapera ce cas la prochaine fois

# Prévention : ajouter un "smoke test" après le déploiement
# = un test basique qui vérifie que l'app répond (curl /api/health)
```

---

## SSH et AWS

### `Connection refused` vs `Connection timed out`

Ce sont **deux problèmes complètement différents** :

| Erreur | Ce que ça veut dire | Cause probable |
|--------|-------------------|----------------|
| `Connection refused` | La machine est joignable MAIS rien n'écoute sur ce port | Le service SSH n'est pas lancé, ou le port est faux |
| `Connection timed out` | La machine n'est PAS joignable du tout | Mauvaise IP, Security Group bloque le port 22, la machine est éteinte |

```bash
# Connection refused → vérifier que SSH tourne sur le serveur
sudo systemctl status sshd

# Connection timed out → vérifier :
# 1. L'IP est correcte ?
# 2. Le Security Group autorise le port 22 depuis ton IP ?
# 3. L'instance est bien "Running" dans la console AWS ?
```

---

### `Permission denied (publickey)`

```
Permission denied (publickey).
```

**Ce que ça veut dire :** Le serveur ne reconnaît pas ta clé SSH.

**Comment résoudre :**
```bash
# 1. Tu utilises la bonne clé ?
ssh -i ~/devops-key.pem ubuntu@IP
# (pas ssh -i ~/autre-cle.pem)

# 2. Les permissions de la clé sont correctes ?
chmod 400 ~/devops-key.pem
# SSH refuse une clé avec des permissions trop ouvertes

# 3. Le bon utilisateur ?
# Ubuntu → ubuntu
# Amazon Linux → ec2-user
# Debian → admin
```

---

### `WARNING: UNPROTECTED PRIVATE KEY FILE`

```
WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions 0644 for 'devops-key.pem' are too open.
```

**Ce que ça veut dire :** La clé SSH est lisible par d'autres utilisateurs sur ta machine. SSH refuse de l'utiliser par sécurité.

**Comment résoudre :**
```bash
chmod 400 ~/devops-key.pem
# 400 = lecture seule, uniquement pour toi
```

---

### `AccessDenied` / `UnauthorizedOperation` sur AWS

```
An error occurred (AccessDenied) when calling the DescribeInstances operation:
User: arn:aws:iam::123456:user/admin-dev is not authorized to perform: ec2:DescribeInstances
```

**Ce que ça veut dire :** Ton utilisateur IAM n'a pas les permissions pour faire cette action sur AWS.

**Comment résoudre :**
```bash
# Vérifier quel utilisateur tu utilises
aws sts get-caller-identity
# Ça te montre quel user/role est actif

# Ajouter les permissions manquantes dans IAM :
# Console AWS → IAM → Users → ton user → Attach policies
# Pour le cours : "AdministratorAccess" (pas en prod !)
```

---

## Terraform

### `Error: No valid credential sources found`

```
Error: error configuring Terraform AWS Provider: no valid credential sources found
```

**Ce que ça veut dire :** Terraform ne trouve pas tes identifiants AWS.

**Comment résoudre :**
```bash
aws configure list
# Si "access_key" et "secret_key" sont vides → reconfigurer :
aws configure
```

---

### `Error: resource already exists`

```
Error: creating EC2 Instance: InvalidParameterValue:
  An instance with the name 'devops-server' already exists
```

**Ce que ça veut dire :** Terraform essaie de créer une ressource qui existe déjà (créée à la main ou par un ancien `apply`).

**Comment résoudre :**
```bash
# Option 1 : importer la ressource existante dans le state
terraform import aws_instance.web i-1234567890abcdef0

# Option 2 : supprimer la ressource manuellement sur AWS, puis relancer
terraform apply
```

---

### `Error: Error acquiring the state lock`

```
Error: Error acquiring the state lock
Lock Info:
  ID:        abc123
  Operation: OperationTypeApply
  Who:       user@machine
```

**Ce que ça veut dire :** Quelqu'un d'autre (ou toi dans un autre terminal) fait un `terraform apply` en même temps. Terraform verrouille le state pour éviter les conflits.

**Comment résoudre :**
```bash
# Attendre que l'autre opération se termine
# OU si tu es sûr que personne d'autre ne travaille dessus :
terraform force-unlock <ID_DU_LOCK>
# ⚠️ Uniquement si l'autre opération est bloquée/morte
```

---

### `Error: Cycle` — Dépendance circulaire

```
Error: Cycle: aws_security_group.web, aws_security_group.db
```

**Ce que ça veut dire :** Deux ressources dépendent l'une de l'autre, créant une boucle infinie. Terraform ne sait pas laquelle créer en premier.

**Comment résoudre :**
```bash
# Identifier la boucle dans ton code :
# Le SG "web" référence le SG "db", ET le SG "db" référence le SG "web"
# → Casser la boucle en utilisant des règles séparées (aws_security_group_rule)
#   au lieu de mettre les règles dans le bloc du Security Group
```

---

## Ansible

### `UNREACHABLE` — Impossible de se connecter

```
fatal: [13.38.42.100]: UNREACHABLE! => {
    "msg": "Failed to connect to the host via ssh"
}
```

**Ce que ça veut dire :** Ansible n'arrive pas à se connecter au serveur en SSH. Même causes que "Connection refused" / "Connection timed out".

**Comment résoudre :**
```bash
# 1. Tester la connexion SSH manuellement
ssh -i ~/devops-key.pem ubuntu@13.38.42.100
# Si ça marche → le problème est dans l'inventory Ansible (mauvais user, mauvaise clé)
# Si ça ne marche pas → problème réseau/AWS (voir section SSH)

# 2. Vérifier l'inventory
cat inventory.ini
# L'IP est correcte ? ansible_user est correct ? Le chemin de la clé est correct ?
```

---

### `MODULE FAILURE` — Un module Ansible a échoué

```
fatal: [13.38.42.100]: FAILED! => {
    "msg": "No package matching 'docker.io' is available"
}
```

**Ce que ça veut dire :** Le module Ansible (ici `apt`) a rencontré une erreur. Le message `msg` te dit exactement ce qui ne va pas.

**Comment résoudre :**
```bash
# Lire le message "msg" — c'est la réponse
# "No package matching" → le paquet n'existe pas (mauvais nom ou apt pas à jour)
# "Permission denied" → il manque become: true (sudo)
# "Could not find" → le fichier source (pour copy) n'existe pas sur ta machine

# Fix courant : ajouter update_cache: true dans la tâche apt
# (équivalent de apt update avant apt install)
```

---

## Base de données

### `FATAL: too many connections`

```
psycopg2.OperationalError: FATAL: too many connections for role "admin"
```

**Ce que ça veut dire :** PostgreSQL a atteint sa limite de connexions simultanées.

**Comment résoudre :**
```bash
# Voir combien de connexions sont ouvertes
psql -h <ENDPOINT_RDS> -U admin -d tasks -c "SELECT count(*) FROM pg_stat_activity;"

# QUICKFIX : augmenter max_connections dans les paramètres RDS
# FIX PERMANENT : les devs implémentent un connection pool (ticket)
```

---

### `Connection refused` vers la base de données

```
psycopg2.OperationalError: could not connect to server: Connection refused
    Is the server running on host "db" and accepting connections on port 5432?
```

**Ce que ça veut dire :** L'application ne peut pas se connecter à la base de données. Soit la DB ne tourne pas, soit le réseau bloque.

**Comment résoudre :**
```bash
# Dans Docker Compose :
docker compose ps
# Le service "db" est bien "Up" ? Si non → docker compose logs db

# Vérifier le DATABASE_URL
# L'host doit être le NOM DU SERVICE ("db"), pas "localhost"
# DATABASE_URL=postgresql://user:pass@db:5432/tasks  ← correct
# DATABASE_URL=postgresql://user:pass@localhost:5432/tasks  ← FAUX dans Docker

# Sur AWS (RDS) :
# Le Security Group du RDS autorise le port 5432 depuis le Security Group de l'EC2 ?
```

---

### `FATAL: password authentication failed`

```
FATAL: password authentication failed for user "admin"
```

**Ce que ça veut dire :** Le mot de passe dans le DATABASE_URL ne correspond pas à celui de la base.

**Comment résoudre :**
```bash
# Vérifier le mot de passe dans la variable d'environnement
echo $DATABASE_URL
# Le mot de passe dans l'URL doit correspondre à POSTGRES_PASSWORD dans docker-compose.yml
# Ou au master password défini lors de la création du RDS
```

---

## Kubernetes

### `CrashLoopBackOff`

```
NAME                       READY   STATUS             RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     CrashLoopBackOff   5          3m
```

**Ce que ça veut dire :** Le container démarre, crash, K8s le redémarre, il re-crash... en boucle. `BackOff` = K8s attend de plus en plus longtemps entre chaque tentative.

**Comment résoudre :**
```bash
# Étape 1 : les logs — la raison du crash est dedans
kubectl logs backend-6d4f5b7c9d-abc12
# Voir les logs du crash PRÉCÉDENT :
kubectl logs backend-6d4f5b7c9d-abc12 --previous

# Causes courantes :
# "ModuleNotFoundError" → dépendances pas installées dans l'image
# "connection refused" → la DB n'est pas accessible
# "Permission denied" → problème de droits dans le container
# Crash silencieux → probablement un OOM

# Étape 2 : les événements
kubectl describe pod backend-6d4f5b7c9d-abc12
# Regarder la section "Events" en bas
```

---

### `ImagePullBackOff`

```
NAME                       READY   STATUS             RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     ImagePullBackOff   0          2m
```

**Ce que ça veut dire :** K8s n'arrive pas à télécharger l'image Docker.

**Comment résoudre :**
```bash
kubectl describe pod backend-6d4f5b7c9d-abc12
# Chercher dans Events : "Failed to pull image"

# Causes :
# 1. Typo dans le nom de l'image → vérifier "image:" dans le YAML
# 2. L'image n'existe pas sur Docker Hub (ou le repo est privé)
# 3. Sur minikube, l'image est locale → minikube image load <image>
```

---

### `Pending` — Le pod ne démarre pas

```
NAME                       READY   STATUS    RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     Pending   0          5m
```

**Ce que ça veut dire :** K8s ne trouve pas de machine avec assez de ressources pour lancer le pod.

**Comment résoudre :**
```bash
kubectl describe pod backend-6d4f5b7c9d-abc12
# "Insufficient memory" → pas assez de RAM sur le node
# "Insufficient cpu" → pas assez de CPU
# "no nodes available" → aucun node dans le cluster

# Sur minikube :
minikube stop
minikube start --memory=4096 --cpus=2
```

---

### `OOMKilled` — Pod tué par manque de mémoire

```
State:          Terminated
Reason:         OOMKilled
Exit Code:      137
```

**Ce que ça veut dire :** Le container a dépassé la limite de mémoire définie dans le Deployment. K8s l'a tué (même principe que Docker exit 137).

**Comment résoudre :**
```bash
# Voir la limite actuelle
kubectl describe pod <pod>
# Chercher "Limits: memory:"

# Augmenter la limite dans le YAML du Deployment :
#   resources:
#     limits:
#       memory: "512Mi"    ← augmenter cette valeur
#     requests:
#       memory: "256Mi"

# Si la mémoire monte sans cesse → fuite mémoire (ticket pour les devs)
```

---

## Récap — Le réflexe face à n'importe quelle erreur

```
1. LIRE le message        → la réponse est souvent dedans
2. IDENTIFIER le composant → Linux ? Docker ? App ? DB ? Réseau ? CI/CD ? K8s ?
3. VÉRIFIER les logs       → docker logs, kubectl logs, GitHub Actions logs
4. CHERCHER le message     → Google, IA (opencode), Stack Overflow
5. QUICKFIX si urgent      → remettre la prod debout
6. FIX PERMANENT           → corriger la cause racine (ticket, PR, config)
7. DOCUMENTER              → post-mortem, mettre à jour le runbook
```
