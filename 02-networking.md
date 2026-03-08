# Module 2 : Réseau

## C'est quoi le réseau et pourquoi c'est important ?

**Le problème :** Tout en DevOps passe par le réseau. Docker, AWS, Kubernetes — tout ça, c'est des machines qui communiquent entre elles. Si tu ne comprends pas comment deux machines se parlent, tu seras bloqué à chaque étape. C'est comme vouloir envoyer du courrier sans connaître le système postal.

**Les analogies :**
- **Adresse IP** = adresse de ta maison
- **Port** = numéro d'appartement dans l'immeuble
- **DNS** = annuaire téléphonique (traduit "google.com" en adresse IP)
- **HTTP** = la langue que tu parles quand tu frappes à la porte
- **Firewall** = le vigile à l'entrée de l'immeuble

## Installation

```bash
sudo apt install -y dnsutils net-tools curl wget
```

## Adresses IP

Une adresse IP identifie une machine sur le réseau. Il en existe deux types :

| Type | Exemple | C'est quoi |
|------|---------|-----------|
| **Publique** | `203.0.113.42` | Ton adresse sur Internet (visible par tous) |
| **Privée** | `192.168.1.15` | Ton adresse locale (visible uniquement sur ton réseau) |

```bash
# Voir ton IP privée
ip addr show
# ou
hostname -I
# 192.168.1.15

# Voir ton IP publique
curl ifconfig.me
# 203.0.113.42
```

**Analogie :** L'IP publique = l'adresse de ton immeuble. L'IP privée = ton numéro d'appartement à l'intérieur.

## Ports

Un port = un numéro entre 1 et 65535 qui identifie un service sur une machine. Une IP sans port, c'est comme une adresse sans numéro d'appartement.

| Port | Service |
|------|---------|
| 22 | SSH (connexion distante) |
| 80 | HTTP (web non sécurisé) |
| 443 | HTTPS (web sécurisé) |
| 8080 | HTTP alternatif (souvent pour le dev) |
| 3000 | Souvent React/Node en dev |
| 5432 | PostgreSQL |
| 8000 | Souvent FastAPI/Django en dev |

```bash
# Voir les ports ouverts sur ta machine
ss -tlnp
# State   Recv-Q  Send-Q   Local Address:Port   ...
# LISTEN  0       128      0.0.0.0:22            ...  sshd
# LISTEN  0       128      0.0.0.0:8000          ...  uvicorn
```

## DNS

Le DNS traduit un nom de domaine (`google.com`) en adresse IP (`142.250.74.206`). Sans DNS, il faudrait retenir les IP de tous les sites.

```bash
dig google.com
# ;; ANSWER SECTION:
# google.com.     300     IN      A       142.250.74.206

# Version simplifiée
dig +short google.com
# 142.250.74.206

# Voir quel serveur DNS tu utilises
cat /etc/resolv.conf
```

## HTTP / HTTPS et codes de statut

HTTP = le protocole que ton navigateur utilise pour parler aux serveurs web. HTTPS = pareil, mais chiffré (cadenas dans le navigateur).

Les codes de statut importants :

| Code | Signification | Analogie |
|------|--------------|----------|
| **200** | OK, tout va bien | "Voilà ta commande" |
| **301** | Redirection permanente | "On a déménagé, va là-bas" |
| **404** | Pas trouvé | "Ça n'existe pas ici" |
| **500** | Erreur serveur | "On a un problème en cuisine" |
| **502** | Bad Gateway | "Le serveur derrière est en panne" |

```bash
# Faire une requête HTTP
curl http://localhost:8000/api/tasks
# [{"id":1,"title":"Apprendre Docker","done":false}]

# Voir les headers (dont le code de statut)
curl -I https://google.com
# HTTP/2 301
# location: https://www.google.com/

# Télécharger un fichier
wget https://example.com/fichier.txt
```

## TCP vs UDP

- **TCP** : fiable, vérifie que tout arrive dans l'ordre (HTTP, SSH, email). Comme un recommandé avec accusé de réception.
- **UDP** : rapide, ne vérifie rien (streaming vidéo, DNS, jeux en ligne). Comme une carte postale — plus rapide mais pas de garantie.

## Subnets / CIDR

Un subnet (sous-réseau) découpe un réseau en morceaux plus petits.

La notation CIDR `/24` veut dire : les 24 premiers bits de l'adresse sont fixes, le reste varie.

| CIDR | Nombre d'adresses | Exemple |
|------|-------------------|---------|
| `/32` | 1 adresse | Une seule machine |
| `/24` | 256 adresses | Un petit réseau (le plus courant) |
| `/16` | 65 536 adresses | Un gros réseau |
| `/0` | Tout Internet | Tout le monde |

**Exemple :** `192.168.1.0/24` = toutes les adresses de `192.168.1.0` à `192.168.1.255`.

C'est tout ce que tu as besoin de savoir. En entretien, retiens `/24 = 256 adresses`.

## Reverse Proxy et Load Balancer

Ces deux termes reviennent tout le temps en DevOps. Ils sont liés mais différents.

### Reverse Proxy

Un reverse proxy se place **devant** ton application et reçoit toutes les requêtes à sa place.

```
Utilisateur → Reverse Proxy (nginx) → Ton app (port 8000)
```

**Pourquoi ?** Ton app n'est pas faite pour gérer le HTTPS, la compression, les fichiers statiques, ou 10 000 connexions en même temps. Le reverse proxy fait tout ça pour elle.

**Analogie :** Le réceptionniste d'un hôtel. Les clients ne vont pas directement dans les chambres — ils passent par le réceptionniste qui les dirige.

**L'outil le plus courant :** nginx. Tu le verras dans le Module 3 (Docker) devant notre frontend.

### Load Balancer

Un load balancer répartit le trafic entre **plusieurs serveurs** identiques.

```
                    ┌── Serveur 1 (ton app)
Utilisateur → LB ──┼── Serveur 2 (ton app)
                    └── Serveur 3 (ton app)
```

**Pourquoi ?** Un seul serveur ne peut pas gérer un trafic illimité. Avec un load balancer, tu ajoutes des serveurs pour absorber plus de trafic. Et si un serveur tombe, les autres prennent le relais.

**Analogie :** Le maître d'hôtel d'un restaurant qui répartit les clients entre les tables. Si un serveur est débordé, il envoie les clients aux autres.

**Sur AWS :** Application Load Balancer (ALB). Tu le verras dans les Modules 5 et 8.

> En pratique, un reverse proxy et un load balancer sont souvent le même outil (nginx, ALB). La différence c'est le rôle : proxy = 1 serveur derrière, load balancer = N serveurs derrière.

## Firewall (ufw)

Un firewall contrôle qui peut entrer et sortir de ta machine. `ufw` (Uncomplicated Firewall) est le firewall simple d'Ubuntu.

```bash
# Activer le firewall
sudo ufw enable

# Voir les règles
sudo ufw status

# Autoriser SSH (sinon tu te coupes l'accès !)
sudo ufw allow 22

# Autoriser le port 80 (HTTP)
sudo ufw allow 80

# Autoriser un port spécifique
sudo ufw allow 8000

# Bloquer un port
sudo ufw deny 3306

# Supprimer une règle
sudo ufw delete allow 8000
```

⚠️ **Toujours autoriser SSH (port 22) AVANT d'activer le firewall sur un serveur distant.** Sinon tu te coupes l'accès.

## Commandes réseau utiles

```bash
# Vérifier si une machine est joignable
ping google.com
# PING google.com (142.250.74.206): 56 data bytes
# 64 bytes from 142.250.74.206: icmp_seq=0 ttl=117 time=12.3 ms

# Voir le chemin réseau vers une machine
traceroute google.com

# Voir les connexions et ports ouverts
ss -tlnp

# Résoudre un nom DNS
dig +short example.com

# Faire une requête HTTP
curl http://localhost:8000/api/health
# {"status":"ok"}
```

## Projet pratique

### 1. Interroger une API publique

```bash
curl https://httpbin.org/ip
# {"origin": "ton.ip.publique"}

curl https://httpbin.org/status/404
# (retourne un 404)

curl -I https://httpbin.org/status/200
# HTTP/2 200
```

### 2. Résoudre des noms DNS

```bash
dig +short google.com
dig +short github.com
dig +short amazon.com
```

### 3. Vérifier les ports de ton projet

Lance le backend du projet fil rouge, puis :
```bash
cd ~/devops-project/backend
uv run uvicorn main:app --reload &

ss -tlnp | grep 8000
# LISTEN  0  128  0.0.0.0:8000  ...  uvicorn

curl http://localhost:8000/api/health
# {"status":"ok"}
```

### 4. Configurer ufw

```bash
sudo ufw allow 22
sudo ufw allow 8000
sudo ufw allow 3000
sudo ufw enable
sudo ufw status
# Status: active
# To                         Action      From
# --                         ------      ----
# 22                         ALLOW       Anywhere
# 8000                       ALLOW       Anywhere
# 3000                       ALLOW       Anywhere
```

## Coin entretien

**Q : C'est quoi une adresse IP ?**
R : Un identifiant unique pour une machine sur un réseau. Deux types : publique (visible sur Internet) et privée (visible uniquement en local).

**Q : C'est quoi un port ?**
R : Un numéro (1-65535) qui identifie un service sur une machine. Exemple : 80 = HTTP, 443 = HTTPS, 22 = SSH.

**Q : C'est quoi le DNS ?**
R : Le système qui traduit les noms de domaine (google.com) en adresses IP (142.250.74.206). Sans DNS, il faudrait retenir les IP.

**Q : Différence entre TCP et UDP ?**
R : TCP est fiable (vérifie que tout arrive), UDP est rapide (ne vérifie pas). HTTP utilise TCP, le streaming utilise souvent UDP.

**Q : C'est quoi un CIDR /24 ?**
R : Un sous-réseau de 256 adresses IP. Exemple : 10.0.1.0/24 = 10.0.1.0 à 10.0.1.255.

**Q : C'est quoi un firewall ?**
R : Un filtre qui contrôle le trafic réseau entrant et sortant. Il autorise ou bloque le trafic en fonction de règles (port, IP source, etc.).

**Q : Que signifie un code 502 ?**
R : Bad Gateway — le serveur proxy/load balancer n'arrive pas à joindre le serveur derrière lui. Souvent le serveur d'application a crashé.

## Erreurs courantes

- **Oublier d'autoriser SSH avant d'activer ufw** → Tu te coupes l'accès au serveur distant.
- **Confondre IP publique et privée** → Une IP privée (192.168.x.x) n'est pas joignable depuis Internet.
- **"Connection refused"** → Le service n'écoute pas sur ce port, ou le firewall le bloque.
- **"Could not resolve host"** → Problème DNS. Vérifie `/etc/resolv.conf` ou essaie avec l'IP directement.

## Bonnes pratiques

- **Ne jamais exposer une base de données sur Internet.** La DB doit être accessible uniquement depuis le réseau interne (subnet privé, Security Group restreint).
- **HTTPS partout.** Même en dev. Let's Encrypt fournit des certificats gratuits. En prod, pas d'excuse pour du HTTP.
- **N'ouvre que les ports nécessaires.** Chaque port ouvert est une surface d'attaque. SSH (22) + HTTP(S) (80/443) suffisent pour la plupart des cas.
- **Change le port SSH par défaut** sur les serveurs exposés à Internet (de 22 à un port custom). Ça réduit les attaques automatisées.

## Pour aller plus loin

- **TCP/IP en profondeur** : le modèle OSI (7 couches), le three-way handshake
- **Wireshark** : outil pour inspecter le trafic réseau en temps réel
- **VPN / Tunneling** : comment créer des connexions sécurisées entre réseaux
- **IPv6** : le successeur d'IPv4 (adresses plus longues, plus d'adresses disponibles)
- **Certification CompTIA Network+** : la certification réseau d'entrée de gamme
