# Module 7 : Ansible (Optionnel)

> **Prérequis :** Module 5 (AWS — avoir un EC2) ou Module 6 (Terraform — avoir créé un EC2 avec Terraform)

> **En résumé :** Terraform crée les serveurs, Ansible les configure. Tu apprends à automatiser l'installation de Docker, le clonage du projet et le lancement de l'app sur un serveur distant — le tout avec un seul fichier YAML et une commande.

## C'est quoi Ansible et pourquoi ça existe ?

**Le problème :** Terraform crée l'infra (le serveur existe). Mais qui installe Docker dessus ? Qui configure nginx ? Qui copie les fichiers de config ? Qui s'assure que tout est à jour ? Tu peux le faire en SSH, mais si tu as 10 serveurs ? 50 ?

**Ansible configure et maintient ce qui tourne SUR les serveurs.** Terraform construit la maison, Ansible la meuble.

**Les analogies :**
- **Inventory** = la liste des maisons à visiter
- **Playbook** = la checklist de tâches à faire dans chaque maison
- **Module** = une action spécifique (installer un logiciel, copier un fichier, démarrer un service)
- **Idempotence** = tu peux relancer la checklist 10 fois, le résultat sera le même (si la peinture est déjà faite, on ne repeint pas)

**Le truc clé :** Ansible est **agentless** — pas besoin d'installer quoi que ce soit sur les serveurs cibles. D'autres outils similaires (Chef, Puppet) nécessitent d'installer un programme ("agent") sur chaque serveur qu'on veut gérer. Ansible, non : il se connecte simplement en SSH (la connexion distante vue au Module 1) et exécute les tâches. C'est ce qui le rend simple à démarrer.

## Installation

```bash
sudo apt update && sudo apt install -y ansible

ansible --version
# ansible [core 2.x.x]
```

## Inventory — La liste des serveurs

L'inventory dit à Ansible quelles machines gérer.

Crée le fichier avec `nano inventory.ini` et copie ce contenu :
```ini
[web]
<IP_DE_TON_EC2> ansible_user=ubuntu ansible_ssh_private_key_file=~/devops-key.pem
# Remplace <IP_DE_TON_EC2> par l'IP publique de ton instance EC2 (ex: 13.38.42.100)
# ansible_user = avec quel utilisateur se connecter en SSH
# ansible_ssh_private_key_file = le fichier de clé SSH téléchargé lors de la création de l'EC2 (Module 5)
```

Vérifie la connexion :
```bash
ansible -i inventory.ini web -m ping
# -i = quel fichier inventory utiliser
# web = le groupe ciblé (défini entre [crochets] dans inventory.ini)
# -m ping = utiliser le module "ping" (teste la connexion SSH)
# 13.38.x.x | SUCCESS => {
#     "ping": "pong"
# }
```

## Playbook — La checklist

Un playbook est un fichier YAML qui décrit les tâches à exécuter.

Crée le fichier avec `nano setup.yml` et copie ce contenu :

```yaml
# setup.yml
---
- name: Configurer le serveur web
  hosts: web              # Le groupe de serveurs ciblé (défini dans inventory.ini)
  become: true            # Exécuter en tant qu'admin (sudo)

  tasks:
    - name: Mettre à jour les paquets
      apt:
        update_cache: true   # = apt update (rafraîchir la liste des paquets)
        upgrade: dist        # = apt upgrade (mettre à jour les paquets installés)

    - name: Installer Docker
      apt:
        name:
          - docker.io
          - docker-compose-v2
        state: present       # "present" = s'assurer que c'est installé (si déjà là, ne rien faire)

    - name: Ajouter ubuntu au groupe docker
      user:
        name: ubuntu
        groups: docker
        append: true         # Ajouter au groupe docker SANS retirer des autres groupes

    - name: Démarrer Docker
      service:
        name: docker
        state: started       # S'assurer que Docker tourne
        enabled: true        # Démarrer automatiquement au boot du serveur
```

Lancer le playbook :
```bash
ansible-playbook -i inventory.ini setup.yml
# -i = quel inventory utiliser
# setup.yml = le playbook à exécuter
```

Tu devrais voir quelque chose comme :
```
PLAY [Configurer le serveur web] ***
TASK [Mettre à jour les paquets] ***
changed: [13.38.x.x]           ← cette tâche a modifié quelque chose sur le serveur
TASK [Installer Docker] ***
changed: [13.38.x.x]
...
PLAY RECAP ***
13.38.x.x : ok=4  changed=4  unreachable=0  failed=0
```

**Ce que veut dire chaque ligne :**
- `PLAY [...]` = début d'un groupe de tâches
- `TASK [...]` = une tâche individuelle
- `changed` = la tâche a modifié quelque chose sur le serveur
- `ok` = la tâche a vérifié mais rien à changer (déjà fait)
- `ok=4 changed=4` = 4 tâches exécutées, 4 ont modifié quelque chose
- `failed=0` = aucune erreur

## Modules utiles

| Module | Ce que ça fait | Exemple |
|--------|---------------|---------|
| `apt` | Installer/supprimer des paquets | `apt: name=nginx state=present` |
| `copy` | Copier un fichier vers le serveur | `copy: src=app.conf dest=/etc/nginx/` |
| `template` | Copier un fichier avec des variables | `template: src=app.conf.j2 dest=/etc/nginx/` |
| `service` | Gérer un service (start/stop/restart) | `service: name=nginx state=started` |
| `file` | Créer des dossiers, changer les permissions | `file: path=/app state=directory` |
| `command` | Exécuter une commande | `command: docker compose up -d` |

## Idempotence — Le concept clé

Tu lances le playbook une première fois : Ansible installe Docker, copie les fichiers, démarre les services. Tu le relances : Ansible vérifie que tout est déjà fait et ne fait rien. **Même résultat, pas d'effets de bord.**

```bash
# Premier lancement
ansible-playbook -i inventory.ini setup.yml
# changed=4

# Deuxième lancement (rien ne change)
ansible-playbook -i inventory.ini setup.yml
# changed=0  ← idempotent !
```

## Variables et Roles (concepts)

**Variables :** Tu peux paramétrer tes playbooks.
```yaml
vars:
  app_port: 8000
  docker_image: "mon-user/devops-backend:latest"
```

**Roles :** Des playbooks réutilisables et organisés. Comme des fonctions. On n'en crée pas dans ce cours, mais sache que ça existe (et Ansible Galaxy en fournit des milliers prêts à l'emploi).

## Projet pratique : Provisionner le serveur EC2

On reprend le serveur créé dans le Module 5 ou 6, et on automatise sa configuration.

### 1. Structure

```bash
mkdir -p ~/devops-ansible
cd ~/devops-ansible
```

### 2. Inventory

Crée le fichier avec `nano inventory.ini` :
```ini
[web]
<IP_DE_TON_EC2> ansible_user=ubuntu ansible_ssh_private_key_file=~/devops-key.pem
# Remplace <IP_DE_TON_EC2> par l'IP publique de ton EC2
```

### 3. Playbook complet

Crée le fichier avec `nano deploy.yml` et copie ce contenu :

> **Les `{{ variable }}`** c'est la syntaxe Ansible pour insérer la valeur d'une variable. C'est comme `$variable` en bash ou `${var}` en Terraform — chaque outil a sa propre syntaxe.

```yaml
---
- name: Déployer le projet DevOps
  hosts: web
  become: true                  # Exécuter en tant qu'admin (sudo)

  vars:                         # Variables réutilisables dans les tâches ci-dessous
    github_repo: "https://github.com/<TON_USER_GITHUB>/devops-project.git"
    app_dir: /home/ubuntu/devops-project

  tasks:
    - name: Installer les dépendances
      apt:
        update_cache: true
        name:
          - docker.io
          - docker-compose-v2
          - git
        state: present

    - name: Ajouter ubuntu au groupe docker
      user:
        name: ubuntu
        groups: docker
        append: true

    - name: Démarrer Docker
      service:
        name: docker
        state: started
        enabled: true

    - name: Cloner le projet
      git:
        repo: "{{ github_repo }}"    # Utilise la variable définie dans "vars" ci-dessus
        dest: "{{ app_dir }}"        # Où cloner sur le serveur
        version: main                # La branche à cloner
        force: true                  # Écraser si le dossier existe déjà
      become_user: ubuntu            # Exécuter en tant que "ubuntu" (pas root) pour que les fichiers lui appartiennent

    - name: Lancer docker compose
      command: docker compose up -d --build
      args:
        chdir: "{{ app_dir }}"       # Se placer dans ce dossier avant d'exécuter la commande
      become_user: ubuntu
```

### 4. Lancer

```bash
ansible-playbook -i inventory.ini deploy.yml
# PLAY RECAP ***
# IP : ok=6  changed=6  unreachable=0  failed=0
```

Ouvre `http://IP_DE_TON_EC2` — l'app tourne.

💡 **Si "unreachable"** : vérifie que l'IP est bonne, que le Security Group autorise SSH (22), et que la clé `.pem` est correcte.

## Coin entretien

**Q : C'est quoi Ansible ?**
R : Un outil de gestion de configuration. Il configure des serveurs (installer des logiciels, copier des fichiers, démarrer des services) de manière automatisée et reproductible.

**Q : Ansible vs Terraform ?**
R : Terraform crée l'infrastructure (serveurs, réseaux). Ansible configure ce qui tourne dessus (logiciels, fichiers). Ils sont complémentaires.

**Q : C'est quoi l'idempotence ?**
R : La capacité d'exécuter une opération plusieurs fois avec le même résultat. Si Docker est déjà installé, Ansible ne le réinstalle pas.

**Q : Pourquoi Ansible est "agentless" ?**
R : Pas besoin d'installer un logiciel sur les serveurs cibles. Ansible se connecte en SSH. Ça simplifie la mise en place par rapport à Chef/Puppet qui nécessitent un agent.

**Q : C'est quoi un playbook ?**
R : Un fichier YAML qui décrit une liste de tâches à exécuter sur des serveurs. C'est le fichier principal qu'on écrit et qu'on lance.

## Bonnes pratiques

- **Utilise les modules Ansible, pas `command`/`shell`.** Les modules (`apt`, `service`, `copy`) sont idempotents. `command: apt install nginx` ne l'est pas — il va réinstaller à chaque exécution.
- **Teste avec `--check` d'abord.** `ansible-playbook --check` simule l'exécution sans rien modifier (dry run). Comme `terraform plan`.
- **Chiffre les secrets avec Ansible Vault.** Mots de passe, clés API → `ansible-vault encrypt secrets.yml`. Ne committe jamais de secrets en clair.
- **Organise en roles dès que ça grandit.** Un playbook de 500 lignes est inmaintenable. Les roles découpent en blocs réutilisables.

## Erreurs courantes

- **"Permission denied"** → Mauvaise clé SSH ou mauvais utilisateur dans l'inventory.
- **Oublier `become: true`** → Les tâches qui nécessitent sudo échouent.
- **Module `command` pas idempotent** → Préfère les modules Ansible dédiés (`apt`, `service`, etc.) qui gèrent l'idempotence.
- **Pas d'indentation correcte en YAML** → YAML est strict sur l'indentation (espaces, pas de tabs).

## Pour aller plus loin

- **Ansible Galaxy** : bibliothèque de roles communautaires (comme npm mais pour Ansible)
- **Ansible Tower / AWX** : interface web pour Ansible (gestion d'équipe, scheduling)
- **Chef / Puppet** : alternatives à Ansible (avec agent, plus complexes)
- **Ansible Vault** : chiffrer les secrets dans les playbooks

## Tu peux passer au module suivant si...

- [ ] Tu sais la différence entre Terraform (crée l'infra) et Ansible (configure l'infra)
- [ ] Tu sais écrire un inventory et un playbook basique
- [ ] Tu comprends l'idempotence (relancer = même résultat)
- [ ] Tu sais pourquoi Ansible est "agentless" (SSH, pas d'agent à installer)
- [ ] Tu as provisionné un EC2 avec le playbook `deploy.yml`
