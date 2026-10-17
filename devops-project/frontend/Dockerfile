# Dockerfile du frontend — Multi-stage build (Bun → nginx)
# Étape 1 : Bun compile le code React en fichiers statiques (HTML/JS/CSS)
# Étape 2 : nginx sert ces fichiers statiques en production
# Résultat : l'image finale ne contient que nginx + les fichiers, pas Bun ni node_modules

# --- Étape 1 : Build ---
FROM oven/bun:latest AS build
WORKDIR /app
COPY package.json bun.lock ./
# Installer les dépendances (versions exactes du lockfile)
RUN bun install --frozen-lockfile
COPY . .
# Compiler React → fichiers statiques dans dist/
RUN bun run build

# --- Étape 2 : Production ---
# nginx:alpine = serveur web ultra-léger (~5 Mo)
FROM nginx:alpine
# Copier les fichiers buildés
COPY --from=build /app/dist /usr/share/nginx/html
# Config nginx (reverse proxy vers backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Le frontend est servi sur le port 80
EXPOSE 80
