# Module 1 : Les Bases de Linux

> **Prérequis :** Module 0 (Git, WSL installé)

> **En résumé :** Tu apprends à naviguer dans un terminal Linux — fichiers, permissions, processus, variables d'environnement. C'est la base de tout ce qui suit : Docker, AWS, Ansible, Kubernetes tournent tous sur Linux.

## C'est quoi Linux et pourquoi ça existe ?

**Le problème :** 90%+ des serveurs dans le monde tournent sous Linux. Pas Windows, pas macOS — Linux. Si tu veux faire du DevOps, tu DOIS savoir naviguer dans un terminal Linux. C'est comme vouloir être cuisinier sans savoir utiliser un couteau.

**L'analogie :** Le système de fichiers Linux, c'est un **immeuble**.
- `/` = le rez-de-chaussée (la racine, tout part de là)
- `/home` = les appartements (chaque utilisateur a le sien)
- `/etc` = le bureau du syndic (fichiers de configuration)
- `/var` = le local poubelle/stockage (logs, données variables)
- `/tmp` = le hall d'entrée (fichiers temporaires, vidé au reboot)

## Les 5 dossiers à connaître

| Dossier | Contenu | Analogie |
|---------|---------|----------|
| `/` | La racine, tout part d'ici | Rez-de-chaussée |
| `/home/ton_user` | Tes fichiers perso | Ton appartement |
| `/etc` | Configuration système | Bureau du syndic |
| `/var` | Logs, données variables | Local de stockage |
| `/tmp` | Fichiers temporaires | Hall d'entrée |

## Navigation

```bash
pwd
# /home/ton_user  ← où tu es actuellement

ls
# Documents  Downloads  devops-project

ls -la
# total 12
# drwxr-xr-x  4 user user 4096 jan  1 12:00 .
# drwxr-xr-x  3 root root 4096 jan  1 12:00 ..
# drwxr-xr-x  2 user user 4096 jan  1 12:00 Documents
# Le -la montre TOUT, même les fichiers cachés (ceux qui commencent par .)

cd Documents
# Tu te déplaces dans Documents

cd ..
# Tu remontes d'un niveau

cd ~
# Tu retournes dans ton dossier personnel (/home/ton_user)

cd /etc
# Tu vas directement dans /etc (chemin absolu)
```

## Fichiers et dossiers

```bash
# Créer un fichier vide
touch mon_fichier.txt

# Créer un dossier
mkdir mon_dossier

# Créer un dossier + sous-dossiers d'un coup
mkdir -p projets/frontend/src

# Lire un fichier
cat mon_fichier.txt

# Copier
cp fichier.txt copie.txt
cp -r dossier/ copie_dossier/    # -r = récursif (pour les dossiers)

# Déplacer / renommer
mv ancien.txt nouveau.txt
mv fichier.txt /home/user/Documents/

# Supprimer
rm fichier.txt
rm -r dossier/    # -r = récursif (pour les dossiers)
# ⚠️ Pas de corbeille sous Linux. rm = supprimé définitivement.

# Éditer un fichier dans le terminal
nano fichier.txt
# Ctrl+O pour sauvegarder, Ctrl+X pour quitter
```

## Permissions

Chaque fichier a 3 types de permissions pour 3 catégories de personnes :

| Permission | Lettre | Chiffre | Ce que ça permet |
|-----------|--------|---------|-----------------|
| Read | r | 4 | Lire le fichier |
| Write | w | 2 | Modifier le fichier |
| Execute | x | 1 | Exécuter le fichier (scripts) |

Les 3 catégories : **propriétaire** (owner), **groupe** (group), **autres** (others).

```bash
ls -la script.sh
# -rwxr-xr-- 1 user group 100 jan 1 12:00 script.sh
#  ^^^         → owner: rwx (7 = 4+2+1)
#     ^^^      → group: r-x (5 = 4+0+1)
#        ^^^   → others: r-- (4 = 4+0+0)

# Changer les permissions
chmod 755 script.sh    # owner=rwx, group=rx, others=rx
chmod 644 config.txt   # owner=rw, group=r, others=r

# Changer le propriétaire
sudo chown user:group fichier.txt
```

**Analogie des clés :** Read = le droit de regarder. Write = le droit de modifier. Execute = le droit d'appuyer sur "lancer".

## Utilisateurs et sudo

```bash
whoami
# ton_user

# sudo = "fais ça en tant qu'administrateur"
sudo apt update
# Demande ton mot de passe, puis exécute la commande en mode admin
```

`sudo` c'est comme demander les clés du syndic pour faire une opération spéciale. Tu en as besoin pour installer des logiciels, modifier des fichiers système, etc.

## Gestion des paquets (logiciels)

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
# USER       PID  %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root         1   0.0  0.0  ...  init
# user      1234   0.1  0.5  ...  python3 main.py

# Voir les processus en temps réel
top
# (Appuie sur q pour quitter)

# Tuer un processus
kill 1234        # Demande poliment au processus de s'arrêter
kill -9 1234     # Force l'arrêt (dernier recours)
```

## Variables d'environnement

Une variable d'environnement = une valeur stockée dans le système, accessible par tous les programmes. C'est comme ça qu'on passe de la configuration aux applications (mots de passe, URLs, modes de fonctionnement).

```bash
# Voir toutes les variables d'environnement
printenv
# HOME=/home/user
# PATH=/usr/local/bin:/usr/bin:/bin
# ...

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

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
API_KEY=abc123
DEBUG=true
```

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
# Chercher "error" dans les logs
cat /var/log/syslog | grep "error"

# Compter le nombre de fichiers
ls | wc -l

# Rediriger la sortie vers un fichier
echo "hello" > fichier.txt     # Écrase le fichier
echo "world" >> fichier.txt    # Ajoute à la fin

cat fichier.txt
# hello
# world
```

## Recherche

```bash
# Chercher du texte dans des fichiers
grep "error" /var/log/syslog
grep -r "TODO" ~/devops-project/     # -r = récursif dans les sous-dossiers
grep -i "error" log.txt              # -i = insensible à la casse

# Chercher des fichiers
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

SSH (Secure Shell) te permet de te connecter à un serveur distant.

```bash
ssh user@192.168.1.100
# Tu es maintenant "dans" le serveur distant. Toutes les commandes s'exécutent là-bas.
# Ctrl+D ou "exit" pour déconnecter.
```

## Services (systemctl)

Un service = un programme qui tourne en arrière-plan (serveur web, base de données...).

```bash
sudo systemctl start nginx      # Démarrer
sudo systemctl stop nginx       # Arrêter
sudo systemctl restart nginx    # Redémarrer
sudo systemctl status nginx     # Voir l'état
sudo systemctl enable nginx     # Lancer au démarrage automatiquement
```

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
# ✅ Correct (2 espaces d'indentation)
services:
  backend:
    port: 8000

# ❌ Incorrect (mélange 2 et 3 espaces)
services:
  backend:
     port: 8000    # ← 3 espaces au lieu de 4, YAML ne comprend pas
```

Si tu as une erreur mystérieuse dans un fichier YAML, c'est presque toujours un problème d'indentation. Vérifie que tu utilises des **espaces** (pas des tabs) et que chaque niveau a le **même nombre d'espaces**.

> **Astuce VS Code :** en bas à droite de l'éditeur, tu vois "Spaces: 2" ou "Tab Size: 4". Clique dessus pour t'assurer que tu utilises des espaces, pas des tabulations. Tu peux aussi activer "Render Whitespace" pour voir les espaces.

## Les commentaires dans le code

Un **commentaire** est une ligne que l'ordinateur **ignore complètement**. C'est du texte écrit pour les humains — pour expliquer ce que fait le code, pourquoi on l'a écrit comme ça, ou prévenir d'un piège.

| Langage | Syntaxe | Exemple |
|---------|---------|---------|
| **Bash / Python / YAML** | `#` | `# Installer les dépendances` |
| **JavaScript / JSX** | `//` | `// Appel HTTP vers le backend` |
| **JavaScript (bloc)** | `/* ... */` | `/* Ceci est un long commentaire */` |
| **Dockerfile** | `#` | `# Image de base` |
| **HTML** | `<!-- ... -->` | `<!-- Menu principal -->` |
| **nginx config** | `#` | `# Rediriger vers le backend` |

**Quand commenter :**
- Expliquer **pourquoi** on fait quelque chose (le *quoi* se voit dans le code)
- Prévenir d'un piège ou d'un comportement non évident
- Documenter les variables d'environnement et les configurations

**Quand NE PAS commenter :**
- Le code est déjà évident : `x = x + 1  # Ajouter 1 à x` → inutile
- Pour commenter du code mort — supprime-le, Git garde l'historique

Dans le projet fil rouge, tous les fichiers sont commentés pour t'aider à comprendre ce que fait chaque ligne. En pratique, on commente moins, car les développeurs expérimentés lisent le code directement.

## Projet pratique : Script bash

Crée un script qui automatise la mise en place d'un projet.

### 1. Crée le script

```bash
nano ~/setup-project.sh
```

Contenu du script :
```bash
#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup-project.sh nom_du_projet"
    exit 1
fi

echo "Création du projet $PROJECT_NAME..."

# Créer la structure
mkdir -p "$PROJECT_NAME"/{src,tests,docs}
touch "$PROJECT_NAME"/src/main.py
touch "$PROJECT_NAME"/tests/test_main.py
touch "$PROJECT_NAME"/README.md

# Mettre les bonnes permissions
chmod 755 "$PROJECT_NAME"/src/main.py

# Écrire un contenu de base
echo "# $PROJECT_NAME" > "$PROJECT_NAME"/README.md
echo 'print("Hello from '$PROJECT_NAME'")' > "$PROJECT_NAME"/src/main.py

echo "Projet créé ! Structure :"
find "$PROJECT_NAME" -type f
```

### 2. Rends-le exécutable et lance-le

```bash
chmod +x ~/setup-project.sh
~/setup-project.sh mon-super-projet
# Création du projet mon-super-projet...
# Projet créé ! Structure :
# mon-super-projet/README.md
# mon-super-projet/src/main.py
# mon-super-projet/tests/test_main.py
```

### 3. Vérifie avec grep

```bash
grep -r "Hello" mon-super-projet/
# mon-super-projet/src/main.py:print("Hello from mon-super-projet")
```

## Coin entretien

**Q : C'est quoi le filesystem Linux ?**
R : Une arborescence qui part de `/` (la racine). Tout est un fichier sous Linux — même les périphériques. Les dossiers importants : `/home` (utilisateurs), `/etc` (config), `/var` (logs/données).

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
- **`rm -rf /`** → NE FAIS JAMAIS ÇA. Ça supprime tout le système. Vérifie toujours ta commande `rm` avant de la lancer.
- **Oublier `sudo apt update` avant `apt install`** → La liste des paquets n'est pas à jour, le paquet peut ne pas être trouvé.
- **Éditer un fichier sans les droits** → `nano /etc/config` ne marchera pas, il faut `sudo nano /etc/config`.

## Bonnes pratiques

- **Ne travaille jamais en root.** Utilise `sudo` uniquement quand c'est nécessaire. Si tout tourne en root, une erreur ou un hack = tout le système est compromis.
- **Lis avant de coller.** Ne copie-colle jamais une commande d'Internet sans comprendre ce qu'elle fait. Surtout avec `sudo`, `rm`, `curl | bash`.
- **Utilise `ls -la` et `pwd` souvent.** Toujours savoir où tu es et ce qu'il y a autour. Ça évite de supprimer le mauvais dossier.
- **Mets des commentaires dans tes scripts.** Toi dans 3 mois, tu ne te souviendras plus pourquoi tu as écrit `chmod 600`.
- **Un fichier de config modifié = une copie de backup avant.** `cp nginx.conf nginx.conf.bak` avant de toucher quoi que ce soit.

## Pour aller plus loin

- **Bash scripting avancé** : boucles, fonctions, variables, conditions
- **sed / awk** : outils de manipulation de texte puissants (pour transformer des fichiers)
- **cron jobs** : planifier des tâches automatiques (`crontab -e`)
- **Linux From Scratch** : un livre pour construire Linux à la main (pour les passionnés)
- **Certification LPIC-1** : la certification Linux d'entrée de gamme, reconnue dans l'industrie

## Tu peux passer au module suivant si...

- [ ] Tu sais naviguer dans le filesystem (`cd`, `ls`, `pwd`, `mkdir`, `cp`, `mv`, `rm`)
- [ ] Tu comprends les permissions (`chmod 755` = owner rwx, group rx, others rx)
- [ ] Tu sais utiliser `sudo` et tu sais pourquoi on ne travaille pas en root
- [ ] Tu sais créer et exporter une variable d'environnement (`export MA_VAR="valeur"`)
- [ ] Tu sais utiliser un pipe (`|`) et une redirection (`>`, `>>`)
- [ ] Tu sais lire un message d'erreur (dernière ligne = l'important)
- [ ] Tu comprends la structure d'un fichier YAML (clé-valeur, listes, indentation = espaces)
