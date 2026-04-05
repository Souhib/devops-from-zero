# Module 8 : Monitoring (Sensibilisation)

> **Prérequis :** Module 3 (Docker — docker-compose pour lancer Prometheus/Grafana)

> **En résumé :** Tu apprends à surveiller ton application en production avec Prometheus (collecte de métriques) et Grafana (tableaux de bord). Sans monitoring, tu ne sais pas si ton app marche — tu l'apprends quand un utilisateur se plaint.

## C'est quoi le monitoring et pourquoi ça existe ?

**Le problème :** Ton app tourne en prod. Comment tu sais si elle marche bien ? Si elle est lente ? Si elle va crasher dans 10 minutes parce que le disque est plein ? Sans monitoring, tu ne le sais que quand un utilisateur se plaint. Ou pire, quand ton chef t'appelle un dimanche matin.

C'est comme **conduire une voiture sans tableau de bord** — pas de compteur de vitesse, pas de jauge d'essence, pas de voyants. Tu roules à l'aveugle.

**Les analogies :**
- **Prometheus** = les capteurs de la voiture (collecte les données)
- **Grafana** = le tableau de bord (affiche les jauges et les graphiques)
- **Alertes** = les voyants lumineux (te préviennent quand ça va mal)

## Les 3 piliers de l'observabilité

| Pilier | C'est quoi | Exemple | Outil |
|--------|-----------|---------|-------|
| **Metrics** | Des chiffres sur ton app (combien de requests, response time, CPU) | "95% des requests en <200ms" | Prometheus |
| **Logs** | Les messages texte de ton app ("user X a fait Y", "erreur Z") | "ERROR: connection refused to DB" | ELK/EFK stack |
| **Traces** | Le parcours d'une requête à travers tes services | "Requête → API → DB → Cache → Réponse (350ms)" | Jaeger, Zipkin |

Pour ce module, on se concentre sur les **metrics** avec Prometheus + Grafana.

### Les 4 Golden Signals (signaux d'or)

Avant de se lancer dans les outils, il faut savoir **quoi** mesurer. Google a défini 4 métriques essentielles (les "Golden Signals") qui suffisent pour surveiller n'importe quelle application :

| Signal | Question | Exemple |
|--------|----------|---------|
| **Latency** | C'est rapide ? | "95% des requêtes en <200ms" |
| **Traffic** | Combien de monde ? | "150 requêtes par seconde" |
| **Errors** | Ça marche ? | "0.5% de réponses en erreur (5xx)" |
| **Saturation** | C'est plein ? | "CPU à 70%, disque à 45%" |

Ces 4 chiffres valent mieux que 200 métriques que personne ne regarde. Commence par ceux-là.

## Prometheus — Le collecteur

Une **métrique**, c'est un chiffre qui mesure quelque chose : nombre de requêtes, temps de réponse, pourcentage de CPU utilisé. Prometheus collecte ces métriques en allant **chercher** les données sur tes applications (c'est le **pull model** — Prometheus va chercher, au lieu que l'app envoie). Concrètement, ton app expose une page spéciale à l'adresse `/metrics` avec tous ses chiffres, et Prometheus la consulte (**scrape** = aller chercher les données) toutes les 15 secondes. Il stocke tout dans une **base de données time series** — une base optimisée pour stocker des chiffres qui changent dans le temps (comme un historique de température).

Comment ça marche :
1. Ton app expose `http://localhost:8000/metrics`
2. Prometheus scrape cet endpoint toutes les 15 secondes
3. Prometheus stocke les données dans sa base de données interne
4. Tu interroges Prometheus pour voir les données

## Grafana — L'afficheur

Grafana se connecte à Prometheus (et d'autres sources) et affiche les données sous forme de graphiques, jauges et tableaux de bord.

## ELK / EFK Stack (juste les noms)

Pour les logs, l'industrie utilise souvent :
- **E**lasticsearch : stocke et indexe les logs
- **L**ogstash / **F**luentd : collecte et transforme les logs
- **K**ibana : interface pour chercher dans les logs

On ne le met pas en place dans ce cours, mais retiens les noms pour les entretiens.

## Structured Logs vs Plain Text Logs

En production, le format de tes logs fait une énorme différence. Comparer :

**Plain text (ce qu'on fait souvent en dev) :**
```
2024-01-15 14:32:01 ERROR Failed to create task: database connection refused
```

**Structured log / JSON (ce qu'on fait en prod) :**
```json
{
  "timestamp": "2024-01-15T14:32:01Z",
  "level": "error",
  "message": "Failed to create task",
  "error": "database connection refused",
  "service": "backend",
  "endpoint": "/api/tasks",
  "method": "POST",
  "request_id": "abc-123",
  "duration_ms": 1502
}
```

**Pourquoi c'est important :**
- Un log en plain text, tu peux le lire à l'oeil. Mais quand tu as **10 000 logs par minute** sur 5 services, tu ne peux pas faire `grep`. Tu as besoin de filtrer par `service`, `level`, `endpoint`, etc.
- Les structured logs (JSON) sont **parsables par les machines** : Elasticsearch, Loki, Datadog peuvent les indexer, les filtrer et les agréger automatiquement.
- Le `request_id` permet de **suivre une request** à travers plusieurs services (c'est le début du tracing).

**En pratique :** La plupart des frameworks ont un mode JSON pour les logs. Pour FastAPI/Python : la librairie `structlog` ou `python-json-logger`. Pour Node.js : `pino` ou `winston` en mode JSON.

**La règle :** En local, les logs lisibles (plain text) c'est OK. En production, toujours du JSON structuré.

## Alerting

Le monitoring sans alertes, c'est inutile. Personne ne regarde les dashboards 24/7.

**Bonnes pratiques :**
- Alerte sur les symptômes, pas les causes (alerte "le site est lent", pas "CPU à 80%")
- Chaque alerte doit être actionnable (si tu ne peux rien faire → ce n'est pas une alerte)
- Pas trop d'alertes (alert fatigue = on ignore tout)

**Outils d'alerting :** Prometheus Alertmanager, PagerDuty, OpsGenie.

## Outils SaaS (juste les noms)

| Outil | Ce que c'est |
|-------|-------------|
| **Datadog** | Monitoring SaaS tout-en-un (metrics, logs, traces) |
| **CloudWatch** | Le monitoring natif d'AWS |
| **New Relic** | Monitoring SaaS, populaire pour l'APM (Application Performance Monitoring) |

Ces outils font la même chose que Prometheus + Grafana, mais en version hébergée (pas besoin de gérer l'infra de monitoring).

## Projet pratique : Monitorer le projet fil rouge

### 1. Ajouter l'instrumentation au backend

**Instrumenter** une application = ajouter du code qui mesure automatiquement ce qui se passe (nombre de requêtes, temps de réponse, etc.) et expose ces chiffres pour Prometheus. La librairie `prometheus-fastapi-instrumentator` fait ça automatiquement pour FastAPI — elle est déjà dans les dépendances du projet (`pyproject.toml`, ajoutée lors du setup initial). Si ce n'est pas le cas, ajoute-la : `uv add prometheus-fastapi-instrumentator`. Il suffit ensuite de l'activer dans le code.

Ajoute ces deux lignes dans `backend/main.py` :

1. L'import en haut du fichier (avec les autres imports) :
```python
from prometheus_fastapi_instrumentator import Instrumentator
# Importe la librairie qui mesure automatiquement les requêtes HTTP
```

2. Juste après le bloc `app.add_middleware(...)`, ajoute :
```python
Instrumentator().instrument(app).expose(app)
# Instrumentator() = créer l'outil de mesure
# .instrument(app) = lui dire de surveiller notre app FastAPI
# .expose(app)     = ajouter l'endpoint /metrics à notre app (c'est la page que Prometheus viendra lire)
```

Le fichier `main.py` complet avec l'instrumentation :
```python
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator  # ← ajouté

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose /metrics pour Prometheus
Instrumentator().instrument(app).expose(app)  # ← ajouté

# ... le reste du code (storage, routes) ne change pas
```

Vérifie :
```bash
cd ~/devops-project/backend
uv run uvicorn main:app --reload &
curl http://localhost:8000/metrics
# # HELP http_requests_total Total number of HTTP requests
# # TYPE http_requests_total counter
# http_requests_total{method="GET",path="/api/tasks",status="2xx"} 5.0
# ...
```

### 2. Docker Compose avec Prometheus + Grafana

Crée le fichier avec `nano ~/devops-project/prometheus.yml` :
```yaml
global:
  scrape_interval: 15s          # Vérifier les métriques toutes les 15 secondes

scrape_configs:                  # Liste des applications à surveiller
  - job_name: "backend"          # Nom de cette cible (tu choisis le nom)
    static_configs:              # Adresses fixes (pas de découverte automatique)
      - targets: ["backend:8000"]
        # "backend" = nom du service dans docker-compose.yml
        # 8000 = le port du backend
        # Prometheus va aller lire http://backend:8000/metrics toutes les 15s
```

Ajoute les services Prometheus et Grafana à ton `docker-compose.yml` (en plus des services existants backend, frontend, db) :
```yaml
  # ... (garde les services backend, frontend, db existants)

  prometheus:
    image: prom/prometheus:latest          # Image officielle de Prometheus
    ports:
      - "9090:9090"                        # Port 9090 = convention Prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      # Copier notre fichier de config dans le container
      # ./prometheus.yml = le fichier qu'on vient de créer
      # /etc/prometheus/prometheus.yml = où Prometheus s'attend à trouver sa config
    depends_on:
      - backend                            # Attendre que le backend démarre

  grafana:
    image: grafana/grafana:latest          # Image officielle de Grafana
    ports:
      - "3001:3000"                        # 3001 sur ta machine → 3000 dans le container
      # On utilise 3001 car le port 3000 est peut-être déjà pris par le frontend en dev
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin   # Mot de passe admin (login: admin / admin)
    depends_on:
      - prometheus
```

### 3. Lancer

```bash
cd ~/devops-project
docker compose up -d --build

# Vérifier
docker compose ps
# 5 services running (backend, frontend, db, prometheus, grafana)
```

### 4. Vérifier Prometheus

Ouvre `http://localhost:9090` dans ton navigateur.
- Va dans **Status** → **Targets** : tu dois voir `backend:8000` avec l'état `UP`
- Dans la barre de recherche, tape `http_requests_total` et clique **Execute**

### 5. Créer un dashboard Grafana

1. Ouvre `http://localhost:3001` (login: admin / admin)
2. **Connections** → **Data sources** → **Add data source** → **Prometheus**
3. URL: `http://prometheus:9090` → **Save & Test**
4. **Dashboards** → **New** → **New Dashboard** → **Add visualization**
5. Choisis la source Prometheus, et entre une requête PromQL :

**PromQL — le langage de requête de Prometheus.** C'est comme SQL mais pour les métriques. Voici les bases :
- `http_requests_total` = le nom d'une métrique (le nombre total de requêtes reçues)
- `[1m]` = "sur les dernières 1 minute"
- `rate()` = calculer le taux par seconde (combien de requêtes par seconde)
- `histogram_quantile(0.95, ...)` = le 95e percentile (95% des requêtes sont plus rapides que cette valeur)

   Essaie ces requêtes :
   - `rate(http_requests_total[1m])` → nombre de requêtes par seconde
   - Clique **Run queries** → tu vois un graphique
6. Ajoute un autre panel :
   - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` → temps de réponse au 95e percentile
7. **Save dashboard** → Nomme-le "DevOps Project"

### 6. Générer du traffic et observer

> **Tape ces commandes dans ton terminal :**

```bash
# Générer du traffic pour voir des métriques dans Grafana
# Cette boucle envoie 100 requêtes au backend
for i in $(seq 1 100); do
  curl -s http://localhost:8000/api/tasks > /dev/null
done
# $(seq 1 100) = créer les nombres de 1 à 100
# curl -s = envoyer une requête silencieusement (pas de barre de progression)
# > /dev/null = jeter la réponse (on veut juste envoyer la requête, pas voir le résultat)
```

Retourne sur Grafana — tu verras les graphiques bouger.

💡 **Si Prometheus ne scrape pas :** vérifie que le target est `backend:8000` (le nom du service Docker, pas localhost).

## Coin entretien

**Q : Pourquoi le monitoring est important ?**
R : Sans monitoring, tu ne sais pas si ton app marche correctement. Tu détectes les problèmes avant les utilisateurs, tu identifies les goulots d'étranglement, et tu as des données pour prendre des décisions.

**Q : C'est quoi les 3 piliers de l'observabilité ?**
R : Metrics (chiffres — CPU, response time), Logs (messages texte des apps), Traces (parcours d'une request à travers les services).

**Q : C'est quoi Prometheus ?**
R : Un système de collecte de métriques en pull model. Il scrape les endpoints `/metrics` des applications à intervalles réguliers et stocke les données en time series.

**Q : C'est quoi Grafana ?**
R : Un outil de visualisation. Il se connecte à des sources de données (Prometheus, etc.) et crée des dashboards avec des graphiques et des alertes.

**Q : Différence entre pull et push model ?**
R : Pull = Prometheus va chercher les données (scrape). Push = les applications envoient les données. Le pull est plus simple à gérer et à débugger.

**Q : C'est quoi une bonne alerte ?**
R : Actionnable (on peut faire quelque chose), basée sur les symptômes (pas les causes), et pas trop fréquente (sinon on l'ignore).

## Bonnes pratiques

- **Commence petit.** 4 métriques suffisent — ce sont les **Golden Signals** (les 4 signaux d'or de Google) : **latency** (temps de réponse), **traffic** (nombre de requêtes), **errors** (taux d'erreurs), **saturation** (est-ce que les ressources sont pleines — CPU, mémoire, disque). Ces 4 chiffres valent mieux que 200 métriques que personne ne regarde.
- **Alerte sur les symptômes, pas les causes.** "Le site est lent pour les utilisateurs" (symptôme) est plus utile que "CPU à 80%" (cause possible). Le CPU à 80% est peut-être normal.
- **Chaque alerte doit avoir une action.** Si tu reçois une alerte et que ta réaction c'est "bof, c'est normal", supprime l'alerte. L'alert fatigue est le plus gros risque : tu finis par ignorer toutes les alertes, y compris les vraies.
- **Dashboard pour chaque audience.** Les devs veulent voir la latency par endpoint. Le CTO veut voir le nombre d'utilisateurs actifs. Pas le même dashboard.
- **Rétention des données.** Ne garde pas les métriques à la seconde indéfiniment — ça coûte du disque. 15 jours en haute résolution, 1 an en résolution réduite, c'est un bon défaut.

## Erreurs courantes

- **Prometheus ne scrape pas** → Vérifie que le target est correct et que le port est accessible.
- **Grafana "No data"** → Vérifie la data source (URL de Prometheus correcte ?).
- **Trop d'alertes** → Alert fatigue. Commence avec peu d'alertes critiques.
- **Monitorer les mauvaises choses** → Monitore ce qui impacte l'utilisateur (latency, errors), pas le CPU.

## Pour aller plus loin

- **PromQL** : le langage de requête de Prometheus — approfondir `rate()`, `histogram_quantile()`, les agrégations
- **Loki** : système de logs par Grafana Labs — centraliser les logs de tous tes services au même endroit
- **PagerDuty / OpsGenie** : plateformes d'alerting et d'astreinte — qui est de garde cette nuit, comment escalader
- **SRE practices** : SLI (indicateurs), SLO (objectifs), SLA (engagements) — le vocabulaire des équipes SRE en entreprise

## Tu peux passer au module suivant si...

- [ ] Tu connais les 3 piliers de l'observabilité (metrics, logs, traces)
- [ ] Tu sais ce que font Prometheus (collecte) et Grafana (affichage)
- [ ] Tu comprends la différence entre pull et push model
- [ ] Tu as vu le endpoint `/metrics` de ton backend retourner des données
- [ ] Tu as créé un dashboard Grafana basique
- [ ] Tu sais ce qu'est une bonne alerte (actionnable, symptôme, pas trop fréquente)
