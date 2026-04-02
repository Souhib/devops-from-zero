# Après la formation — Aller plus loin

Ce cursus te donne les bases pour décrocher un premier poste. Mais le DevOps est un domaine immense. Voici des outils et concepts que tu n'as **pas** vus dans la formation et que tu croiseras en entreprise.

## Accessible rapidement (après la formation)

| Outil | C'est quoi | Pourquoi c'est utile |
|-------|-----------|---------------------|
| **HashiCorp Vault** | Gestion centralisée des secrets (mots de passe, tokens, clés API) | En entreprise, les secrets ne sont pas dans des `.env` ou GitHub Secrets — ils sont dans Vault. C'est le standard |
| **Trivy / Snyk** | Scanners de vulnérabilités — ils analysent tes images Docker et tes dépendances pour trouver des failles de sécurité | De plus en plus demandé, s'intègre dans le pipeline CI/CD |
| **Datadog / New Relic** | Monitoring SaaS (tout-en-un, payant) — métriques, logs, traces dans une seule interface | Beaucoup d'entreprises utilisent ça au lieu de Prometheus + Grafana. Le concept est le même, juste l'outil change |
| **Loki** | Collecteur de logs par Grafana — comme ELK mais plus simple | Complète Prometheus (métriques) avec les logs centralisés |

## Niveau senior (tu les croiseras avec l'expérience)

| Outil | C'est quoi | Pourquoi c'est senior |
|-------|-----------|----------------------|
| **Helm** | Gestionnaire de packages pour Kubernetes — comme `apt` pour Linux mais pour K8s. Tu décris ton app dans un "chart" réutilisable | Nécessite de bien maîtriser K8s d'abord. Tu ne l'utiliseras que si ton entreprise fait du K8s en prod |
| **ArgoCD** | GitOps — le repo Git EST la source de vérité pour le déploiement. Tu push du YAML dans Git, ArgoCD le déploie automatiquement sur K8s | Très puissant mais complexe. Demande K8s + Helm + Git avancé |
| **Istio / Service Mesh** | Gère le traffic entre microservices (sécurité, observabilité, retry automatique) | Utile uniquement avec 10+ microservices. Over-kill sinon |
| **OpenTelemetry** | Standard pour les traces distribuées — suivre une requête de bout en bout à travers plusieurs services | Nécessite une architecture microservices pour avoir du sens |
| **Terragrunt** | Wrapper autour de Terraform pour gérer des dizaines de modules et d'environnements | Utile quand tu as une infra Terraform massive (5+ environnements, 20+ modules) |

> **Le conseil :** Ne te disperse pas. Apprends ces outils **quand tu en as besoin** (ton entreprise l'utilise, un projet le demande), pas "au cas où". Les bases de ce cursus te portent très loin. Le reste vient naturellement avec l'expérience.

## Les équivalents — "C'est la même chose, juste un autre nom"

En entreprise, tu tomberas sur des outils différents de ceux du cursus. Pas de panique — les concepts sont les mêmes, seul le nom change. Si tu maîtrises la colonne de gauche, tu peux apprendre la colonne de droite en quelques jours.

| Ce que tu connais (cursus) | Équivalent que tu croiseras | Ce qui change |
|---------------------------|---------------------------|---------------|
| **GitHub Actions** (CI/CD) | GitLab CI, Jenkins, CircleCI | La syntaxe du fichier YAML. Les concepts (jobs, steps, triggers) sont identiques |
| **AWS** (cloud) | GCP (Google), Azure (Microsoft) | Les noms des services changent (EC2 → Compute Engine, S3 → Cloud Storage, RDS → Cloud SQL). Les concepts sont les mêmes |
| **Terraform** (IaC) | OpenTofu (fork open-source), Pulumi (IaC en Python/TS), CloudFormation (IaC spécifique AWS) | Terraform et OpenTofu sont quasi identiques. Pulumi utilise un vrai langage au lieu de HCL. CloudFormation = même idée mais bloqué sur AWS |
| **Docker Compose** (orchestration locale) | Podman Compose, Docker Swarm | Podman = Docker sans daemon (plus sécurisé). Swarm = orchestration basique intégrée à Docker |
| **Prometheus + Grafana** (monitoring) | Datadog, New Relic, CloudWatch | Même concept (métriques + dashboards + alertes), mais en SaaS payant. Plus simple à setup, moins de contrôle |
| **Ansible** (configuration) | Chef, Puppet, SaltStack | Ansible = agentless (SSH). Chef/Puppet = agent installé sur chaque serveur. Même but : configurer des serveurs automatiquement |
| **GitHub** (hébergement code) | GitLab, Bitbucket | Git est le même partout. Seule l'interface web et les features intégrées changent (CI/CD, issues, etc.) |
