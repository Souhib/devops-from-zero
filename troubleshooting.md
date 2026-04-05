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
# LISTEN  0  128  0.0.0.0:8000  ...  users:(("docker-proxy",pid=1234,...))

# Si c'est un ancien container Docker
docker ps -a | grep 8000
docker stop <nom_du_container>
docker rm <nom_du_container>

# Si c'est un processus local (uvicorn lancé manuellement par exemple)
kill <PID>
```

---

### `Exited (137)` — Container tué (Out Of Memory)

```
CONTAINER ID  IMAGE       STATUS                      NAMES
abc123        mon-app     Exited (137) 2 minutes ago  backend
```

**Ce que ça veut dire :** Le code de sortie `137` signifie que le container a été tué par le système parce qu'il utilisait trop de mémoire (OOM = Out Of Memory). C'est Linux qui le tue, pas Docker.

**Comment résoudre :**
```bash
# Vérifier la consommation mémoire des containers
docker stats
# CONTAINER  CPU %  MEM USAGE / LIMIT
# backend    2%     450MiB / 512MiB     ← presque à la limite !

# Solutions :
# 1. Augmenter la limite mémoire dans docker-compose.yml :
#    deploy:
#      resources:
#        limits:
#          memory: 1024M
#
# 2. Si la mémoire monte sans arrêter → c'est une fuite mémoire dans le code
#    → remonter aux devs avec les métriques (graphe Grafana de la RAM)
```

---

### `no matching manifest for linux/arm64` (Mac M1/M2/M3)

```
no matching manifest for linux/arm64/v8 in the manifest list entries
```

**Ce que ça veut dire :** L'image Docker est faite pour les processeurs Intel (x86), mais ton Mac a un processeur ARM (Apple Silicon). L'image n'est pas compatible.

**Comment résoudre :**
```bash
# Forcer le build pour la plateforme Intel
docker build --platform linux/amd64 -t mon-app .

# Ou dans docker-compose.yml, ajouter :
#   services:
#     backend:
#       platform: linux/amd64
```

> Ce problème n'arrive pas sur WSL/Linux (processeur Intel). Tu le croiseras si tu travailles sur Mac.

---

## Terraform

### `Error: No valid credential sources found`

```
Error: error configuring Terraform AWS Provider: no valid credential sources found
```

**Ce que ça veut dire :** Terraform ne trouve pas tes identifiants AWS. Il ne sait pas QUEL compte AWS utiliser.

**Comment résoudre :**
```bash
# Vérifier que tes credentials sont configurées
aws configure list
# Si "access_key" et "secret_key" sont vides → reconfigurer :
aws configure
# Entrer ton Access Key ID et Secret Access Key (créés dans IAM)
```

---

### `Error: resource already exists`

```
Error: creating EC2 Instance: InvalidParameterValue:
  An instance with the name 'devops-server' already exists
```

**Ce que ça veut dire :** Terraform essaie de créer une ressource qui existe déjà sur AWS (créée à la main ou par un ancien `apply`).

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
  Path:      terraform.tfstate
  Operation: OperationTypeApply
  Who:       user@machine
```

**Ce que ça veut dire :** Quelqu'un d'autre (ou toi-même dans un autre terminal) est en train de faire un `terraform apply` en même temps. Terraform verrouille le state pour éviter les conflits.

**Comment résoudre :**
```bash
# Attendre que l'autre opération se termine
# OU si tu es sûr que personne d'autre ne travaille dessus :
terraform force-unlock <ID_DU_LOCK>
# ⚠️ Ne fais ça que si tu es CERTAIN que l'autre opération est bloquée/morte
```

---

## Kubernetes

### `CrashLoopBackOff`

```
NAME                       READY   STATUS             RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     CrashLoopBackOff   5          3m
```

**Ce que ça veut dire :** Le container démarre, crash, Kubernetes le redémarre, il re-crash, Kubernetes le re-redémarre... en boucle. `BackOff` = Kubernetes attend de plus en plus longtemps entre chaque tentative.

**Comment résoudre :**
```bash
# Étape 1 : lire les logs — la raison du crash est dedans
kubectl logs backend-6d4f5b7c9d-abc12
# Si le pod a redémarré, voir les logs du crash PRÉCÉDENT :
kubectl logs backend-6d4f5b7c9d-abc12 --previous

# Étape 2 : les causes les plus courantes
# - "ModuleNotFoundError" → le Dockerfile n'installe pas les dépendances
# - "connection refused" → le backend essaie de se connecter à une DB qui n'existe pas
# - "Permission denied" → problème de droits dans le container
# - Crash silencieux → probablement un OOM (mémoire insuffisante)

# Étape 3 : voir les événements
kubectl describe pod backend-6d4f5b7c9d-abc12
# Regarder la section "Events" en bas — elle montre pourquoi le pod échoue
```

---

### `ImagePullBackOff`

```
NAME                       READY   STATUS             RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     ImagePullBackOff   0          2m
```

**Ce que ça veut dire :** Kubernetes n'arrive pas à télécharger l'image Docker. Il a essayé plusieurs fois et a abandonné.

**Comment résoudre :**
```bash
# Voir le message d'erreur détaillé
kubectl describe pod backend-6d4f5b7c9d-abc12
# Chercher dans Events : "Failed to pull image"

# Causes courantes :
# 1. Le nom de l'image est faux (typo)
#    → Vérifier le champ "image:" dans le YAML

# 2. L'image n'existe pas sur Docker Hub (ou le repo est privé)
#    → docker pull <image> pour tester manuellement

# 3. Tu es sur minikube et l'image est locale (pas sur Docker Hub)
#    → minikube image load mon-user/devops-backend:latest
```

---

### `Pending` — Le pod ne démarre pas

```
NAME                       READY   STATUS    RESTARTS   AGE
backend-6d4f5b7c9d-abc12   0/1     Pending   0          5m
```

**Ce que ça veut dire :** Kubernetes ne trouve pas de machine (node) avec assez de ressources pour lancer le pod.

**Comment résoudre :**
```bash
kubectl describe pod backend-6d4f5b7c9d-abc12
# Chercher dans Events :
# "Insufficient memory" → le node n'a pas assez de RAM
# "Insufficient cpu" → le node n'a pas assez de CPU
# "no nodes available" → aucun node dans le cluster

# Sur minikube : augmenter les ressources
minikube stop
minikube start --memory=4096 --cpus=2
```

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
# "ruff check failed" → le linter a trouvé des erreurs de style
# "FAILED tests/test_main.py" → un test a échoué
# "docker build failed" → erreur dans le Dockerfile
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

## SSH

### `Connection refused` vs `Connection timed out`

Ce sont **deux problèmes complètement différents** :

| Erreur | Ce que ça veut dire | Cause probable |
|--------|-------------------|----------------|
| `Connection refused` | La machine est joignable MAIS rien n'écoute sur ce port | Le service SSH n'est pas lancé, ou le port est faux |
| `Connection timed out` | La machine n'est PAS joignable du tout | Mauvaise IP, Security Group bloque le port 22, la machine est éteinte |

```bash
# Connection refused → vérifier que SSH tourne sur le serveur
# (si tu as un autre moyen d'accéder au serveur)
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
# La clé doit être en lecture seule pour toi. SSH refuse une clé trop permissive.

# 3. Le bon utilisateur ?
# Ubuntu → ubuntu
# Amazon Linux → ec2-user
# Debian → admin
```

---

## La base de données

### `FATAL: too many connections for role "admin"`

```
psycopg2.OperationalError: FATAL: too many connections for role "admin"
```

**Ce que ça veut dire :** PostgreSQL a atteint sa limite de connexions simultanées. Chaque requête de l'API ouvre une connexion — si elles ne sont pas fermées, elles s'accumulent.

**Comment résoudre :**
```bash
# Voir combien de connexions sont ouvertes
psql -h <ENDPOINT_RDS> -U admin -d tasks -c "SELECT count(*) FROM pg_stat_activity;"

# QUICKFIX : augmenter max_connections sur le RDS
# Console AWS → RDS → Parameter groups → modifier max_connections

# FIX PERMANENT : implémenter un connection pool dans le code (ticket pour les devs)
```

---

## Récap — Le réflexe face à n'importe quelle erreur

```
1. LIRE le message        → la réponse est souvent dedans
2. IDENTIFIER le composant → Docker ? App ? DB ? Réseau ? CI/CD ?
3. VÉRIFIER les logs       → docker logs, kubectl logs, GitHub Actions logs
4. CHERCHER le message     → Google, IA (opencode), Stack Overflow
5. QUICKFIX si urgent      → remettre la prod debout
6. FIX PERMANENT           → corriger la cause racine (ticket, PR, config)
7. DOCUMENTER              → post-mortem, mettre à jour le runbook
```
