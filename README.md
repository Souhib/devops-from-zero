# DevOps — De Zéro à Prêt pour l'Entretien

Un cursus pratique pour apprendre le DevOps. Pas de blabla, des analogies simples, des commandes copy-paste, et un projet fil rouge qu'on fait évoluer du début à la fin.

## C'est quoi le DevOps ?

Dans le monde du logiciel, il y a généralement trois grands domaines :

- **Frontend** — ce que l'utilisateur voit et touche : les boutons, les pages, le design. Le développeur frontend écrit le code qui tourne dans ton navigateur (ou ton appli mobile). Technologies : React, Vue, HTML/CSS, etc.
- **Backend** — ce qui tourne sur le serveur, derrière l'écran. Le coeur du backend, c'est l'**API** : un programme qui tourne 24h/24 sur un serveur et qui reçoit des messages du frontend. Quand tu ouvres ton panier, le frontend envoie un message à l'API ("donne-moi le panier de cet utilisateur"), l'API va chercher les données dans la base de données et les renvoie au frontend qui les affiche. Quand tu cliques sur "Valider ma commande", le frontend envoie un autre message à l'API, et c'est l'API qui traite la demande : elle vérifie le panier, débite la carte, enregistre la commande en base de données, et répond au frontend "c'est bon, commande validée". Technologies : Python, Java, Go, Node.js, etc.
- **DevOps** — tout ce qu'il y a entre le code et l'utilisateur final. Le code est écrit, ok — mais comment on le teste automatiquement ? Comment on le met en ligne ? Sur quel serveur ? Comment on sait que ça marche ? Comment on gère 10 000 utilisateurs en même temps ? **C'est le DevOps.**

Concrètement, le DevOps c'est le métier de **construire et maintenir l'infrastructure** qui permet au code de tourner en production. Tu ne codes pas l'application — tu fais en sorte qu'elle soit livrée, déployée, surveillée, et qu'elle tienne la charge.

### Pourquoi c'est un bon choix pour se lancer

En frontend, on te demandera souvent de comprendre le backend et d'avoir un bon sens du design/UX. En backend, on attendra de toi que tu saches aussi faire du frontend basique et parfois du DevOps. Ces deux domaines ont des frontières floues — tu finis vite par porter plusieurs casquettes.

**Le DevOps, c'est un domaine à part.** En entreprise, on ne va pas te demander de coder des features frontend ou de designer des pages. Ton périmètre est clair : l'infrastructure, le déploiement, l'automatisation, le monitoring. Tu peux te concentrer sur un seul domaine et devenir opérationnel rapidement.

C'est aussi un domaine où il y a beaucoup de demande, et les compétences de base (Linux, Docker, CI/CD, Cloud) s'apprennent en quelques semaines avec de la pratique. Ce cursus est fait pour ça.

## Parcours d'apprentissage

```
Module 0 (Git + WSL) ─▶ Module 1 (Linux) ─▶ Module 2 (Réseau) ─▶ Module 3 (Docker)
                                                                        │
                                             ┌──────────────┬───────────┼──────────────┐
                                             ▼              ▼           ▼              ▼
                                       Module 4        Module 8    Module 9       (tous les
                                       (CI/CD)         (K8s)       (Monitoring)    modules
                                             │         optionnel   sensibilisation  suivants)
                                             ▼
                                       Module 5
                                       (AWS)
                                             │
                                             ▼
                                       Module 6
                                       (Terraform)
                                             │
                                             ▼
                                       Module 7
                                       (Ansible)
                                       optionnel
```

**Légende :** Les flèches montrent les dépendances. Module 3 (Docker) est le carrefour — il débloque CI/CD, K8s, et Monitoring. Les modules 7, 8 et 9 sont optionnels/sensibilisation.

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

## Combien de temps ça prend ?

Si tu y consacres environ **1h tous les 2 jours**, tu peux terminer le cursus en **6 à 8 semaines**. Ce n'est pas une course — mieux vaut aller doucement et comprendre que tout survoler.

Mais la formation n'est que le début. Le monde DevOps a **énormément de technologies** et ça évolue en permanence. Ce cursus te donne les bases solides (Docker, CI/CD, AWS, Terraform, monitoring) — c'est suffisant pour décrocher un premier poste. Mais tu devras continuer à pratiquer et à découvrir d'autres outils au fil du temps. Voir [Après la formation — Aller plus loin](aller-plus-loin.md).

Ce qui va te prendre le plus de temps, ce n'est pas la formation — c'est **trouver un emploi**. C'est pour ça qu'il ne faut pas attendre la fin du cursus pour commencer à préparer ton CV et ton LinkedIn. Contacte [Souhib TRABELSI](https://www.linkedin.com/in/souhib-trabelsi/) **avant la fin de la formation** pour qu'il t'aide à construire ton profil (LinkedIn, CV, préparation aux entretiens). Avec son accompagnement, ça peut aller beaucoup plus vite.

> **Exemple de CV :** [CV Souhib TRABELSI](assets/cv-exemple-souhib-trabelsi.pdf) — c'est un profil de développeur backend, mais tu y retrouves énormément de DevOps (Docker, Terraform, Ansible, AWS, CI/CD, ECS) car comme expliqué plus haut, backend et DevOps sont très liés. C'est juste un exemple pour voir comment structurer un CV technique — adapte-le à ton propre parcours et à un poste DevOps.

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

## Journée type d'un DevOps

> Cette question revient souvent en entretien : "C'est quoi concrètement le métier ?"

**Le matin :**
- Vérifier les **dashboards** (Grafana, Datadog) — est-ce que tout tourne bien ? Des errors cette nuit ?
- Lire les **alerts** reçues pendant la nuit — trier entre le bruit et les vrais problèmes
- Regarder les **pull requests** en attente — review de code, surtout les changements d'infra (Terraform, Dockerfiles, CI/CD)

**En journée :**
- **Améliorer l'infra** — optimiser un pipeline CI/CD trop lent, upgrader une version de Kubernetes, migrer un service vers un nouveau provider
- **Aider les devs** — "mon container crash", "le deployment ne marche pas", "comment je configure la variable d'env en staging ?"
- **Écrire du code d'infra** — Terraform pour un nouveau service, un playbook Ansible, un nouveau workflow GitHub Actions
- **Automatiser** — tout ce qui est fait à la main plus de 2 fois doit être scripté

**Quand ça va mal (incident) :**
- Diagnostiquer : logs, metrics, traces
- Corriger en urgence (rollback, restart, scale up)
- Communiquer avec l'équipe (status page, Slack)
- Écrire un **post-mortem** après l'incident (qu'est-ce qui s'est passé, comment éviter que ça se reproduise)

**Les compétences clés au quotidien :**

| Compétence | Pourquoi |
|------------|----------|
| Linux + terminal | Tu vis dans le terminal |
| Docker + containers | Tout tourne en containers |
| CI/CD | Tu construis et maintiens les pipelines |
| Cloud (AWS/GCP/Azure) | L'infra est dans le cloud |
| IaC (Terraform) | L'infra est du code |
| Monitoring | Tu dois savoir si ça marche |
| Communication | Tu es le lien entre les devs et la prod |

## Ressources

- [Cheatsheet](cheatsheet.md) — toutes les commandes clés en un fichier
- [Après la formation — Aller plus loin](aller-plus-loin.md) — outils à découvrir après le cursus + tableau des équivalents

## Préparer ton entretien

En entretien DevOps, il y a 3 types de questions. Pratique-les **dans cet ordre** :

| Étape | Type de question | Ressource |
|-------|-----------------|-----------|
| **1. Définitions** | "C'est quoi un container Docker ?", "C'est quoi le state Terraform ?" | [Questions d'entretien](interview-questions.md) (Partie 1) |
| **2. Expérience** | "Raconte-moi un incident en prod", "Comment tu gères un rollback ?" | [Questions d'expérience](interview-experience.md) (contexte QuickBite) |
| **3. System design** | "Comment tu déploierais cette app pour 50 000 utilisateurs ?" | [Exercices system design](system-design-exercises.md) (5 scénarios) |

Les [mises en situation](interview-questions.md) (Partie 2) mélangent les 3 types — à pratiquer après les 3 étapes.
