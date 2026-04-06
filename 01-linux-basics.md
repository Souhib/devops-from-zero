# Module 1 : Les Bases de Linux

> **Prérequis :** Module 0 (Git, WSL installé)

> **En résumé :** Tu apprends à naviguer dans un terminal Linux — fichiers, permissions, processus, variables d'environnement. C'est la base de tout ce qui suit : Docker, AWS, Ansible, Kubernetes tournent tous sur Linux.

## C'est quoi Linux et pourquoi ça existe ?

**Le problème :** 90%+ des serveurs dans le monde tournent sous Linux. Pas Windows, pas macOS — Linux. Si tu veux faire du DevOps, tu DOIS savoir naviguer dans un terminal Linux. C'est comme vouloir être cuisinier sans savoir utiliser un couteau.

**C'est quoi DevOps ?** C'est un métier (et une façon de travailler) qui fait le pont entre les développeurs (ceux qui écrivent le code) et les opérations (ceux qui gèrent les serveurs). Le DevOps automatise tout ce qui est entre "le code est écrit" et "l'app tourne en production pour les utilisateurs" : tests, déploiement, monitoring, infrastructure.

La seule chose à retenir : sur Linux, tout est organisé en dossiers à partir de `/` (la racine). Ton dossier personnel est `/home/ton_user` (ou `~` en raccourci). Le reste, tu le découvriras au fur et à mesure.

## Navigation

> **Essaie ces commandes dans ton terminal.** Tape-les une par une et regarde le résultat.

```bash
pwd
# /home/ton_user  ← où tu es actuellement

ls
# Documents  Downloads  devops-project

ls -la
# Montre TOUT, même les fichiers cachés (ceux qui commencent par .)
# Le "-l" = format détaillé, le "-a" = inclure les fichiers cachés

cd Documents
# Tu te déplaces dans Documents

pwd
# /home/ton_user/Documents  ← tu as changé de dossier

cd ..
# Tu remontes d'un niveau

pwd
# /home/ton_user  ← tu es revenu

cd ~
# Tu retournes dans ton dossier personnel (~ = raccourci pour /home/ton_user)
```

## Fichiers et dossiers

> **Ce sont des exemples à essayer.** Tu peux les taper dans ton terminal pour voir ce qu'ils font. Les fichiers créés ici sont juste pour s'entraîner — tu peux les supprimer après.

```bash
# Créer un fichier vide
touch mon_fichier.txt

ls
# mon_fichier.txt est apparu

# Créer un dossier
mkdir mon_dossier

# Créer un dossier + sous-dossiers d'un coup
mkdir -p projets/frontend/src
# -p = crée les dossiers parents s'ils n'existent pas

# Lire un fichier (affiche tout d'un coup)
cat mon_fichier.txt
# (rien — le fichier est vide, on vient de le créer avec touch)

# Lire un fichier long (page par page)
less mon_fichier.txt
# Flèches haut/bas pour naviguer, "q" pour quitter
# Utile pour les fichiers de logs qui font des milliers de lignes

# Copier
cp mon_fichier.txt copie.txt
cp -r mon_dossier/ copie_dossier/
# -r = récursif (copie le dossier ET tout ce qu'il contient)

# Renommer un fichier
mv copie.txt nouveau_nom.txt

# Déplacer un fichier dans un autre dossier
mv nouveau_nom.txt mon_dossier/
# Le fichier est maintenant dans mon_dossier/nouveau_nom.txt
# C'est la même commande "mv" pour renommer ET déplacer

# Supprimer
rm nouveau_nom.txt
rm -r mon_dossier/
# -r = récursif (supprime le dossier ET tout ce qu'il contient)
# ⚠️ Pas de corbeille sous Linux. rm = supprimé définitivement.

# Éditer un fichier dans le terminal
nano mon_fichier.txt
# Tape du texte, puis Ctrl+O → Entrée pour sauvegarder, Ctrl+X pour quitter
```

## Permissions

Chaque fichier a 3 types de permissions pour 3 catégories de personnes :

| Permission | Lettre | Chiffre | Ce que ça permet |
|-----------|--------|---------|-----------------|
| Read | r | 4 | Lire le fichier |
| Write | w | 2 | Modifier le fichier |
| Execute | x | 1 | Exécuter le fichier (lancer un script) |

Les 3 catégories : **propriétaire** (owner = toi), **groupe** (group = ton équipe), **autres** (others = tout le monde).

Le nombre `755` c'est un raccourci : `7` pour le propriétaire (4+2+1 = rwx), `5` pour le groupe (4+0+1 = r-x), `5` pour les autres (4+0+1 = r-x).

```bash
# Voir les permissions d'un fichier
ls -la mon_fichier.txt
# -rw-r--r-- 1 user user 0 jan 1 12:00 mon_fichier.txt
#  ^^^         → owner: rw- (lire + écrire)
#     ^^^      → group: r-- (lire seulement)
#        ^^^   → others: r-- (lire seulement)

# Changer les permissions (ces commandes sont des exemples, pas besoin de les taper)
chmod 755 mon_fichier.txt    # owner=rwx, group=rx, others=rx
chmod 644 mon_fichier.txt    # owner=rw, group=r, others=r
```

**En résumé :** Read = le droit de regarder. Write = le droit de modifier. Execute = le droit de lancer.

## Utilisateurs et sudo

```bash
whoami
# ton_user

# sudo = "fais ça en tant qu'administrateur"
sudo apt update
# Demande ton mot de passe, puis exécute la commande en mode admin
```

`sudo` c'est comme le mode administrateur sur Windows. Tu en as besoin pour installer des logiciels, modifier des fichiers système, etc. Sans `sudo`, tu ne peux faire que des choses dans ton propre dossier.

## Gestion des paquets (logiciels)

On a vu dans le Module 0 que chaque langage a son gestionnaire de paquets (uv pour Python, bun pour JS). **Linux aussi a le sien : `apt`.** Ici, un paquet = un logiciel prêt à être installé (curl, git, docker, etc.). `apt` va le télécharger et l'installer en une commande.

```bash
# Mettre à jour la liste des logiciels disponibles
sudo apt update

# Installer un logiciel
sudo apt install -y curl wget git

# Chercher un paquet
apt search nom_du_logiciel

# Supprimer un logiciel
sudo apt remove nom_du_logiciel
```

## Processus

Un processus = un programme en train de tourner.

```bash
# Voir tous les processus
ps aux
# USER       PID  %CPU %MEM  ...  COMMAND
# root         1   0.0  0.0  ...  init
# user      1234   0.1  0.5  ...  python3 main.py
# PID = l'identifiant unique du processus (un numéro)

# Voir les processus en temps réel (comme le Gestionnaire des tâches sur Windows)
top
# Appuie sur q pour quitter

# Tuer un processus (si un programme est bloqué par exemple)
kill 1234        # Demande poliment au processus de s'arrêter (remplace 1234 par le vrai PID)
kill -9 1234     # Force l'arrêt immédiat (dernier recours, si kill normal ne marche pas)
```

## Variables d'environnement

Une variable d'environnement = une valeur stockée dans le système, accessible par tous les programmes qui tournent. Imagine un post-it collé sur le frigo que tout le monde dans la maison peut lire. On s'en sert pour passer de la configuration aux applications (adresse de la base de données, mots de passe, modes de fonctionnement) sans la mettre directement dans le code.

```bash
# Voir toutes les variables d'environnement
printenv
# HOME=/home/user
# PATH=/usr/local/bin:/usr/bin:/bin
# ... (il y en a beaucoup, c'est normal)

# Voir une variable spécifique
echo $HOME
# /home/user

# Créer une variable (disponible dans le terminal courant uniquement)
MY_VAR="hello"
echo $MY_VAR
# hello

# Exporter une variable (disponible pour les programmes lancés depuis ce terminal)
export DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"

# Vérifier
echo $DATABASE_URL
# postgresql://user:pass@localhost:5432/mydb
```

### Le fichier `.env`

En pratique, on met les variables dans un fichier `.env` pour ne pas les taper à chaque fois :

```
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
API_KEY=abc123
DEBUG=true
```

> Ce fichier n'est pas à créer maintenant — c'est un exemple pour comprendre le concept. Tu le retrouveras dans Docker (Module 3).

⚠️ **Ne committe JAMAIS un fichier `.env` dans Git.** Il contient souvent des secrets. On le met dans `.gitignore`.

Tu retrouveras les variables d'environnement partout dans ce cursus : Docker (`-e`, `environment:`), CI/CD (`secrets`), Terraform (`TF_VAR_`), etc.

## Les environnements (dev / staging / prod)

Un concept transversal que tu retrouveras dans chaque module de ce cursus :

| Environnement | C'est quoi | Qui l'utilise |
|--------------|-----------|---------------|
| **dev** (local) | Ta machine. Tu développes, tu testes, tu casses — c'est fait pour ça. | Toi |
| **staging** | Une copie de la prod. On y teste avant de mettre en production. | L'équipe |
| **prod** (production) | Le vrai site, les vrais utilisateurs. Si ça casse ici, tout le monde le voit. | Les utilisateurs |

**La règle d'or :** Le même code tourne partout. Ce qui change entre les environnements, ce sont les **variables d'environnement** (vu juste au-dessus) : URL de la base de données, clés API, mode debug...

| Variable | Dev | Staging | Prod |
|----------|-----|---------|------|
| `DATABASE_URL` | (absente → in-memory) | `postgresql://staging-db:5432/tasks` | `postgresql://prod-db:5432/tasks` |
| `DEBUG` | `true` | `true` | `false` |

Tu retrouveras ce concept dans Docker (environment), CI/CD (secrets par environnement), Terraform (`.tfvars` par environnement), et Kubernetes (namespaces).

## Pipes et redirections

Le pipe `|` envoie la sortie d'une commande vers une autre. C'est comme une chaîne de montage.

```bash
# Chercher le mot "error" dans un fichier
cat mon_fichier.txt | grep "error"
# cat affiche le fichier → grep filtre les lignes contenant "error"

# Compter le nombre de fichiers dans un dossier
ls | wc -l
# ls liste les fichiers → wc -l compte le nombre de lignes

# Rediriger la sortie vers un fichier
echo "hello" > fichier.txt     # Écrase le fichier (ou le crée s'il n'existe pas)
echo "world" >> fichier.txt    # Ajoute à la fin du fichier

cat fichier.txt
# hello
# world
```

## Recherche

```bash
# Chercher du texte dans des fichiers
grep "error" mon_fichier.txt
grep -r "TODO" ~/devops-project/     # -r = récursif (cherche dans les sous-dossiers aussi)
grep -i "error" mon_fichier.txt      # -i = insensible à la casse (Error, ERROR, error → tous trouvés)

# Chercher des fichiers par nom
find ~/devops-project -name "*.py"
# /home/user/devops-project/backend/main.py
# /home/user/devops-project/backend/test_main.py
```

## Lire un message d'erreur

Savoir lire un message d'erreur, c'est 50% du métier DevOps. La plupart des débutants paniquent devant un mur de texte rouge. En réalité, l'erreur te dit exactement ce qui ne va pas — il faut juste savoir où regarder.

### La méthode : lis de bas en haut

Les erreurs Python (et la plupart des langages) affichent un **stacktrace** — la pile d'appels qui a mené à l'erreur. La ligne la plus importante est **la dernière** :

```bash
uv run uvicorn main:app
# Traceback (most recent call last):
#   File "main.py", line 3, in <module>
#     from fastapi import FastAPI
# ModuleNotFoundError: No module named 'fastapi'
#                      ^^^^^^^^^^^^^^^^^^^^^^^^
#                      ← C'EST ICI : fastapi n'est pas installé
```

**Traduction :** Python essaie d'importer `fastapi` mais ne le trouve pas. Fix : `uv sync` (pour installer les dépendances).

### Les erreurs les plus fréquentes

| Message | Ce que ça veut dire | Fix |
|---------|-------------------|-----|
| `ModuleNotFoundError: No module named 'X'` | La dépendance X n'est pas installée | `uv sync` ou `bun install` |
| `FileNotFoundError: No such file or directory` | Le fichier/dossier n'existe pas | Vérifie le chemin, `ls` pour voir ce qui existe |
| `PermissionError: Permission denied` | Tu n'as pas les droits | `sudo` ou `chmod` |
| `Connection refused` | Rien n'écoute sur ce port | Le serveur n'est pas lancé, ou mauvais port |
| `Address already in use` | Le port est déjà pris | Un autre processus utilise ce port (`ss -tlnp`) |
| `command not found` | La commande n'est pas installée | `sudo apt install ...` ou vérifier le PATH |
| `YAML syntax error` | Erreur d'indentation dans un fichier YAML | Vérifier espaces vs tabs, indentation cohérente |

### Le réflexe : copie-colle l'erreur dans Google

Quand tu ne comprends pas un message d'erreur :
1. Copie **la dernière ligne** du message (sans les chemins spécifiques à ta machine)
2. Colle-la dans Google
3. Le premier résultat Stack Overflow a la réponse dans 90% des cas

C'est ce que font tous les développeurs, même les seniors. Ce n'est pas de la triche.

## SSH

SSH (Secure Shell) te permet de te connecter à un serveur distant — tu l'utiliseras dans le Module 5 (AWS) pour te connecter à ton EC2.

```bash
ssh user@192.168.1.100
# Tu es maintenant "dans" le serveur distant. Toutes les commandes s'exécutent là-bas.
# Ctrl+D ou "exit" pour déconnecter.
```

> Tu n'as pas besoin d'utiliser SSH maintenant — c'est juste pour savoir que ça existe. Tu le feras pour de vrai dans le Module 5.

## Services (systemctl)

Un service = un programme qui tourne en arrière-plan (serveur web, base de données...).

> **Ces commandes sont des exemples.** Tu n'as pas besoin de les taper maintenant — nginx n'est probablement pas installé sur ta machine. Tu utiliseras `systemctl` dans les modules suivants.

```bash
sudo systemctl start nginx      # Démarrer
sudo systemctl stop nginx       # Arrêter
sudo systemctl restart nginx    # Redémarrer
sudo systemctl status nginx     # Voir l'état
sudo systemctl enable nginx     # Lancer au démarrage automatiquement
```

> **Note WSL :** `systemctl` ne fonctionne pas par défaut dans WSL (pas de systemd). Tu peux l'activer en ajoutant `[boot] systemd=true` dans `/etc/wsl.conf` puis en relançant WSL (`wsl --shutdown` depuis PowerShell). Sinon, lance les services manuellement (`sudo service nginx start`).

## YAML — Le format de config universel

Tu vas écrire du YAML dans presque tous les modules suivants : Docker Compose, GitHub Actions, Ansible, Kubernetes. C'est LE format de configuration en DevOps. Il faut comprendre ses règles avant de commencer.

**YAML c'est quoi ?** Un format texte pour écrire de la configuration. Plus lisible que JSON, mais strict sur l'indentation.

### Les 3 types de base

```yaml
# 1. Clé-valeur (comme une variable)
name: "devops-project"
port: 8000
debug: true

# 2. Liste (comme un tableau)
services:
  - backend
  - frontend
  - database

# 3. Objet imbriqué (comme un dossier avec des sous-dossiers)
backend:
  image: "python:3.12"
  port: 8000
  environment:
    - DATABASE_URL=postgresql://...
```

### Les règles d'or

| Règle | Bon | Mauvais |
|-------|-----|---------|
| Indentation = **espaces** (2 ou 4) | `  port: 8000` | `\tport: 8000` (tabulation) |
| Pas de tabulations | Espaces uniquement | Tab = erreur silencieuse |
| Indentation = hiérarchie | 2 espaces = un niveau | Indentation incohérente = crash |
| Les `:` sont suivis d'un espace | `port: 8000` | `port:8000` |

### L'erreur la plus fréquente

```yaml
# Correct (2 espaces d'indentation)
services:
  backend:
    port: 8000

# Incorrect (mélange 2 et 3 espaces)
services:
  backend:
     port: 8000    # ← 3 espaces au lieu de 4, YAML ne comprend pas
```

Si tu as une erreur mystérieuse dans un fichier YAML, c'est presque toujours un problème d'indentation. Vérifie que tu utilises des **espaces** (pas des tabs) et que chaque niveau a le **même nombre d'espaces**.

> **Astuce VS Code :** en bas à droite de l'éditeur, tu vois "Spaces: 2" ou "Tab Size: 4". Clique dessus pour t'assurer que tu utilises des espaces, pas des tabulations.

## Projet pratique : Script bash

> **Ce projet est optionnel.** C'est un bon exercice pour pratiquer les commandes vues dans ce module, mais tu peux passer au module suivant si tu es pressé.

On va créer un petit script qui automatise la mise en place d'un projet.

### 1. Crée le script

```bash
nano ~/setup-project.sh
```

`nano` ouvre un éditeur de texte dans le terminal. Tape le contenu suivant :

```bash
#!/bin/bash
# ↑ Cette ligne dit à Linux "exécute ce fichier avec bash"

# On récupère le nom du projet passé en argument
# Quand tu tapes : ./setup-project.sh mon-projet
# "mon-projet" est le 1er argument, accessible via $1
PROJECT_NAME=$1

# Vérifier qu'un nom a été donné
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup-project.sh nom_du_projet"
    exit 1
fi

echo "Création du projet $PROJECT_NAME..."

# Créer la structure de dossiers
mkdir -p "$PROJECT_NAME"/src
mkdir -p "$PROJECT_NAME"/tests
mkdir -p "$PROJECT_NAME"/docs

# Créer des fichiers de base
touch "$PROJECT_NAME"/src/main.py
touch "$PROJECT_NAME"/tests/test_main.py

# Écrire du contenu dans les fichiers
echo "# $PROJECT_NAME" > "$PROJECT_NAME"/README.md
echo "print('Hello from $PROJECT_NAME')" > "$PROJECT_NAME"/src/main.py

echo "Projet créé ! Structure :"
ls -la "$PROJECT_NAME"/
```

Sauvegarde avec `Ctrl+O` → `Entrée`, puis quitte avec `Ctrl+X`.

### 2. Rends-le exécutable et lance-le

```bash
chmod +x ~/setup-project.sh
# chmod +x = ajouter la permission "execute" au fichier
# Sans ça, Linux refuse de le lancer (permission denied)

~/setup-project.sh mon-super-projet
# Création du projet mon-super-projet...
# Projet créé ! Structure :
# (tu vois la liste des fichiers créés)

ls mon-super-projet/
# README.md  docs  src  tests

cat mon-super-projet/src/main.py
# print('Hello from mon-super-projet')
```

### 3. Nettoyer

```bash
# Supprime le projet de test (c'était juste un exercice)
rm -r mon-super-projet
rm ~/setup-project.sh
```

## Coin entretien

**Q : Expliquer les permissions Linux (rwx, 755, etc.)**
R : Chaque fichier a 3 blocs de permissions (owner, group, others). Chaque bloc = read (4) + write (2) + execute (1). Exemple : 755 = owner peut tout faire (7), group et others peuvent lire et exécuter (5).

**Q : C'est quoi un pipe (`|`) ?**
R : Il envoie la sortie d'une commande comme entrée de la suivante. Exemple : `ps aux | grep python` liste les processus puis filtre ceux contenant "python".

**Q : Différence entre `>` et `>>` ?**
R : `>` écrase le fichier. `>>` ajoute à la fin.

**Q : C'est quoi sudo ?**
R : Exécuter une commande en tant qu'administrateur (root). Nécessaire pour installer des logiciels, modifier la config système, etc.

**Q : Comment voir les logs d'un service ?**
R : `journalctl -u nom_du_service` ou regarder dans `/var/log/`.

## Erreurs courantes

- **"Permission denied"** → Il te manque les droits. Essaie avec `sudo` ou vérifie les permissions (`ls -la`).
- **`rm -rf /`** → Le problème ici c'est le `/` à la fin. `/` c'est la racine du système (tout le disque dur). Cette commande dit "supprime récursivement tout depuis la racine" — c'est comme formater ton disque. La commande `rm -rf` en elle-même n'est pas dangereuse (tu l'utilises souvent pour supprimer des dossiers), c'est le fait de cibler `/` qui est catastrophique. Les systèmes modernes ont une sécurité qui bloque `rm -rf /` sans le flag `--no-preserve-root`, mais fais toujours attention à CE QUE tu supprimes — vérifie le chemin avant d'appuyer sur Entrée.
- **Oublier `sudo apt update` avant `apt install`** → La liste des paquets n'est pas à jour, le paquet peut ne pas être trouvé.
- **Éditer un fichier sans les droits** → `nano /etc/config` ne marchera pas, il faut `sudo nano /etc/config`.

## Bonnes pratiques

- **Ne travaille jamais en root.** Utilise `sudo` uniquement quand c'est nécessaire. Si tout tourne en root, une erreur ou un hack = tout le système est compromis.
- **Lis avant de coller.** Ne copie-colle jamais une commande d'Internet sans comprendre ce qu'elle fait. Surtout avec `sudo`, `rm`, `curl | bash`.
- **Utilise `ls` et `pwd` souvent.** Toujours savoir où tu es et ce qu'il y a autour. Ça évite de supprimer le mauvais dossier.
- **Mets des commentaires dans tes scripts.** Toi dans 3 mois, tu ne te souviendras plus pourquoi tu as écrit `chmod 600`.

## Pour aller plus loin

- **journalctl** : lire les logs système en détail — essentiel pour debugger des services qui crashent
- **cron jobs** : planifier des tâches automatiques (`crontab -e`) — tu le verras en entreprise pour des scripts de nettoyage, backups, etc.
- **sed / awk** : outils de manipulation de texte — utile pour transformer des fichiers de config en masse

## Tu peux passer au module suivant si...

- [ ] Tu sais naviguer dans le filesystem (`cd`, `ls`, `pwd`, `mkdir`, `cp`, `mv`, `rm`)
- [ ] Tu comprends les permissions (`chmod 755` = owner rwx, group rx, others rx)
- [ ] Tu sais utiliser `sudo` et tu sais pourquoi on ne travaille pas en root
- [ ] Tu sais créer et exporter une variable d'environnement (`export MA_VAR="valeur"`)
- [ ] Tu sais utiliser un pipe (`|`) et une redirection (`>`, `>>`)
- [ ] Tu sais lire un message d'erreur (dernière ligne = l'important)
- [ ] Tu comprends la structure d'un fichier YAML (clé-valeur, listes, indentation = espaces)
