# DevOps — De Zéro à Prêt pour l'Entretien

Un cursus pratique pour apprendre le DevOps. Pas de blabla, des analogies simples, des commandes copy-paste, et un projet fil rouge qu'on fait évoluer du début à la fin.

## Parcours d'apprentissage

```
Module 0: Prérequis (Git + WSL)
    │
    ▼
Module 1: Linux ──────────────────────────┐
    │                                      │
    ▼                                      │
Module 2: Réseau                           │
    │                                      │
    ▼                                      │
Module 3: Docker                           │
    │                                      │
    ▼                                      │
Module 4: CI/CD (GitHub Actions)           │
    │                                      │
    ▼                                      │
Module 5: AWS                              │
    │                                      │
    ▼                                      │
Module 6: Terraform                        │
    │                                      │
    ├──▶ Module 7: Ansible (optionnel)     │
    │                                      │
    ├──▶ Module 8: Kubernetes (optionnel)  │
    │                                      │
    ▼                                      │
Module 9: Monitoring (sensibilisation) ◀───┘
```

## Le projet fil rouge

Une **Task List** toute simple : frontend React + backend FastAPI. L'app elle-même est triviale — c'est l'infrastructure autour qui compte.

Le code est dans [`devops-project/`](devops-project/).

On la fait évoluer à chaque module :
- **Module 0-1 :** On la clone, on la lance en local
- **Module 3 :** On la dockerize
- **Module 4 :** On ajoute un pipeline CI/CD
- **Module 5 :** On la déploie sur AWS à la main
- **Module 6 :** On automatise l'infra avec Terraform
- **Module 7 :** On configure le serveur avec Ansible
- **Module 8 :** On l'orchestre avec Kubernetes
- **Module 9 :** On la monitore avec Prometheus + Grafana

## Comment utiliser ce cursus

1. Suis les modules **dans l'ordre** (chaque module dépend des précédents)
2. **Tape les commandes toi-même** — ne fais pas copier-coller sans lire
3. Quand tu es bloqué, regarde les 💡 indices avant de chercher sur Google
4. Après chaque module, fais le **Coin entretien** pour vérifier que tu as compris
5. Le [cheatsheet](cheatsheet.md) est ta référence rapide pour les commandes
6. Les [questions d'entretien](interview-questions.md) consolidées sont ta révision finale

## Environnement requis

- Windows avec WSL2 + Ubuntu (voir [Module 0](00-prerequisites.md))
- VS Code avec l'extension Remote WSL
- Un compte GitHub
- Connexion internet

## Modules

| # | Module | Fichier | Obligatoire |
|---|--------|---------|-------------|
| 0 | Prérequis | [00-prerequisites.md](00-prerequisites.md) | ✅ |
| 1 | Linux | [01-linux-basics.md](01-linux-basics.md) | ✅ |
| 2 | Réseau | [02-networking.md](02-networking.md) | ✅ |
| 3 | Docker | [03-docker.md](03-docker.md) | ✅ |
| 4 | CI/CD | [04-cicd.md](04-cicd.md) | ✅ |
| 5 | AWS | [05-aws.md](05-aws.md) | ✅ |
| 6 | Terraform | [06-terraform.md](06-terraform.md) | ✅ |
| 7 | Ansible | [07-ansible.md](07-ansible.md) | Optionnel |
| 8 | Kubernetes | [08-kubernetes.md](08-kubernetes.md) | Optionnel |
| 9 | Monitoring | [09-monitoring.md](09-monitoring.md) | Sensibilisation |

## Ressources transversales

- [Cheatsheet](cheatsheet.md) — toutes les commandes clés en un fichier
- [Questions d'entretien](interview-questions.md) — Q&A consolidées par module
