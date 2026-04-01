# Cheatsheet DevOps

> **3 niveaux de fréquence :**
> - **quotidien** — tu tapes ça tous les jours, apprends-les par coeur. Si tu connais celles-là, tu t'en sors.
> - occasionnel — utile régulièrement, tu reviendras les chercher ici quand il faudra.
> - *rarement* — tu en auras besoin une ou deux fois, surtout pour le setup ou le nettoyage.

> **Les mots entre `<chevrons>` sont des placeholders** — remplace-les par ta propre valeur.
> Exemple : `git checkout -b <branche>` → `git checkout -b feature/login`

## Git

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `git status` | Voir l'état | **quotidien** |
| `git add .` | Tout ajouter au staging | **quotidien** |
| `git commit -m "<message>"` | Committer | **quotidien** |
| `git push` | Pousser sur le remote | **quotidien** |
| `git pull` | Récupérer depuis le remote | **quotidien** |
| `git checkout -b <branche>` | Créer et aller sur une branche | **quotidien** |
| `git log --oneline` | Historique compact | occasionnel |
| `git merge <branche>` | Fusionner une branche | occasionnel |
| `git init` | Initialiser un repo | *rarement* |
| `git branch <branche>` | Créer une branche (sans y aller) | *rarement* |

## Linux

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `ls -la` | Lister tout (fichiers cachés inclus) | **quotidien** |
| `cd <chemin>` | Se déplacer | **quotidien** |
| `cat <fichier>` | Lire un fichier | **quotidien** |
| `mkdir -p <chemin>` | Créer des dossiers récursifs | **quotidien** |
| `grep -r "<texte>" <dossier>/` | Chercher du texte | **quotidien** |
| `sudo apt update && sudo apt install -y <paquet>` | Installer un paquet (ex: `curl`, `git`) | **quotidien** |
| `pwd` | Afficher le répertoire courant | occasionnel |
| `nano <fichier>` | Éditer un fichier dans le terminal | occasionnel |
| `rm -r <dossier>` | Supprimer (récursif) | occasionnel |
| `cp -r <source> <destination>` | Copier (récursif) | occasionnel |
| `mv <source> <destination>` | Déplacer / renommer | occasionnel |
| `chmod 755 <fichier>` | Changer les permissions | occasionnel |
| `export <NOM_VARIABLE>="<valeur>"` | Définir une variable d'environnement | occasionnel |
| `ps aux` | Lister les processus | occasionnel |
| `kill <PID>` | Tuer un processus (`PID` = numéro affiché par `ps aux`) | occasionnel |
| `find . -name "*.py"` | Chercher des fichiers | *rarement* |
| `chown <user>:<group> <fichier>` | Changer le propriétaire | *rarement* |
| `systemctl start/stop/status <service>` | Gérer un service (ex: `nginx`, `docker`) | *rarement* |
| `whoami` | Afficher l'utilisateur courant | *rarement* |
| `printenv` | Lister les variables d'environnement | *rarement* |
| `journalctl -u <service>` | Voir les logs d'un service | *rarement* |

## Réseau

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `curl <URL>` | Requête HTTP (ex: `curl http://localhost:8000/api/tasks`) | **quotidien** |
| `ss -tlnp` | Ports ouverts | occasionnel |
| `ping <hôte>` | Tester la connectivité (ex: `ping google.com`) | occasionnel |
| `curl -I <URL>` | Voir les headers | occasionnel |
| `dig +short <domaine>` | Résoudre un DNS (ex: `dig +short google.com`) | *rarement* |
| `wget <URL>` | Télécharger un fichier | *rarement* |
| `hostname -I` | Voir son IP privée | *rarement* |
| `curl ifconfig.me` | Voir son IP publique | *rarement* |
| `traceroute <hôte>` | Chemin réseau | *rarement* |
| `sudo ufw allow <port>` | Ouvrir un port (ex: `sudo ufw allow 8000`) | *rarement* |
| `sudo ufw enable` | Activer le firewall | *rarement* |
| `sudo ufw status` | Voir les règles | *rarement* |

## HTTP Methods

| Méthode | Ce que ça fait | Exemple |
|---------|---------------|---------|
| `GET` | Lire une ressource | `curl http://localhost:8000/api/tasks` |
| `POST` | Créer une ressource | `curl -X POST -H "Content-Type: application/json" -d '{"title":"..."}' http://localhost:8000/api/tasks` |
| `PATCH` | Modifier une donnée existante | `curl -X PATCH http://localhost:8000/api/tasks/1` |
| `PUT` | Modifier une donnée existante | (non utilisé dans ce projet) |
| `DELETE` | Supprimer | `curl -X DELETE http://localhost:8000/api/tasks/1` |

> **PATCH vs PUT :** pour faire simple, les deux servent à **modifier une donnée qui existe déjà**. La différence technique : `PATCH` modifie seulement les champs envoyés, `PUT` remplace la ressource entièrement. En pratique, beaucoup d'APIs utilisent l'un ou l'autre sans distinction. Dans ce cursus on utilise `PATCH` — si tu vois `PUT` ailleurs, dis-toi que c'est la même idée.

## Docker

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `docker compose up -d --build` | Lancer avec Compose | **quotidien** |
| `docker compose down` | Tout arrêter | **quotidien** |
| `docker compose ps` | Voir l'état des services | **quotidien** |
| `docker compose logs -f` | Logs de tous les services | **quotidien** |
| `docker ps` | Containers en cours | **quotidien** |
| `docker logs -f <container>` | Suivre les logs d'un container | **quotidien** |
| `docker exec -it <container> bash` | Entrer dans un container | occasionnel |
| `docker build -t <nom>:<tag> .` | Construire une image (ex: `docker build -t mon-app:1.0 .`) | occasionnel |
| `docker stop <container>` | Arrêter un container | occasionnel |
| `docker rm <container>` | Supprimer le container | occasionnel |
| `docker ps -a` | Tous les containers (même arrêtés) | occasionnel |
| `docker run -d -p <port_machine>:<port_container> --name <nom> <image>` | Lancer un container sans Compose | *rarement* |
| `docker rmi <image>` | Supprimer l'image | *rarement* |
| `docker pull <image>` | Télécharger une image (ex: `docker pull postgres:16`) | *rarement* |
| `docker images` | Lister les images locales | *rarement* |
| `docker system df` | Voir l'espace utilisé par Docker | *rarement* |
| `docker system prune -a` | Nettoyer images/containers inutilisés | *rarement* |

## Bun (frontend)

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `bun install` | Installer les dépendances | **quotidien** |
| `bun run dev` | Lancer le serveur de dev | **quotidien** |
| `bun run build` | Compiler pour la production | occasionnel |
| `bunx oxlint .` | Lancer le linter | occasionnel |

> Bun remplace npm + Node.js. Les commandes équivalentes npm : `npm install`, `npm run dev`, `npx oxlint .`

## uv (backend Python)

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `uv sync` | Installer les dépendances | **quotidien** |
| `uv run uvicorn main:app --reload` | Lancer le serveur backend | **quotidien** |
| `uv run pytest` | Lancer les tests | **quotidien** |
| `uv run ruff check .` | Lancer le linter | occasionnel |
| `uv add <paquet>` | Ajouter une dépendance (ex: `uv add fastapi`) | *rarement* |

> uv remplace pip + venv. Les commandes équivalentes : `pip install -r requirements.txt`, `python -m pytest`

## GitHub Actions

```yaml
# Structure minimale
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello CI"
```

| Concept | Syntaxe |
|---------|---------|
| Secret | `${{ secrets.<NOM_DU_SECRET> }}` |
| Dépendance entre jobs | `needs: <nom_du_job>` |
| Condition | `if: github.ref == 'refs/heads/main'` |

## AWS CLI

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `aws ec2 describe-instances` | Lister les instances | **quotidien** |
| `aws ec2 stop-instances --instance-ids <ID>` | Arrêter (ex: `--instance-ids i-0abc123`) | **quotidien** |
| `aws ec2 start-instances --instance-ids <ID>` | Démarrer | **quotidien** |
| `aws s3 cp <fichier> s3://<bucket>/` | Upload | occasionnel |
| `aws s3 ls s3://<bucket>/` | Lister le contenu d'un bucket | occasionnel |
| `aws ec2 terminate-instances --instance-ids <ID>` | Supprimer définitivement | occasionnel |
| `aws configure` | Configurer les credentials | *rarement* |
| `aws s3 mb s3://<bucket>` | Créer un bucket | *rarement* |
| `aws rds describe-db-instances` | Lister les bases RDS | *rarement* |
| `aws rds delete-db-instance --db-instance-identifier <ID> --skip-final-snapshot` | Supprimer une base RDS | *rarement* |
| `aws lambda list-functions` | Lister les fonctions Lambda | *rarement* |
| `aws lambda invoke --function-name <NOM> output.json` | Invoquer une Lambda | *rarement* |
| `aws lambda delete-function --function-name <NOM>` | Supprimer une Lambda | *rarement* |

## Terraform

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `terraform plan` | Prévisualiser | **quotidien** |
| `terraform apply` | Appliquer | **quotidien** |
| `terraform init` | Initialiser (télécharger providers) | occasionnel |
| `terraform destroy` | Tout supprimer | occasionnel |
| `terraform fmt` | Formater le code | occasionnel |
| `terraform validate` | Vérifier la syntaxe | *rarement* |
| `terraform state list` | Voir les ressources gérées | *rarement* |

## Ansible

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `ansible-playbook -i <inventory> <playbook>.yml` | Lancer un playbook | **quotidien** |
| `ansible -i <inventory> <hosts> -m ping` | Tester la connexion | occasionnel |
| `ansible-playbook -i <inventory> <playbook>.yml --check` | Dry run | occasionnel |
| `ansible-vault encrypt <fichier>` | Chiffrer un fichier | *rarement* |

## Kubernetes (kubectl)

| Commande | Description | Fréquence |
|----------|------------|-----------|
| `kubectl get pods` | Lister les pods | **quotidien** |
| `kubectl get services` | Lister les services | **quotidien** |
| `kubectl logs <pod>` | Voir les logs | **quotidien** |
| `kubectl apply -f <fichier>.yml` | Appliquer une config | **quotidien** |
| `kubectl describe pod <pod>` | Détails d'un pod | occasionnel |
| `kubectl get deployments` | Lister les deployments | occasionnel |
| `kubectl delete -f <fichier>.yml` | Supprimer | occasionnel |
| `kubectl scale deployment <nom> --replicas=<N>` | Scaler (ex: `--replicas=3`) | occasionnel |
| `kubectl rollout status deployment/<nom>` | Suivre un deployment | *rarement* |
| `kubectl get namespaces` | Lister les namespaces | *rarement* |
| `kubectl set image deployment/<nom> <container>=<image>:<tag>` | Mettre à jour l'image | *rarement* |
| `minikube start` | Lancer le cluster local | *rarement* |
| `minikube stop` | Arrêter le cluster local | *rarement* |
| `minikube image load <image>` | Charger une image locale dans minikube | *rarement* |
| `minikube service <nom> --url` | Obtenir l'URL d'un service | *rarement* |

## Monitoring

| Commande / URL | Description | Fréquence |
|----------------|------------|-----------|
| `http://localhost:9090` | Prometheus UI | **quotidien** |
| `http://localhost:3001` | Grafana UI | **quotidien** |
| `curl http://localhost:8000/metrics` | Voir les métriques brutes | occasionnel |
| `rate(<métrique>[1m])` | Taux par seconde (PromQL) | *rarement* |
| `histogram_quantile(0.95, ...)` | Percentile 95 (PromQL) | *rarement* |
| `docker compose up -d` (avec prometheus.yml) | Lancer Prometheus + Grafana | *rarement* |
