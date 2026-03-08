# Cheatsheet DevOps

## Git

| Commande | Description |
|----------|------------|
| `git init` | Initialiser un repo |
| `git add .` | Tout ajouter au staging |
| `git commit -m "msg"` | Committer |
| `git push` | Pousser sur le remote |
| `git pull` | Récupérer depuis le remote |
| `git branch nom` | Créer une branche |
| `git checkout -b nom` | Créer et aller sur une branche |
| `git merge nom` | Fusionner une branche |
| `git status` | Voir l'état |
| `git log --oneline` | Historique compact |

## Linux

| Commande | Description |
|----------|------------|
| `pwd` | Afficher le répertoire courant |
| `ls -la` | Lister tout (fichiers cachés inclus) |
| `cd chemin` | Se déplacer |
| `mkdir -p a/b/c` | Créer des dossiers récursifs |
| `cp -r src dest` | Copier (récursif) |
| `mv src dest` | Déplacer / renommer |
| `rm -r dossier` | Supprimer (récursif) |
| `chmod 755 fichier` | Changer les permissions |
| `chown user:group fichier` | Changer le propriétaire |
| `cat fichier` | Lire un fichier |
| `grep -r "texte" dossier/` | Chercher du texte |
| `find . -name "*.py"` | Chercher des fichiers |
| `ps aux` | Lister les processus |
| `kill PID` | Tuer un processus |
| `sudo apt update && sudo apt install -y pkg` | Installer un paquet |
| `systemctl start/stop/status svc` | Gérer un service |

## Réseau

| Commande | Description |
|----------|------------|
| `ping host` | Tester la connectivité |
| `curl URL` | Requête HTTP |
| `curl -I URL` | Voir les headers |
| `dig +short domaine` | Résoudre un DNS |
| `ss -tlnp` | Ports ouverts |
| `traceroute host` | Chemin réseau |
| `sudo ufw allow PORT` | Ouvrir un port |
| `sudo ufw enable` | Activer le firewall |
| `sudo ufw status` | Voir les règles |

## Docker

| Commande | Description |
|----------|------------|
| `docker build -t nom:tag .` | Construire une image |
| `docker run -d -p 8000:8000 --name c img` | Lancer un container |
| `docker ps` | Containers en cours |
| `docker ps -a` | Tous les containers |
| `docker stop nom` | Arrêter |
| `docker rm nom` | Supprimer le container |
| `docker rmi img` | Supprimer l'image |
| `docker logs -f nom` | Suivre les logs |
| `docker exec -it nom bash` | Entrer dans un container |
| `docker compose up -d --build` | Lancer avec Compose |
| `docker compose down` | Tout arrêter |
| `docker compose logs -f` | Logs de tous les services |

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
| Secret | `${{ secrets.NOM }}` |
| Dépendance entre jobs | `needs: job_name` |
| Condition | `if: github.ref == 'refs/heads/main'` |

## AWS CLI

| Commande | Description |
|----------|------------|
| `aws configure` | Configurer les credentials |
| `aws ec2 describe-instances` | Lister les instances |
| `aws ec2 start-instances --instance-ids ID` | Démarrer |
| `aws ec2 stop-instances --instance-ids ID` | Arrêter |
| `aws ec2 terminate-instances --instance-ids ID` | Supprimer |
| `aws s3 mb s3://bucket` | Créer un bucket |
| `aws s3 cp file s3://bucket/` | Upload |
| `aws s3 ls s3://bucket/` | Lister |
| `aws rds describe-db-instances` | Lister les bases RDS |
| `aws rds delete-db-instance --db-instance-identifier ID --skip-final-snapshot` | Supprimer une base RDS |
| `aws lambda list-functions` | Lister les fonctions Lambda |
| `aws lambda invoke --function-name NAME output.json` | Invoquer une Lambda |
| `aws lambda delete-function --function-name NAME` | Supprimer une Lambda |

## Terraform

| Commande | Description |
|----------|------------|
| `terraform init` | Initialiser (télécharger providers) |
| `terraform plan` | Prévisualiser |
| `terraform apply` | Appliquer |
| `terraform destroy` | Tout supprimer |
| `terraform fmt` | Formater le code |
| `terraform validate` | Vérifier la syntaxe |
| `terraform state list` | Voir les ressources gérées |

## Ansible

| Commande | Description |
|----------|------------|
| `ansible -i inv hosts -m ping` | Tester la connexion |
| `ansible-playbook -i inv playbook.yml` | Lancer un playbook |
| `ansible-playbook -i inv pb.yml --check` | Dry run |
| `ansible-vault encrypt fichier` | Chiffrer un fichier |

## Kubernetes (kubectl)

| Commande | Description |
|----------|------------|
| `kubectl apply -f file.yml` | Appliquer une config |
| `kubectl get pods` | Lister les pods |
| `kubectl get services` | Lister les services |
| `kubectl get deployments` | Lister les deployments |
| `kubectl describe pod NOM` | Détails d'un pod |
| `kubectl logs NOM` | Voir les logs |
| `kubectl delete -f file.yml` | Supprimer |
| `kubectl scale deployment NOM --replicas=N` | Scaler |
| `kubectl rollout status deployment/NOM` | Suivre un deployment |
| `minikube start` | Lancer le cluster local |
| `minikube service NOM --url` | Obtenir l'URL d'un service |

## Monitoring

| Commande / URL | Description |
|----------------|------------|
| `http://localhost:9090` | Prometheus UI |
| `http://localhost:3001` | Grafana UI |
| `rate(metric[1m])` | Taux par seconde (PromQL) |
| `histogram_quantile(0.95, ...)` | Percentile 95 (PromQL) |
