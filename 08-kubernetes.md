# Module 8 : Kubernetes (Optionnel)

## C'est quoi Kubernetes et pourquoi ça existe ?

**Le problème :** Tu as 1 serveur avec docker-compose, ça marche. Mais si tu as 50 containers sur 10 serveurs ? Qui redémarre un container qui crash à 3h du matin ? Qui répartit le traffic entre les containers ? Qui fait un deployment sans downtime ?

**Kubernetes (K8s)** est le chef d'orchestre qui gère tout ça automatiquement. Tu lui dis "je veux 3 instances de mon backend", et il se débrouille : où les placer, les redémarrer si elles crashent, répartir le traffic.

**Les analogies (restaurant) :**
- **Pod** = un cuisinier à son poste
- **Deployment** = "garde toujours 3 cuisiniers pasta en service"
- **Service** = le serveur qui route les commandes aux bons cuisiniers
- **Node** = une cuisine (un serveur physique/virtuel)
- Un cuisinier tombe malade ? Le manager en embauche un nouveau automatiquement.

## Architecture (simplifiée)

```
┌─── Control Plane (le cerveau) ─────────────────┐
│  API Server    = le réceptionniste              │
│  Scheduler     = celui qui assigne les tâches   │
│  etcd          = le carnet d'adresses           │
│  Controller    = celui qui vérifie que tout va   │
└─────────────────────────────────────────────────┘
        │
        ├── Node 1 (une machine)
        │   ├── Pod (backend)
        │   └── Pod (frontend)
        │
        └── Node 2 (une machine)
            ├── Pod (backend)
            └── Pod (backend)
```

- **Control Plane** : décide OÙ placer les pods, surveille tout
- **Node** : une machine qui fait tourner les pods
- **kubelet** : l'agent sur chaque node qui communique avec le control plane

## Installation (minikube)

Minikube crée un cluster Kubernetes local (un seul node) pour apprendre.

```bash
# Installer kubectl (le client)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
# Client Version: v1.x.x

# Installer minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Lancer le cluster
minikube start
# 🎉  minikube v1.x.x
# ✅  Using the docker driver
# 🏄  Done! kubectl is now configured to use "minikube"

kubectl get nodes
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   1m    v1.x.x
```

## Les objets Kubernetes

### Pod

L'unité de base. Un pod = un ou plusieurs containers qui tournent ensemble. En pratique, 1 pod = 1 container.

```yaml
# pod.yml (on n'en crée presque jamais directement)
apiVersion: v1
kind: Pod
metadata:
  name: mon-backend
spec:
  containers:
    - name: backend
      image: mon-user/devops-backend:latest
      ports:
        - containerPort: 8000
```

### Deployment

Gère un groupe de pods identiques. Si un pod crash → il en recrée un. Si tu veux 3 replicas → il en maintient 3.

```yaml
# backend-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: mon-user/devops-backend:latest
          ports:
            - containerPort: 8000
```

### Service

Expose les pods sur le réseau. Même si les pods meurent et sont recréés (avec de nouvelles IPs), le Service garde une adresse stable.

```yaml
# backend-service.yml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP
```

| Type de Service | C'est quoi |
|----------------|-----------|
| **ClusterIP** | Accessible uniquement dans le cluster (défaut) |
| **NodePort** | Accessible depuis l'extérieur via un port sur le node |
| **LoadBalancer** | Crée un load balancer externe (cloud) |

### ConfigMap et Secret

```yaml
# ConfigMap = config non sensible
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"

# Secret = config sensible (encodé en base64)
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: bW9ucGFzcw==  # base64 de "monpass"
```

## Commandes kubectl essentielles

```bash
# Appliquer un fichier YAML
kubectl apply -f backend-deployment.yml

# Voir les pods
kubectl get pods
# NAME                       READY   STATUS    RESTARTS   AGE
# backend-6d4f5b7c9d-abc12   1/1     Running   0          1m
# backend-6d4f5b7c9d-def34   1/1     Running   0          1m

# Voir les deployments
kubectl get deployments

# Voir les services
kubectl get services

# Détails sur un pod
kubectl describe pod backend-6d4f5b7c9d-abc12

# Voir les logs
kubectl logs backend-6d4f5b7c9d-abc12

# Supprimer
kubectl delete -f backend-deployment.yml

# Scaler
kubectl scale deployment backend --replicas=5
```

## Namespaces

Un namespace isole les ressources dans le cluster (comme des dossiers). Par défaut, tout est dans le namespace `default`.

```bash
kubectl get namespaces
kubectl get pods -n kube-system  # Voir les pods système
```

## Projet pratique : Déployer sur minikube

### 1. Créer les fichiers

```bash
mkdir -p ~/devops-k8s
cd ~/devops-k8s
```

### 2. Backend Deployment + Service

Crée `backend.yml` :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: mon-user/devops-backend:latest
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 8000
      targetPort: 8000
  type: NodePort
```

### 3. Frontend Deployment + Service

Crée `frontend.yml` :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: mon-user/devops-frontend:latest
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
  type: NodePort
```

### 4. Déployer

```bash
kubectl apply -f backend.yml
kubectl apply -f frontend.yml

kubectl get pods
# NAME                        READY   STATUS    RESTARTS   AGE
# backend-xxx-abc12           1/1     Running   0          30s
# backend-xxx-def34           1/1     Running   0          30s
# frontend-xxx-ghi56          1/1     Running   0          25s
# frontend-xxx-jkl78          1/1     Running   0          25s

kubectl get services
# NAME               TYPE       CLUSTER-IP      PORT(S)
# backend-service    NodePort   10.96.x.x       8000:3xxxx/TCP
# frontend-service   NodePort   10.96.x.x       80:3yyyy/TCP
```

### 5. Accéder à l'app

```bash
minikube service frontend-service --url
# http://192.168.49.2:3yyyy
# Ouvre cette URL dans ton navigateur
```

### 6. Scaler et observer

```bash
# Passer de 2 à 5 replicas
kubectl scale deployment backend --replicas=5
kubectl get pods
# 5 pods backend !

# Supprimer un pod (K8s en recrée un automatiquement)
kubectl delete pod backend-xxx-abc12
kubectl get pods
# Toujours 5 pods — K8s a recréé le pod manquant

# Rolling update (changer l'image)
kubectl set image deployment/backend backend=mon-user/devops-backend:v2
kubectl rollout status deployment/backend
# Waiting for deployment "backend" rollout to finish...
# deployment "backend" successfully rolled out
```

### 7. Nettoyer

```bash
kubectl delete -f backend.yml
kubectl delete -f frontend.yml
minikube stop
```

## Coin entretien

**Q : C'est quoi Kubernetes ?**
R : Un orchestrateur de containers. Il gère le deployment, le scaling, et la high availability des applications containerisées sur un cluster de machines.

**Q : Différence entre Docker et Kubernetes ?**
R : Docker fait tourner UN container. Kubernetes orchestre des DIZAINES/CENTAINES de containers sur plusieurs machines (scheduling, scaling, self-healing).

**Q : C'est quoi un Pod ?**
R : L'unité de base dans K8s. Un pod contient un ou plusieurs containers qui partagent le même réseau et stockage. En pratique, 1 pod = 1 container.

**Q : C'est quoi un Deployment ?**
R : Un objet qui gère un groupe de pods identiques. Il maintient le nombre de replicas voulu, gère les updates (rolling update), et recrée les pods qui crashent.

**Q : C'est quoi un Service ?**
R : Un point d'accès réseau stable vers un groupe de pods. Les pods ont des IPs éphémères, le Service a une IP fixe et répartit le traffic.

**Q : Comment K8s gère un pod qui crash ?**
R : Le Controller détecte que le nombre de replicas ne correspond plus au nombre voulu, et recrée automatiquement un pod pour compenser (self-healing).

**Q : C'est quoi un Namespace ?**
R : Un moyen d'isoler les ressources dans un cluster. Utile pour séparer les environnements (dev, staging, prod) ou les équipes.

## Bonnes pratiques

- **Déclare les ressources (CPU/RAM).** Sans `resources.requests` et `resources.limits`, un pod peut consommer tout le node et faire crasher les autres. Toujours définir des limites.
- **Utilise des health checks.** `readinessProbe` (le pod est prêt à recevoir du traffic ?) et `livenessProbe` (le pod est encore vivant ?). Sans ça, K8s envoie du traffic à des pods qui ne sont pas prêts.
- **Ne déploie jamais `:latest`.** Tag tes images avec un hash de commit ou un numéro de version. `:latest` change sans prévenir, et tu ne peux pas faire de rollback propre.
- **Un namespace par environnement.** `dev`, `staging`, `prod`. Ça isole les ressources et évite de supprimer la prod par erreur.
- **Stocke tes YAML dans Git.** Les fichiers de deployment K8s sont du code — ils doivent être versionnés, reviewés en PR, et jamais appliqués à la main en prod.

## Erreurs courantes

- **Image pas trouvée** → Vérifie le nom de l'image dans le YAML. Si c'est une image locale, utilise `minikube image load`.
- **CrashLoopBackOff** → Le container crash en boucle. `kubectl logs POD` pour voir l'erreur.
- **Pending** → Pas assez de ressources sur le node. Réduis les replicas ou les resource requests.
- **Oublier le selector** → Le Service ne trouve pas les pods. Les labels dans le Deployment doivent matcher le selector du Service.

## Pour aller plus loin

- **Helm** : gestionnaire de packages pour K8s (comme apt mais pour les deployments K8s)
- **Ingress** : routage HTTP (un seul point d'entrée pour plusieurs services, avec des noms de domaine)
- **EKS / GKE** : Kubernetes managé par AWS / Google (pas besoin de gérer le control plane)
- **K3s** : version légère de K8s (idéal pour les petits serveurs, IoT, edge)
- **CKA** : Certified Kubernetes Administrator, la certification de référence
- **Service Mesh (Istio)** : gestion avancée du traffic entre services
