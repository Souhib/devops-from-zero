# Module 9 : Monitoring (Sensibilisation)

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

## Prometheus — Le collecteur

Prometheus collecte des métriques en allant **chercher** les données sur tes applications (pull model). Ton app expose un endpoint `/metrics`, Prometheus le scrape régulièrement.

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

Installe la librairie Prometheus pour FastAPI :

```bash
cd ~/devops-project/backend
uv add prometheus-fastapi-instrumentator
```

Modifie `backend/main.py` pour ajouter l'instrumentation :
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose /metrics pour Prometheus
Instrumentator().instrument(app).expose(app)

# ... le reste du code ne change pas
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

Crée `~/devops-project/prometheus.yml` :
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "backend"
    static_configs:
      - targets: ["backend:8000"]
```

Mets à jour `~/devops-project/docker-compose.yml` :
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    depends_on:
      - backend

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

### 3. Lancer

```bash
cd ~/devops-project
docker compose up -d --build

# Vérifier
docker compose ps
# 4 services running
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
5. Choisis la source Prometheus, et entre la requête :
   - `rate(http_requests_total[1m])` → nombre de requests per second
   - Clique **Run queries** → tu vois un graphique
6. Ajoute un autre panel :
   - `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` → response time au 95e percentile
7. **Save dashboard** → Nomme-le "DevOps Project"

### 6. Générer du traffic et observer

```bash
# Dans un terminal, bombarde l'API
for i in $(seq 1 100); do curl -s http://localhost:8000/api/tasks > /dev/null; done
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

- **Commence petit.** 4 métriques (les Golden Signals : latency, traffic, errors, saturation) valent mieux que 200 métriques que personne ne regarde.
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

- **PromQL** : le langage de requête de Prometheus (très demandé en entretien)
- **Loki** : système de logs par Grafana Labs (comme ELK mais plus simple)
- **OpenTelemetry** : le standard émergent pour l'instrumentation (metrics + logs + traces)
- **PagerDuty / OpsGenie** : plateformes d'alerting et d'astreinte
- **SRE practices** : SLI (indicateurs), SLO (objectifs), SLA (engagements) — le vocabulaire Google
