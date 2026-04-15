# Questions d'entretien DevOps

Ce fichier est en deux parties :
1. **Définitions rapides** — les classiques "c'est quoi X", pour ne pas sécher sur les bases. Commence par là.
2. **Mises en situation** — des vrais problèmes qu'on te pose en entretien pour voir comment tu réfléchis

---

# Partie 1 : Définitions et questions techniques

Pour chaque techno, les questions qu'on te posera en entretien.

**Comment utiliser cette section :**
1. Lis la question et essaie d'y répondre toi-même (à voix haute c'est le mieux)
2. Si tu bloques, ouvre l'**indice** — il te donne une piste sans te donner la réponse
3. Ouvre la **réponse** pour comparer avec la tienne

## Git

**Q : C'est quoi Git ?**
<details><summary>💡 Indice</summary>Pense à un système de sauvegarde, avec un historique et la possibilité de travailler à plusieurs.</details>
<details><summary>✅ Réponse</summary>Système de versioning distribué. Garde l'historique de chaque modification du code, permet de travailler à plusieurs sans se marcher dessus.</details>

**Q : Merge vs Rebase ?**
<details><summary>💡 Indice</summary>Les deux servent à intégrer des changements d'une branche dans une autre. L'un garde l'historique tel quel, l'autre le réécrit.</details>
<details><summary>✅ Réponse</summary>Merge préserve l'historique (crée un commit de fusion). Rebase le réécrit (historique linéaire, plus propre, mais plus dangereux car on réécrit des commits).</details>

**Q : Pull vs Fetch ?**
<details><summary>💡 Indice</summary>Les deux récupèrent les changements distants. L'un les applique directement, l'autre non.</details>
<details><summary>✅ Réponse</summary>Fetch télécharge les changements distants sans les appliquer. Pull = fetch + merge. Pull applique directement.</details>

**Q : Un collègue et toi avez modifié la même ligne, que se passe-t-il ?**
<details><summary>💡 Indice</summary>Git ne peut pas choisir tout seul quelle version garder.</details>
<details><summary>✅ Réponse</summary>Un conflit de merge. Git te montre les deux versions, tu choisis laquelle garder (ou tu combines les deux), puis tu commit la résolution.</details>

**Q : C'est quoi votre workflow Git en équipe ?**
<details><summary>💡 Indice</summary>Pense au cycle : créer une branche → travailler → pousser → demander une revue → fusionner.</details>
<details><summary>✅ Réponse</summary>On crée une branche par feature, on commit dessus, on push, on ouvre une Pull Request. Un collègue review le code, et si c'est bon on merge dans main. Personne ne push directement sur main — tout passe par une PR.</details>

**Q : Quelle est la différence entre `git add` et `git commit` ?**
<details><summary>💡 Indice</summary>L'un prépare les fichiers, l'autre les sauvegarde. Pense à un carton qu'on remplit puis qu'on ferme.</details>
<details><summary>✅ Réponse</summary><code>git add</code> prépare les fichiers (staging area), <code>git commit</code> les sauvegarde dans l'historique. C'est comme mettre des objets dans un carton (add) puis fermer et étiqueter le carton (commit).</details>

**Q : C'est quoi une branche ?**
<details><summary>💡 Indice</summary>Pense à un univers parallèle du code où tu peux travailler sans toucher à la version principale.</details>
<details><summary>✅ Réponse</summary>Une copie parallèle du code. On développe dessus sans toucher à la branche principale (main). Quand c'est prêt, on fusionne (merge).</details>

**Q : C'est quoi une Pull Request ?**
<details><summary>💡 Indice</summary>C'est le mécanisme pour proposer ses changements à l'équipe avant de les intégrer dans la branche principale.</details>
<details><summary>✅ Réponse</summary>Une demande de fusion de code. Tu crées une branche, tu travailles dessus, et quand c'est prêt tu ouvres une PR sur GitHub. Un collègue relit ton code (code review), et si c'est bon, on fusionne dans main. Ça permet de vérifier le code avant qu'il arrive en production.</details>

## Linux

**Q : Explique les permissions 755**
<details><summary>💡 Indice</summary>3 blocs de 3 permissions (read, write, execute) pour 3 catégories de personnes. Chaque permission a une valeur numérique.</details>
<details><summary>✅ Réponse</summary>3 blocs (owner/group/others). read=4, write=2, execute=1. 755 = owner peut tout faire (7), group et others peuvent lire et exécuter (5).</details>

**Q : C'est quoi une variable d'environnement ?**
<details><summary>💡 Indice</summary>Pense à un moyen de passer de la configuration à une application sans la mettre dans le code.</details>
<details><summary>✅ Réponse</summary>Une valeur stockée dans le système, accessible par les programmes. Sert à passer de la configuration (URL de la base, clés API, mode debug) sans la mettre dans le code. <code>export MA_VAR="valeur"</code> pour en créer une.</details>

**Q : Un processus consomme tout le CPU, comment tu le trouves et tu le tues ?**
<details><summary>💡 Indice</summary>Il y a une commande pour lister les processus triés par consommation, et une autre pour arrêter un processus par son numéro (PID).</details>
<details><summary>✅ Réponse</summary><code>top</code> ou <code>ps aux</code> pour le trouver (tri par CPU), <code>kill &lt;PID&gt;</code> pour l'arrêter, <code>kill -9 &lt;PID&gt;</code> si ça ne suffit pas.</details>

**Q : Comment tu vérifies l'espace disque sur un serveur ?**
<details><summary>💡 Indice</summary>Une commande courte avec un flag qui rend la sortie lisible par un humain (human-readable).</details>
<details><summary>✅ Réponse</summary><code>df -h</code> — montre l'espace disque utilisé et disponible sur chaque partition. Le <code>-h</code> = human-readable (Go, Mo au lieu d'octets). Un disque plein c'est une cause fréquente de crash en prod.</details>

**Q : Comment tu vois quel processus écoute sur un port ?**
<details><summary>💡 Indice</summary>La commande <code>ss</code> avec les bons flags, combinée avec <code>grep</code> pour filtrer.</details>
<details><summary>✅ Réponse</summary><code>ss -tlnp | grep &lt;port&gt;</code> — ça montre le processus qui écoute sur ce port.</details>

**Q : C'est quoi sudo ?**
<details><summary>💡 Indice</summary>Pense à "Exécuter en tant qu'administrateur" sur Windows.</details>
<details><summary>✅ Réponse</summary>"Super User DO" — exécuter une commande en tant qu'administrateur (root). Nécessaire pour installer des logiciels, modifier la config système, etc.</details>

**Q : Différence entre `>` et `>>` ?**
<details><summary>💡 Indice</summary>Les deux redirigent la sortie d'une commande vers un fichier. L'un écrase, l'autre non.</details>
<details><summary>✅ Réponse</summary><code>></code> écrase le fichier. <code>>></code> ajoute à la fin du fichier. Exemple : <code>echo "log" > fichier.txt</code> remplace le contenu, <code>echo "log" >> fichier.txt</code> ajoute une ligne.</details>

**Q : Comment voir les logs d'un service ?**
<details><summary>💡 Indice</summary>Il y a une commande spécifique pour les services systemd, et un répertoire classique pour les logs système.</details>
<details><summary>✅ Réponse</summary><code>journalctl -u nom_du_service</code> pour les services systemd, ou regarder dans <code>/var/log/</code> pour les logs système classiques.</details>

**Q : C'est quoi un processus ?**
<details><summary>💡 Indice</summary>Chaque programme qui tourne sur ta machine en est un. Chacun a un numéro unique.</details>
<details><summary>✅ Réponse</summary>Un programme en cours d'exécution. Quand tu lances <code>python3 main.py</code>, ça crée un processus. Chaque processus a un numéro unique (PID). Tu peux les voir avec <code>ps aux</code> ou <code>top</code>.</details>

**Q : C'est quoi le PATH ?**
<details><summary>💡 Indice</summary>C'est ce que le système consulte quand tu tapes le nom d'un programme dans le terminal. Si le programme n'y est pas...</details>
<details><summary>✅ Réponse</summary>Une variable d'environnement qui contient la liste des dossiers où le système cherche les programmes. Quand tu tapes <code>python3</code>, Linux parcourt les dossiers du PATH pour trouver le fichier. Si tu as "command not found", c'est souvent que le programme n'est pas dans le PATH.</details>

## Réseau

**Q : C'est quoi une adresse IP ?**
<details><summary>💡 Indice</summary>C'est un identifiant. Il en existe deux types selon qu'on est sur Internet ou en local.</details>
<details><summary>✅ Réponse</summary>Identifiant d'une machine sur le réseau. Publique = visible sur Internet. Privée = visible uniquement en local.</details>

**Q : C'est quoi un port ?**
<details><summary>💡 Indice</summary>Une machine peut faire tourner plusieurs services (web, SSH, base de données). Le port identifie lequel.</details>
<details><summary>✅ Réponse</summary>Numéro (1-65535) qui identifie un service sur une machine. 22=SSH, 80=HTTP, 443=HTTPS, 5432=PostgreSQL.</details>

**Q : C'est quoi le DNS ?**
<details><summary>💡 Indice</summary>Pense à un annuaire qui traduit quelque chose de lisible par un humain en quelque chose de lisible par une machine.</details>
<details><summary>✅ Réponse</summary>Le système qui traduit les noms de domaine (google.com) en adresses IP. Sans DNS, il faudrait retenir les IP de tous les sites.</details>

**Q : Différence entre TCP et UDP ?**
<details><summary>💡 Indice</summary>L'un est fiable mais plus lent, l'autre est rapide mais ne vérifie rien. Pense à HTTP vs streaming vidéo.</details>
<details><summary>✅ Réponse</summary>TCP est fiable (vérifie que les données arrivent dans l'ordre). UDP est rapide (pas de vérification). HTTP utilise TCP, le streaming vidéo utilise souvent UDP.</details>

**Q : Un utilisateur te dit "le site ne marche pas", par quoi tu commences ?**
<details><summary>💡 Indice</summary>Une commande qui te donne le code de réponse HTTP. Le code te dit quel type de problème c'est (réseau, proxy, code).</details>
<details><summary>✅ Réponse</summary><code>curl</code> le site pour voir le code de réponse (200, 502, timeout). Si timeout → problème réseau/DNS. Si 502 → l'app derrière le proxy est down. Si 500 → bug dans le code.</details>

**Q : Qu'est-ce qu'il se passe quand tu tapes une URL dans ton navigateur ?**
<details><summary>💡 Indice</summary>5 étapes : résolution d'adresse, envoi de requête, traitement côté serveur, réponse, affichage. Pense à DNS, HTTP, et au navigateur.</details>
<details><summary>✅ Réponse</summary>1. <strong>Résolution DNS</strong> — le navigateur demande à un DNS de traduire le nom de domaine en adresse IP. 2. <strong>Envoi de la requête</strong> — le navigateur envoie une requête HTTP au serveur. 3. <strong>Traitement côté serveur</strong> — le serveur reçoit la requête et prépare la réponse. 4. <strong>Réponse du serveur</strong> — le serveur renvoie le contenu (HTML/CSS/JS et données en JSON). 5. <strong>Affichage</strong> — le navigateur assemble et affiche la page.</details>

**Q : C'est quoi un CIDR /24 ?**
<details><summary>💡 Indice</summary>C'est une notation pour décrire un sous-réseau. Le nombre après le / indique combien d'adresses IP sont disponibles.</details>
<details><summary>✅ Réponse</summary>Un sous-réseau de 256 adresses IP. Exemple : 10.0.1.0/24 = 10.0.1.0 à 10.0.1.255. Plus le nombre après le / est grand, moins il y a d'adresses.</details>

**Q : C'est quoi un firewall ?**
<details><summary>💡 Indice</summary>Pense à un vigile qui contrôle qui entre et qui sort d'un bâtiment.</details>
<details><summary>✅ Réponse</summary>Un filtre qui contrôle le traffic réseau entrant et sortant. Il autorise ou bloque le traffic en fonction de règles (port, IP source, protocole). Sur Linux, <code>ufw</code> est un outil simple pour configurer le firewall.</details>

**Q : Que signifie un code 502 ?**
<details><summary>💡 Indice</summary>C'est un problème de proxy — le serveur qui reçoit ta requête n'arrive pas à joindre le serveur derrière lui.</details>
<details><summary>✅ Réponse</summary>Bad Gateway — le serveur proxy/load balancer n'arrive pas à joindre le serveur d'application derrière lui. Cause fréquente : l'application a crashé.</details>

**Q : Différence entre HTTP et HTTPS ?**
<details><summary>💡 Indice</summary>Le S à la fin veut dire "Secure". Pense au cadenas dans la barre d'adresse du navigateur.</details>
<details><summary>✅ Réponse</summary>HTTPS = HTTP + chiffrement (TLS/SSL). Les données sont chiffrées entre ton navigateur et le serveur — personne ne peut les lire en transit. Le cadenas dans le navigateur = HTTPS. Aujourd'hui, tout site sérieux doit être en HTTPS.</details>

**Q : C'est quoi un reverse proxy ?**
<details><summary>💡 Indice</summary>C'est un serveur intermédiaire entre les utilisateurs et ton application. Il peut faire plusieurs choses utiles (distribution de traffic, HTTPS, cache).</details>
<details><summary>✅ Réponse</summary>Un serveur qui se place devant ton application et reçoit les requêtes à sa place. Il peut distribuer le traffic entre plusieurs serveurs, gérer le HTTPS, mettre en cache, etc. Nginx est le reverse proxy le plus courant.</details>

**Q : C'est quoi un load balancer ?**
<details><summary>💡 Indice</summary>Si tu as plusieurs serveurs, comment tu répartis les requêtes entre eux ?</details>
<details><summary>✅ Réponse</summary>Un outil qui répartit le traffic entre plusieurs serveurs. Si tu as 3 serveurs backend, le load balancer envoie chaque requête à un serveur différent pour répartir la charge. Si un serveur tombe, le load balancer arrête de lui envoyer du traffic.</details>

## Docker

**Q : Différence entre image et container ?**
<details><summary>💡 Indice</summary>Pense à une recette de cuisine vs un plat cuisiné. L'un est un template, l'autre est une instance en cours.</details>
<details><summary>✅ Réponse</summary>Image = template en lecture seule (la recette). Container = instance en cours d'exécution (le plat cuisiné). Une image peut créer plusieurs containers.</details>

**Q : C'est quoi un Dockerfile ?**
<details><summary>💡 Indice</summary>Un fichier texte avec des instructions. Pense aux mots-clés : FROM, COPY, RUN, CMD.</details>
<details><summary>✅ Réponse</summary>Fichier texte qui décrit étape par étape comment construire une image Docker. FROM pour la base, COPY pour les fichiers, RUN pour les commandes, CMD pour le lancement.</details>

**Q : Un container crash en boucle, comment tu débugues ?**
<details><summary>💡 Indice</summary>La première chose c'est toujours les logs. Si le container ne tourne plus, il y a une façon de lancer l'image avec un shell au lieu de l'app.</details>
<details><summary>✅ Réponse</summary><code>docker logs &lt;container&gt;</code> pour lire les logs. Si le container ne tourne plus, <code>docker run -it --entrypoint bash &lt;image&gt;</code> pour rentrer dedans et investiguer manuellement.</details>

**Q : Pourquoi utiliser un multi-stage build ?**
<details><summary>💡 Indice</summary>Le but c'est la taille de l'image finale. On sépare la phase de construction et la phase d'exécution.</details>
<details><summary>✅ Réponse</summary>Pour réduire la taille de l'image finale. On build dans une image lourde (avec les outils de build), puis on copie uniquement le résultat dans une image légère. Le frontend passe de 500 Mo à 20 Mo.</details>

**Q : Comment les containers communiquent entre eux dans Docker Compose ?**
<details><summary>💡 Indice</summary>Docker Compose crée quelque chose automatiquement qui permet aux containers de se trouver par leur nom de service.</details>
<details><summary>✅ Réponse</summary>Via un réseau interne créé automatiquement. Chaque container est accessible par le nom de son service (ex: <code>backend:8000</code>, <code>db:5432</code>). C'est du service discovery par DNS interne.</details>

**Q : Différence entre CMD et ENTRYPOINT ?**
<details><summary>💡 Indice</summary>L'un est remplaçable au lancement, l'autre non. Lequel utilise-t-on dans 90% des cas ?</details>
<details><summary>✅ Réponse</summary>CMD = commande par défaut, remplaçable au lancement. ENTRYPOINT = commande fixe, les arguments du <code>docker run</code> sont ajoutés après. En pratique, CMD suffit dans 90% des cas.</details>

**Q : C'est quoi Docker ?**
<details><summary>💡 Indice</summary>Pense à un moyen d'emballer une application avec tout ce dont elle a besoin pour tourner partout de la même façon.</details>
<details><summary>✅ Réponse</summary>Un outil qui empaquète une application avec toutes ses dépendances dans un container isolé. Le container tourne de la même façon partout (ton PC, un serveur, le cloud).</details>

**Q : C'est quoi Docker Compose ?**
<details><summary>💡 Indice</summary>Quand tu as plusieurs containers (backend, frontend, base de données), il te faut un outil pour les gérer ensemble.</details>
<details><summary>✅ Réponse</summary>Un outil pour gérer plusieurs containers ensemble avec un fichier YAML. Tu définis tes services, réseaux et volumes, puis <code>docker compose up</code> lance tout d'un coup.</details>

**Q : C'est quoi un volume Docker ?**
<details><summary>💡 Indice</summary>Par défaut, les données d'un container disparaissent quand il est supprimé. Comment on persiste les données ?</details>
<details><summary>✅ Réponse</summary>Un stockage persistant. Sans volume, les données disparaissent quand le container est supprimé. Essentiel pour les bases de données — les données survivent au redémarrage du container.</details>

**Q : Différence entre COPY et ADD dans un Dockerfile ?**
<details><summary>💡 Indice</summary>Les deux copient des fichiers. L'un fait plus de choses que l'autre — mais est-ce toujours souhaitable ?</details>
<details><summary>✅ Réponse</summary>Les deux copient des fichiers dans l'image. <code>COPY</code> fait une simple copie. <code>ADD</code> peut en plus décompresser des archives (.tar.gz) et télécharger depuis une URL. En pratique, utilise toujours <code>COPY</code> — c'est plus explicite.</details>

**Q : C'est quoi un registry Docker ?**
<details><summary>💡 Indice</summary>Pense à GitHub, mais pour les images Docker au lieu du code source.</details>
<details><summary>✅ Réponse</summary>Un serveur qui stocke des images Docker. Docker Hub est le registry public par défaut. En entreprise, on utilise souvent un registry privé (AWS ECR, GitHub Container Registry) pour stocker ses propres images.</details>

**Q : Pourquoi l'ordre des instructions dans un Dockerfile est important ?**
<details><summary>💡 Indice</summary>Docker utilise un système de cache par couches. Si une couche change, toutes celles d'après sont reconstruites.</details>
<details><summary>✅ Réponse</summary>À cause du cache. Docker exécute chaque instruction comme une couche (layer). Si une couche n'a pas changé, Docker réutilise le cache. En mettant <code>COPY requirements.txt</code> + <code>RUN pip install</code> AVANT <code>COPY . .</code>, les dépendances ne sont réinstallées que quand elles changent vraiment — pas à chaque modification de code.</details>

## CI/CD

**Q : C'est quoi CI/CD ?**
<details><summary>💡 Indice</summary>CI = avant le déploiement (vérifier). CD = le déploiement lui-même (livrer).</details>
<details><summary>✅ Réponse</summary>CI = vérification automatique à chaque push (lint, tests). CD = déploiement automatique (ou semi-automatique). L'objectif : détecter les bugs le plus tôt possible et déployer en confiance.</details>

**Q : C'est quoi le "fail fast" ?**
<details><summary>💡 Indice</summary>Si une étape rapide échoue, est-ce qu'on lance quand même les étapes longues ?</details>
<details><summary>✅ Réponse</summary>Si le lint échoue, on ne lance pas les tests. Si les tests échouent, on ne build pas. On arrête dès qu'un problème est détecté pour ne pas perdre de temps.</details>

**Q : Où tu mets les secrets dans un pipeline ?**
<details><summary>💡 Indice</summary>Jamais dans le code, jamais dans le YAML committé. Il y a un endroit dédié dans GitHub/GitLab pour ça.</details>
<details><summary>✅ Réponse</summary>Dans les secrets du CI (GitHub Secrets, GitLab Variables). Ils sont injectés au moment de l'exécution et n'apparaissent jamais dans les logs.</details>

**Q : Un test passe en local mais échoue en CI, pourquoi ?**
<details><summary>💡 Indice</summary>Pense aux différences entre ta machine et le runner CI : versions, variables d'environnement, services disponibles.</details>
<details><summary>✅ Réponse</summary>Souvent une différence d'environnement : version de Python/Node différente, variable d'environnement manquante, dépendance pas installée, ou le test dépend d'un service (DB) qui n'existe pas en CI.</details>

**Q : Comment tu fais un rollback si le déploiement casse la prod ?**
<details><summary>💡 Indice</summary>Les images Docker sont taggées avec le hash du commit. Comment tu utilises ça pour revenir en arrière ?</details>
<details><summary>✅ Réponse</summary>On redéploie l'image Docker précédente. C'est pour ça qu'on tag les images avec le hash du commit — on peut revenir à n'importe quelle version en quelques minutes.</details>

**Q : Quelles sont les étapes d'un pipeline CI/CD typique ?**
<details><summary>💡 Indice</summary>4 étapes dans l'ordre. Si la première échoue, les suivantes ne se lancent pas.</details>
<details><summary>✅ Réponse</summary>Lint (qualité du code) → Tests → Build (construction de l'artefact) → Deploy. Chaque étape bloque la suivante si elle échoue.</details>

**Q : Différence entre Continuous Delivery et Continuous Deployment ?**
<details><summary>💡 Indice</summary>Les deux commencent par "Continuous D...". La différence : est-ce qu'un humain appuie sur un bouton avant la prod ?</details>
<details><summary>✅ Réponse</summary>Delivery = prêt à déployer mais bouton manuel. Deployment = déploiement automatique en prod. La plupart des entreprises font du Delivery (un humain valide avant la prod).</details>

**Q : C'est quoi un runner ?**
<details><summary>💡 Indice</summary>Le pipeline ne s'exécute pas tout seul dans le vide — il a besoin d'une machine pour tourner.</details>
<details><summary>✅ Réponse</summary>La machine (serveur) qui exécute les jobs du pipeline. GitHub fournit des runners gratuits (<code>ubuntu-latest</code>). On peut aussi utiliser ses propres runners (self-hosted) pour plus de contrôle.</details>

**Q : C'est quoi un blue/green deployment ?**
<details><summary>💡 Indice</summary>Deux environnements identiques. Un sert la prod, l'autre attend la nouvelle version. On bascule le traffic d'un coup.</details>
<details><summary>✅ Réponse</summary>Une stratégie de déploiement avec deux environnements identiques. Le "blue" sert la prod, on déploie la nouvelle version sur le "green", on teste, puis on bascule le traffic. Si ça casse, on rebascule en quelques secondes. Avantage : rollback instantané.</details>

**Q : C'est quoi un canary deployment ?**
<details><summary>💡 Indice</summary>Au lieu de déployer pour tout le monde d'un coup, on commence par un petit pourcentage. Le nom vient des canaris dans les mines.</details>
<details><summary>✅ Réponse</summary>On déploie la nouvelle version sur un petit pourcentage de serveurs (ex: 5%). On surveille les métriques. Si tout va bien, on augmente progressivement (25% → 50% → 100%). Si ça casse, seul 5% des utilisateurs sont impactés.</details>

## AWS

### EC2

**Q : C'est quoi EC2 ?**
<details><summary>💡 Indice</summary>Pense à louer un ordinateur au lieu d'en acheter un.</details>
<details><summary>✅ Réponse</summary>Un serveur virtuel dans le cloud. Tu choisis la puissance (CPU, RAM), l'OS, et tu paies à l'heure.</details>

**Q : Comment tu te connectes à un EC2 ?**
<details><summary>💡 Indice</summary>Un protocole de connexion à distance + un fichier de clé téléchargé à la création de l'instance.</details>
<details><summary>✅ Réponse</summary>En SSH avec une key pair : <code>ssh -i ~/devops-key.pem ubuntu@IP_PUBLIQUE</code>. La clé .pem est téléchargée à la création de l'instance.</details>

**Q : Ton EC2 ne répond plus, quelles sont les premières choses que tu vérifies ?**
<details><summary>💡 Indice</summary>3 choses : l'instance elle-même (elle tourne ?), le réseau (le port est ouvert ?), et l'adresse (elle a une IP publique ?).</details>
<details><summary>✅ Réponse</summary>1. L'instance est "Running" dans la console AWS ? 2. Le Security Group autorise le port SSH (22) et HTTP (80) ? 3. L'instance a une IP publique ? 4. Si tout est OK côté AWS, se connecter en SSH et vérifier les logs de l'app.</details>

### VPC et réseau

**Q : C'est quoi un VPC ?**
<details><summary>💡 Indice</summary>C'est ton réseau privé dans AWS. Tu y mets tes ressources et tu contrôles qui peut accéder à quoi.</details>
<details><summary>✅ Réponse</summary>Virtual Private Cloud — un réseau isolé dans AWS. Tu y mets tes ressources (EC2, RDS). Tu contrôles les subnets, le routage, et les accès.</details>

**Q : Différence entre subnet public et privé ?**
<details><summary>💡 Indice</summary>L'un est accessible depuis Internet, l'autre non. Pense à où tu mettrais un serveur web vs une base de données.</details>
<details><summary>✅ Réponse</summary>Public = accessible depuis Internet (via Internet Gateway). Privé = pas d'accès direct depuis Internet. On met les serveurs web en public, les bases de données en privé.</details>

**Q : C'est quoi un Security Group ?**
<details><summary>💡 Indice</summary>C'est comme un firewall. Il contrôle le traffic par port et par source. Il est "stateful" — qu'est-ce que ça veut dire ?</details>
<details><summary>✅ Réponse</summary>Firewall virtuel attaché à une instance. Il filtre le traffic entrant (ingress) et sortant (egress) par port et IP source. "Stateful" = si tu autorises le traffic entrant sur un port, la réponse sortante est automatiquement autorisée.</details>

**Q : C'est quoi un Internet Gateway ?**
<details><summary>💡 Indice</summary>Sans ça, ton VPC est complètement isolé d'Internet. C'est la porte entre ton réseau privé et le monde extérieur.</details>
<details><summary>✅ Réponse</summary>La porte qui connecte ton VPC à Internet. Sans Internet Gateway, aucune ressource dans le VPC ne peut accéder à Internet (et personne ne peut y accéder depuis Internet).</details>

### RDS

**Q : Pourquoi utiliser RDS au lieu d'installer PostgreSQL sur un EC2 ?**
<details><summary>💡 Indice</summary>Pense à tout ce que tu n'as PAS à gérer avec RDS : les backups, les mises à jour, la haute disponibilité.</details>
<details><summary>✅ Réponse</summary>RDS gère les backups automatiques, les security updates, la replication et la haute disponibilité. Tu n'as pas à maintenir le serveur de base de données toi-même. Le surcoût est compensé par le temps gagné.</details>

**Q : C'est quoi Multi-AZ sur RDS ?**
<details><summary>💡 Indice</summary>Ta base est copiée dans un 2ème endroit. Si le premier tombe...</details>
<details><summary>✅ Réponse</summary>Ta base de données est automatiquement répliquée dans un 2ème datacenter (Availability Zone). Si le premier tombe en panne, le 2ème prend le relais automatiquement. C'est la haute disponibilité.</details>

**Q : Comment tu protèges ta base de données sur AWS ?**
<details><summary>💡 Indice</summary>Pense au subnet (où elle est placée) et au Security Group (qui a le droit de s'y connecter).</details>
<details><summary>✅ Réponse</summary>Tu la mets dans un subnet privé (pas d'IP publique), avec un Security Group qui n'autorise le port 5432 que depuis le Security Group de l'EC2. Jamais d'accès direct depuis Internet.</details>

### S3

**Q : C'est quoi S3 ?**
<details><summary>💡 Indice</summary>Du stockage de fichiers dans le cloud. Illimité, haute durabilité, pas cher.</details>
<details><summary>✅ Réponse</summary>Simple Storage Service — stockage d'objets (fichiers) illimité dans le cloud. Utilisé pour les backups, les fichiers statiques (images, CSS, JS d'un frontend), les logs, les exports de données.</details>

**Q : Comment tu sécurises un bucket S3 ?**
<details><summary>💡 Indice</summary>Par défaut un bucket est privé. Le danger c'est de le rendre public par erreur.</details>
<details><summary>✅ Réponse</summary>Par défaut, un bucket S3 est privé (c'est bien). On vérifie que "Block all public access" est activé. On contrôle l'accès via des bucket policies et des rôles IAM. Jamais d'accès public sauf pour du contenu statique intentionnellement public (frontend).</details>

### IAM

**Q : C'est quoi IAM ?**
<details><summary>💡 Indice</summary>Le système de permissions d'AWS. Qui a le droit de faire quoi.</details>
<details><summary>✅ Réponse</summary>Identity and Access Management. Gère les utilisateurs (Users), les rôles (Roles) et les permissions (Policies). Le principe clé : le moindre privilège — on ne donne que les droits strictement nécessaires.</details>

**Q : User vs Role, quelle différence ?**
<details><summary>💡 Indice</summary>L'un est permanent (une personne ou un programme), l'autre est temporaire (on l'"enfile" quand on en a besoin).</details>
<details><summary>✅ Réponse</summary>User = un compte permanent pour une personne ou un programme (avec des credentials fixes). Role = un ensemble de permissions temporaires qu'un service peut "enfiler" (ex: un EC2 qui a besoin d'accéder à S3 utilise un rôle, pas un user).</details>

### Lambda et SQS

**Q : Quand utiliser Lambda vs EC2 ?**
<details><summary>💡 Indice</summary>Pense à la durée d'exécution et à la fréquence. L'un tourne 24/7, l'autre s'exécute à la demande.</details>
<details><summary>✅ Réponse</summary>Lambda = tâches courtes (&lt;15 min), ponctuelles, avec scaling automatique (webhooks, traitement de fichiers). EC2 = applications qui tournent en continu 24/7 (API web, serveur). Lambda tu paies à l'exécution, EC2 tu paies à l'heure même au repos.</details>

**Q : C'est quoi SQS et pourquoi c'est utile ?**
<details><summary>💡 Indice</summary>Pense à une file d'attente. Au lieu de traiter les messages directement (et risquer de les perdre si ça crash), on les met dans...</details>
<details><summary>✅ Réponse</summary>Simple Queue Service — une file d'attente managée. Tu y mets des messages, un autre programme les consomme. Si le consommateur crash, le message reste dans la file et sera re-traité. Utile pour découpler les services, absorber les pics de traffic, et ne jamais perdre de données.</details>

### ECS et EKS

**Q : C'est quoi la différence entre ECS et EKS ?**
<details><summary>💡 Indice</summary>Les deux font tourner des containers sur AWS. L'un est spécifique AWS et plus simple, l'autre est un standard portable.</details>
<details><summary>✅ Réponse</summary>ECS = orchestration de containers spécifique AWS (plus simple, pas de frais de control plane). EKS = Kubernetes managé (standard, portable multi-cloud, mais plus complexe et plus cher ~75$/mois de base).</details>

**Q : C'est quoi Fargate ?**
<details><summary>💡 Indice</summary>Un mode d'ECS où tu ne gères aucun serveur. Tu donnes juste ton image Docker et la quantité de CPU/RAM.</details>
<details><summary>✅ Réponse</summary>Mode "serverless" d'ECS — tu donnes ton image Docker, tu définis CPU et RAM, AWS lance le container quelque part dans le cloud. Tu ne vois jamais de machine, tu ne gères aucun serveur. Tu paies uniquement le CPU/RAM utilisé.</details>

**Q : C'est quoi AWS ?**
<details><summary>💡 Indice</summary>Le plus gros fournisseur de cloud au monde. Tu loues des ressources informatiques au lieu de les acheter.</details>
<details><summary>✅ Réponse</summary>Un fournisseur de cloud computing. Tu loues des serveurs (EC2), du stockage (S3), des bases de données (RDS) et plein d'autres services, à la demande. Tu paies ce que tu utilises.</details>

**Q : C'est quoi RDS ?**
<details><summary>💡 Indice</summary>Pense à une base de données dont AWS gère toute la maintenance pour toi.</details>
<details><summary>✅ Réponse</summary>Relational Database Service — une base de données managée par AWS. Tu choisis le moteur (PostgreSQL, MySQL...), AWS gère les backups, updates, et haute disponibilité.</details>

**Q : C'est quoi DynamoDB ?**
<details><summary>💡 Indice</summary>C'est l'alternative NoSQL d'AWS. Au lieu de tableaux SQL avec colonnes fixes, on stocke...</details>
<details><summary>✅ Réponse</summary>Une base de données NoSQL managée par AWS. Au lieu de tableaux SQL avec des colonnes fixes, tu stockes des documents JSON flexibles. Le scaling est automatique et le prix est à la requête.</details>

**Q : Quand utiliser RDS vs DynamoDB ?**
<details><summary>💡 Indice</summary>Pense au type de données : est-ce qu'elles ont des relations entre elles (users → commandes → produits) ?</details>
<details><summary>✅ Réponse</summary>RDS quand tes données ont des relations entre elles et que tu as besoin de requêtes SQL complexes. DynamoDB quand tu as des données simples à très fort traffic (sessions, cache, compteurs). En cas de doute, RDS — c'est plus polyvalent.</details>

**Q : C'est quoi ECS ?**
<details><summary>💡 Indice</summary>Tu lui donnes des images Docker, il les fait tourner, les surveille et les scale. Avec Fargate, tu n'as même pas de serveur à gérer.</details>
<details><summary>✅ Réponse</summary>Elastic Container Service — tu donnes tes images Docker à AWS, et il les lance, les surveille et les scale. Avec Fargate, tu ne gères aucun serveur — tu paies uniquement le CPU et la RAM utilisés.</details>

**Q : C'est quoi EKS ?**
<details><summary>💡 Indice</summary>Kubernetes managé sur AWS. AWS gère une partie, toi tu gères l'autre. L'avantage c'est la portabilité.</details>
<details><summary>✅ Réponse</summary>Elastic Kubernetes Service — Kubernetes managé sur AWS. AWS gère le control plane, toi tu gères les workers. L'avantage par rapport à ECS : K8s est un standard portable sur n'importe quel cloud.</details>

**Q : C'est quoi Lambda ?**
<details><summary>💡 Indice</summary>Du code qui s'exécute sans serveur. Tu paies uniquement quand ton code tourne.</details>
<details><summary>✅ Réponse</summary>Du serverless — tu envoies ton code, AWS l'exécute quand il faut, tu paies à l'exécution. Pas de serveur à gérer. Idéal pour des tâches courtes et ponctuelles (&lt;15 min).</details>

**Q : Quand utiliser Lambda vs EC2 vs ECS ?**
<details><summary>💡 Indice</summary>Pense à la durée d'exécution et à si l'app doit tourner en permanence ou non.</details>
<details><summary>✅ Réponse</summary>Lambda pour les tâches courtes (&lt;15 min) et ponctuelles. ECS/EKS pour des apps containerisées qui tournent en continu avec du scaling automatique. EC2 quand tu as besoin de contrôle total sur le serveur ou pour des petits projets simples.</details>

**Q : C'est quoi un cold start ?**
<details><summary>💡 Indice</summary>La première exécution d'une Lambda est plus lente. Pourquoi ?</details>
<details><summary>✅ Réponse</summary>La première exécution d'une Lambda est plus lente parce qu'AWS doit démarrer un environnement. Les exécutions suivantes (warm start) sont plus rapides car l'environnement est déjà prêt.</details>

**Q : Différence entre scaling horizontal et vertical ?**
<details><summary>💡 Indice</summary>L'un ajoute de la puissance à une machine, l'autre ajoute des machines. Lequel a une limite physique ?</details>
<details><summary>✅ Réponse</summary>Vertical = augmenter la puissance d'une machine (plus de CPU, plus de RAM). Horizontal = ajouter plus de machines. Le vertical a une limite physique, le horizontal est quasi illimité. En cloud, on privilégie le scaling horizontal.</details>

**Q : C'est quoi le modèle de responsabilité partagée ?**
<details><summary>💡 Indice</summary>AWS et toi avez chacun une part de responsabilité en matière de sécurité. Qui gère quoi ?</details>
<details><summary>✅ Réponse</summary>AWS gère la sécurité <strong>du</strong> cloud (datacenters, réseau physique, hyperviseurs). Toi tu gères la sécurité <strong>dans</strong> le cloud (tes données, tes Security Groups, tes IAM policies, ton code). Si ton Security Group est ouvert à tout le monde, c'est ta faute, pas celle d'AWS.</details>

## Terraform

**Q : C'est quoi Infrastructure as Code ?**
<details><summary>💡 Indice</summary>Au lieu de cliquer dans une console pour créer des serveurs, tu fais quoi ?</details>
<details><summary>✅ Réponse</summary>Décrire ton infra dans des fichiers de code au lieu de cliquer dans une console. Reproductible, versionné dans Git, auditable, partageable.</details>

**Q : Explique plan, apply, destroy**
<details><summary>💡 Indice</summary>Trois étapes : prévisualiser, exécuter, supprimer. Laquelle fait-on toujours en premier ?</details>
<details><summary>✅ Réponse</summary><code>plan</code> montre ce qui va changer sans rien faire. <code>apply</code> exécute les changements. <code>destroy</code> supprime tout. On fait toujours plan avant apply pour vérifier.</details>

**Q : C'est quoi le state file et pourquoi il est important ?**
<details><summary>💡 Indice</summary>Terraform a besoin de savoir ce qui existe ACTUELLEMENT pour comparer avec ce que tu veux. Il stocke ça dans un fichier.</details>
<details><summary>✅ Réponse</summary>Fichier JSON qui enregistre l'état actuel de l'infra. Terraform le compare avec ton code pour savoir quoi créer/modifier/supprimer. Ne jamais le modifier à la main, ne jamais le committer (il peut contenir des secrets).</details>

**Q : Comment tu intéragis avec une ressource qui existe déjà sur AWS mais pas dans ton Terraform ?**
<details><summary>💡 Indice</summary>Il y a un mot-clé différent de <code>resource</code> qui va CHERCHER une info au lieu de CRÉER quelque chose.</details>
<details><summary>✅ Réponse</summary>Avec un bloc <code>data</code>. Contrairement à <code>resource</code> qui crée quelque chose, <code>data</code> va chercher une information qui existe déjà (une AMI, un VPC, un Security Group existant).</details>

**Q : Quelqu'un a modifié l'infra à la main dans la console AWS, que se passe-t-il ?**
<details><summary>💡 Indice</summary>Le state file ne correspond plus à la réalité. Terraform va détecter la différence au prochain <code>plan</code>. Comment on appelle ça ?</details>
<details><summary>✅ Réponse</summary>C'est du drift. Au prochain <code>terraform plan</code>, Terraform montre les différences entre le code et la réalité. Soit on importe le changement dans le code, soit <code>apply</code> écrase le changement manuel.</details>

**Q : C'est quoi Terraform ?**
<details><summary>💡 Indice</summary>Un outil pour décrire ton infrastructure dans des fichiers de code au lieu de cliquer dans une console.</details>
<details><summary>✅ Réponse</summary>Un outil d'Infrastructure as Code. Tu décris ton infra dans des fichiers HCL, Terraform la crée/modifie/supprime. Versionnable, reproductible, collaboratif.</details>

**Q : Terraform vs CloudFormation ?**
<details><summary>💡 Indice</summary>L'un est multi-cloud, l'autre est spécifique à un seul cloud provider.</details>
<details><summary>✅ Réponse</summary>Terraform est multi-cloud (AWS, GCP, Azure). CloudFormation est spécifique AWS. Terraform a une communauté plus large et une syntaxe plus lisible.</details>

**Q : C'est quoi un module Terraform ?**
<details><summary>💡 Indice</summary>Pense à une fonction en programmation — du code réutilisable qu'on appelle avec des paramètres.</details>
<details><summary>✅ Réponse</summary>Un bloc de code Terraform réutilisable. Au lieu de copier-coller la même config pour chaque environnement, tu crées un module et tu l'appelles avec des paramètres différents. C'est comme une fonction en programmation.</details>

**Q : C'est quoi un provider Terraform ?**
<details><summary>💡 Indice</summary>Terraform tout seul ne sait rien faire. Il a besoin de plugins pour parler à AWS, GCP, etc.</details>
<details><summary>✅ Réponse</summary>Un plugin qui connecte Terraform à un service (AWS, GCP, Azure, GitHub...). Le provider AWS permet à Terraform de créer des EC2, S3, RDS. Sans provider, Terraform ne sait pas parler à quoi que ce soit.</details>

## Ansible

**Q : C'est quoi Ansible ?**
<details><summary>💡 Indice</summary>Outil de configuration de serveurs. Le mot-clé c'est "agentless" — il n'a pas besoin d'installer quoi que ce soit sur le serveur cible.</details>
<details><summary>✅ Réponse</summary>Outil de gestion de configuration. Configure des serveurs de manière automatisée, agentless (se connecte en SSH, pas besoin d'installer quoi que ce soit sur le serveur cible).</details>

**Q : Ansible vs Terraform ?**
<details><summary>💡 Indice</summary>L'un crée l'infra, l'autre configure ce qui tourne dessus. Pense "construire la maison" vs "la meubler".</details>
<details><summary>✅ Réponse</summary>Terraform crée l'infra (le serveur existe). Ansible configure ce qui tourne dessus (installe Docker, copie les fichiers, lance l'app). Terraform construit la maison, Ansible la meuble.</details>

**Q : C'est quoi l'idempotence ?**
<details><summary>💡 Indice</summary>Que se passe-t-il si tu lances le même playbook 10 fois de suite ?</details>
<details><summary>✅ Réponse</summary>Exécuter un playbook plusieurs fois donne toujours le même résultat. Si Docker est déjà installé, Ansible ne le réinstalle pas. C'est ce qui le rend sûr à relancer.</details>

**Q : C'est quoi un playbook ?**
<details><summary>💡 Indice</summary>C'est un fichier dans un format que tu connais bien (utilisé partout en DevOps). Il décrit des tâches à exécuter.</details>
<details><summary>✅ Réponse</summary>Un fichier YAML qui décrit les tâches à exécuter sur les serveurs. Chaque tâche utilise un module (apt, copy, service) et est nommée pour la lisibilité.</details>

**Q : Comment tu gères les secrets dans Ansible ?**
<details><summary>💡 Indice</summary>Ansible a un outil intégré pour chiffrer des fichiers. Son nom fait penser à un coffre-fort.</details>
<details><summary>✅ Réponse</summary>Avec Ansible Vault. Tu chiffres les fichiers contenant des secrets, et au moment de l'exécution tu passes <code>--ask-vault-pass</code> pour les déchiffrer.</details>

**Q : C'est quoi un inventory Ansible ?**
<details><summary>💡 Indice</summary>Ansible doit savoir sur quelles machines agir. Il y a un fichier pour ça.</details>
<details><summary>✅ Réponse</summary>Le fichier qui liste les serveurs sur lesquels Ansible va agir. Il contient les adresses IP ou noms des machines, organisées en groupes (web, db, etc.). Ansible se connecte en SSH à chaque machine de l'inventory pour exécuter les tâches.</details>

**Q : C'est quoi un role Ansible ?**
<details><summary>💡 Indice</summary>Quand ton playbook grossit, il faut l'organiser en composants réutilisables.</details>
<details><summary>✅ Réponse</summary>Une façon d'organiser un playbook en composants réutilisables. Un role regroupe les tâches, fichiers, templates et variables liés à une fonction (ex: un role "docker" qui installe et configure Docker). On peut réutiliser le même role dans plusieurs playbooks.</details>

## Kubernetes

**Q : C'est quoi Kubernetes ?**
<details><summary>💡 Indice</summary>Pense à un chef d'orchestre pour les containers. Il gère 3 choses principales : déploiement, scaling, et...</details>
<details><summary>✅ Réponse</summary>Un orchestrateur de containers. Il gère le déploiement, le scaling et la haute disponibilité de tes containers sur un cluster de machines.</details>

**Q : C'est quoi un Pod ?**
<details><summary>💡 Indice</summary>C'est l'unité de base. La plupart du temps, 1 pod = 1 container.</details>
<details><summary>✅ Réponse</summary>L'unité de base de K8s. 1 pod ≈ 1 container. Kubernetes ne gère pas les containers directement — il gère des pods.</details>

**Q : Un pod crash, que fait Kubernetes ?**
<details><summary>💡 Indice</summary>K8s maintient le nombre de replicas défini dans le Deployment. Si un manque, il...</details>
<details><summary>✅ Réponse</summary>Le Deployment détecte qu'un pod manque et en recrée un automatiquement. C'est le self-healing. C'est pour ça qu'on ne crée jamais de pods directement — on passe par un Deployment.</details>

**Q : C'est quoi la différence entre port et targetPort dans un Service ?**
<details><summary>💡 Indice</summary>L'un est le port "d'entrée" du Service, l'autre est le port sur lequel le container écoute réellement. Ils peuvent être différents.</details>
<details><summary>✅ Réponse</summary><code>port</code> = le port pour accéder au Service (depuis l'intérieur du cluster). <code>targetPort</code> = le port du container vers lequel le traffic est redirigé. Souvent les mêmes, mais on pourrait mapper le port 80 du Service vers le port 8000 du container.</details>

**Q : Comment tu mets à jour une app sans downtime sur K8s ?**
<details><summary>💡 Indice</summary>K8s remplace les pods un par un, pas tous d'un coup. Il attend que le nouveau soit prêt avant de supprimer l'ancien. Comment ça s'appelle ?</details>
<details><summary>✅ Réponse</summary>Rolling update (le défaut). Kubernetes crée un nouveau pod avec la nouvelle version, attend qu'il soit prêt (health check), puis supprime l'ancien. Les pods sont remplacés un par un — les utilisateurs ne voient aucune coupure.</details>

**Q : Différence entre Docker et Kubernetes ?**
<details><summary>💡 Indice</summary>L'un fait tourner UN container, l'autre en orchestre des dizaines/centaines sur plusieurs machines.</details>
<details><summary>✅ Réponse</summary>Docker fait tourner UN container. Kubernetes orchestre des dizaines/centaines de containers sur plusieurs machines (scheduling, scaling, self-healing).</details>

**Q : C'est quoi un Deployment ?**
<details><summary>💡 Indice</summary>Tu ne crées jamais de pods directement. Tu passes par un objet qui les gère pour toi.</details>
<details><summary>✅ Réponse</summary>Un objet qui gère un groupe de pods identiques. Il maintient le nombre de replicas voulu, gère les updates (rolling update), et recrée les pods qui crashent.</details>

**Q : C'est quoi un Service K8s ?**
<details><summary>💡 Indice</summary>Les pods ont des IPs qui changent à chaque redémarrage. Il faut un point d'accès stable.</details>
<details><summary>✅ Réponse</summary>Un point d'accès réseau stable vers un groupe de pods. Les pods ont des IPs éphémères, le Service a une IP fixe et répartit le traffic entre les pods.</details>

**Q : C'est quoi un Namespace ?**
<details><summary>💡 Indice</summary>Pense à des dossiers pour organiser et isoler les ressources dans un cluster.</details>
<details><summary>✅ Réponse</summary>Un moyen d'isoler les ressources dans un cluster. Utile pour séparer les environnements (dev, staging, prod) ou les équipes.</details>

**Q : C'est quoi un Ingress ?**
<details><summary>💡 Indice</summary>Comment tu fais pour que les requêtes HTTP de l'extérieur arrivent aux bons Services dans le cluster ?</details>
<details><summary>✅ Réponse</summary>Un objet K8s qui gère le routage HTTP(S) vers les Services. Il permet de dire "les requêtes vers <code>api.monsite.com</code> vont vers le Service backend" et "les requêtes vers <code>monsite.com</code> vont vers le Service frontend". C'est le point d'entrée HTTP du cluster.</details>

**Q : C'est quoi un ConfigMap et un Secret ?**
<details><summary>💡 Indice</summary>Comment tu passes de la configuration et des secrets à tes pods sans les mettre dans l'image Docker ?</details>
<details><summary>✅ Réponse</summary>Des objets K8s pour stocker de la configuration. Un <strong>ConfigMap</strong> stocke des données non sensibles (URLs, feature flags). Un <strong>Secret</strong> stocke des données sensibles (mots de passe, clés API) encodées en base64. Les deux sont injectés dans les pods comme variables d'environnement ou fichiers.</details>

**Q : C'est quoi une liveness probe et une readiness probe ?**
<details><summary>💡 Indice</summary>K8s a besoin de savoir si tes pods sont vivants et prêts. Il utilise deux types de checks différents.</details>
<details><summary>✅ Réponse</summary>Des health checks que K8s exécute sur tes pods. La <strong>liveness probe</strong> vérifie que le pod est vivant — si elle échoue, K8s redémarre le pod. La <strong>readiness probe</strong> vérifie que le pod est prêt à recevoir du traffic — si elle échoue, K8s arrête de lui envoyer des requêtes sans le redémarrer.</details>

**Q : Différence entre ClusterIP, NodePort et LoadBalancer ?**
<details><summary>💡 Indice</summary>Ce sont les trois types de Service K8s. Chacun expose le Service à un niveau d'accessibilité différent.</details>
<details><summary>✅ Réponse</summary>Trois types de Service K8s. <strong>ClusterIP</strong> (défaut) = accessible uniquement depuis l'intérieur du cluster. <strong>NodePort</strong> = accessible depuis l'extérieur via un port sur chaque node. <strong>LoadBalancer</strong> = crée un load balancer externe (cloud provider) qui redirige vers le Service. En prod, on utilise généralement un Ingress devant un Service ClusterIP.</details>

## Monitoring

**Q : C'est quoi les 3 piliers de l'observabilité ?**
<details><summary>💡 Indice</summary>Trois types de données : des chiffres, du texte, et le parcours d'une requête.</details>
<details><summary>✅ Réponse</summary>Metrics (chiffres — CPU, temps de réponse), Logs (messages texte des applications), Traces (le parcours d'une requête à travers plusieurs services).</details>

**Q : Comment tu fais la différence entre un problème de code et un problème d'infra ?**
<details><summary>💡 Indice</summary>Si toutes les instances ont le même problème, c'est probablement le code. Si c'est une seule instance... pense aux ressources.</details>
<details><summary>✅ Réponse</summary>On vérifie les métriques d'infra d'abord (CPU, RAM, disque, réseau). Si tout est normal côté infra mais que l'app retourne des erreurs → c'est un bug dans le code (ticket pour les devs). Si le CPU est à 100% ou le disque est plein → c'est un problème d'infra (ton problème).</details>

**Q : Comment tu sais si ton app est lente ?**
<details><summary>💡 Indice</summary>On ne regarde pas la moyenne (elle cache les problèmes). On regarde un percentile — lequel ?</details>
<details><summary>✅ Réponse</summary>Le p95 ou p99 de la latency dans Grafana. Le p95 = 95% des requêtes sont plus rapides que cette valeur. Si le p95 est à 2 secondes, 5% de tes utilisateurs attendent plus de 2 secondes.</details>

**Q : C'est quoi une bonne alerte vs une mauvaise alerte ?**
<details><summary>💡 Indice</summary>Une bonne alerte te pousse à agir. Une mauvaise alerte, tu finis par l'ignorer. Pense symptômes vs causes.</details>
<details><summary>✅ Réponse</summary>Bonne : actionnable, basée sur les symptômes ("le taux d'erreur 5xx dépasse 5%"). Mauvaise : bruit ("CPU à 80%" — peut-être normal). Si tu reçois une alerte et que ta réaction c'est "bof", supprime l'alerte.</details>

**Q : C'est quoi la différence entre Prometheus et Grafana ?**
<details><summary>💡 Indice</summary>L'un collecte les données, l'autre les affiche. Pense capteur vs tableau de bord.</details>
<details><summary>✅ Réponse</summary>Prometheus collecte et stocke les métriques (il va scraper /metrics toutes les 15s). Grafana les affiche dans des dashboards. Prometheus = le capteur, Grafana = le tableau de bord.</details>

**Q : Pourquoi le monitoring est important ?**
<details><summary>💡 Indice</summary>Sans monitoring, comment tu sais que ton app fonctionne correctement ?</details>
<details><summary>✅ Réponse</summary>Sans monitoring, tu ne sais pas si ton app marche correctement. Tu détectes les problèmes avant les utilisateurs, tu identifies les goulots d'étranglement, et tu as des données pour prendre des décisions.</details>

**Q : C'est quoi Prometheus ?**
<details><summary>💡 Indice</summary>Un outil de collecte de métriques. Il va chercher les données lui-même (pull model) au lieu d'attendre qu'on les lui envoie.</details>
<details><summary>✅ Réponse</summary>Un système de collecte de métriques en pull model. Il scrape les endpoints <code>/metrics</code> des applications à intervalles réguliers et stocke les données en time series.</details>

**Q : C'est quoi Grafana ?**
<details><summary>💡 Indice</summary>C'est l'outil de visualisation qui va avec Prometheus. Pense tableaux de bord et graphiques.</details>
<details><summary>✅ Réponse</summary>Un outil de visualisation. Il se connecte à des sources de données (Prometheus, etc.) et crée des dashboards avec des graphiques et des alertes.</details>

**Q : Différence entre pull et push model ?**
<details><summary>💡 Indice</summary>Qui initie la collecte de données ? Le serveur de monitoring, ou l'application elle-même ?</details>
<details><summary>✅ Réponse</summary>Pull = Prometheus va chercher les données (scrape). Push = les applications envoient les données. Le pull est plus simple à gérer et à debugger.</details>

**Q : C'est quoi un SLI, SLO et SLA ?**
<details><summary>💡 Indice</summary>Trois niveaux : ce qu'on mesure, ce qu'on vise, ce qu'on s'engage contractuellement à respecter.</details>
<details><summary>✅ Réponse</summary><strong>SLI</strong> (Service Level Indicator) = la métrique mesurée (ex: 99.2% des requêtes répondent en moins de 200ms). <strong>SLO</strong> (Service Level Objective) = l'objectif interne (ex: on vise 99.5%). <strong>SLA</strong> (Service Level Agreement) = l'engagement contractuel avec le client (ex: si on passe sous 99%, on rembourse). SLI mesure, SLO guide, SLA engage.</details>

---

# Partie 2 : Mises en situation

## Scénario 1 — Déployer une app web en production

> **"Tu rejoins une startup. Ils ont une app web (frontend React + backend API + base PostgreSQL). Tout tourne sur le laptop du CTO. Comment tu mets ça en production ?"**

### Comment approcher la question

Ne plonge pas directement dans les outils. Pose des questions d'abord :
- Combien d'utilisateurs ? (10 ? 10 000 ? 1 million ?)
- Quel budget ? (0€ ? 50€/mois ? 1000€/mois ?)
- Quelle équipe ? (1 dev, 10 devs ? Y a-t-il un DevOps ?)
- Quels sont les besoins de disponibilité ? (side project vs. app bancaire)
- Le frontend est-il statique (juste du HTML/JS buildé) ou a-t-il besoin de server-side rendering ?

Cette dernière question est clé, parce qu'elle change complètement l'architecture pour le frontend.

### Le frontend — 3 approches différentes

**Notre cas : React avec Vite = frontend statique.** Le build produit des static files (HTML/CSS/JS) qu'on peut servir depuis n'importe quel serveur web ou CDN.

**Approche 1 — CDN / Hébergement statique (le plus simple et le plus performant)**

Le frontend buildé est juste des static files. Pas besoin d'un serveur pour ça.

| Service | Ce que c'est | Coût | Complexité |
|---------|-------------|------|-----------|
| **S3 + CloudFront** | Bucket S3 (stockage) + CDN AWS (distribution mondiale) | ~0-5$/mois | Faible |
| **Vercel** | Hébergement spécialisé frontend, deployment auto depuis Git | Gratuit (hobby) | Très faible |
| **Netlify** | Même concept que Vercel | Gratuit (hobby) | Très faible |
| **AWS Amplify Hosting** | Service AWS pour héberger des apps frontend, deployment auto depuis Git | Gratuit (Free Tier) | Faible |

**Quand choisir :** Quasi toujours pour un frontend statique (React, Vue, Angular buildé). C'est plus rapide (CDN = serveurs proches des utilisateurs), moins cher, et tu n'as aucun serveur à gérer.

**Approche 2 — Nginx dans un container** (ce qu'on fait dans le projet fil rouge)

On build le frontend, puis on sert les fichiers avec nginx dans un container Docker. C'est ce qu'on fait dans le Module 3.

**Quand choisir :** Quand tu veux tout avoir dans le même docker-compose pour simplifier le deployment, ou quand tu as besoin d'un reverse proxy custom (règles de routage complexes).

**Approche 3 — Server-Side Rendering (Next.js, Nuxt, etc.)**

Si le frontend fait du SSR (le HTML est généré côté serveur), alors il a besoin d'un serveur Node.js qui tourne en permanence. Dans ce cas, on le traite comme un backend (EC2, ECS, App Runner, etc.).

**Quand choisir :** SEO critique (e-commerce, blog), contenu dynamique qui change souvent.

### Le backend + base de données — Du plus simple au plus robuste

**Option A : 1 serveur, Docker Compose (MVP / side project)**

```
1 EC2 (t3.small)
├── Frontend (nginx)
├── Backend (API container)
└── PostgreSQL (container avec volume)
```

**Avantages :** Rapide à mettre en place, pas cher (~15$/mois), une seule machine.
**Inconvénients :** Single point of failure. DB dans Docker = risqué (pas de backup automatique). Scaling impossible.
**Quand choisir :** MVP, side project, <100 utilisateurs, budget ~0€.

**Option B : EC2 + RDS (startup sérieuse)**

```
VPC
├── Subnet public
│   └── EC2 (backend en Docker)
└── Subnet privé
    └── RDS PostgreSQL (backups automatiques)
+ S3 + CloudFront (frontend statique)
```

**Avantages :** La DB est managée (backups, updates auto). Séparation réseau. Le frontend sur CDN est rapide et gratuit. On peut ajouter un 2ème EC2 + load balancer plus tard.
**Inconvénients :** Plus cher (~50-100$/mois). Tu gères les EC2 toi-même (updates OS, Docker, etc.).
**Quand choisir :** App en prod, vrais utilisateurs, besoin de fiabilité, équipe petite.

**Option C : ECS Fargate (scaling sans gérer de serveurs)**

```
VPC
├── Subnet public
│   └── Application Load Balancer
├── Subnet privé
│   ├── ECS Fargate (containers backend, auto-scaling)
│   └── RDS PostgreSQL Multi-AZ
+ S3 + CloudFront (frontend)
+ Route 53 (DNS)
```

ECS (Elastic Container Service) fait tourner tes containers Docker sans que tu gères de serveurs. Fargate = tu lui donnes une image Docker, tu définis CPU/RAM, il lance le container quelque part dans le cloud. Tu ne vois jamais de machine.

**Avantages :** Auto-scaling, pas de serveurs à gérer, high availability. Tu pousses une image Docker et c'est déployé.
**Inconvénients :** Plus cher que EC2 brut (~100-300$/mois). Configuration plus complexe (task definitions, services, target groups...).
**Quand choisir :** Traffic variable, besoin de scaling, pas envie de gérer des EC2.

**Option D : AWS App Runner (le plus simple pour des containers)**

```
App Runner (backend container)
+ RDS PostgreSQL
+ S3 + CloudFront (frontend)
```

App Runner est le service le plus simple d'AWS pour faire tourner un container web. Tu lui donnes ton image Docker (ou ton code source) et il gère tout : build, deployment, scaling, HTTPS, load balancing.

**Avantages :** Ultra simple. Aucune configuration réseau. Auto-scaling inclus. HTTPS automatique.
**Inconvénients :** Moins de contrôle que ECS. Pas de VPC par défaut (configurable). Plus cher à fort traffic.
**Quand choisir :** Tu veux déployer vite, tu ne veux pas configurer VPC/ALB/ECS, équipe petite sans DevOps dédié.

**Option E : AWS Amplify (frontend + backend intégré)**

Amplify est une plateforme complète qui peut héberger un frontend statique ET un backend (via des fonctions Lambda ou un API GraphQL).

**Avantages :** Tout-en-un : hébergement, auth, API, base de données. Déploiement auto depuis Git. Idéal pour les devs fullstack qui ne veulent pas toucher à l'infra.
**Inconvénients :** Vendor lock-in fort (tu es lié à la façon de faire Amplify). Moins de contrôle. Peut devenir limitant pour des architectures complexes.
**Quand choisir :** Petit projet fullstack, prototypage rapide, pas de DevOps dans l'équipe.

**Option F : Kubernetes / EKS (grosse échelle)**

```
EKS (Kubernetes managé)
├── Deployments backend (auto-scaling)
├── Deployments workers
├── Ingress Controller (routage HTTP)
+ RDS Multi-AZ
+ S3 + CloudFront (frontend)
+ Helm pour le packaging
```

**Avantages :** Scaling massif, portabilité (pas locked à AWS), orchestration fine.
**Inconvénients :** Complexe à opérer. EKS coûte ~75$/mois rien que pour le control plane. Over-engineering si tu n'as pas 10+ microservices.
**Quand choisir :** Beaucoup de microservices, grosse équipe DevOps, besoin de portabilité multi-cloud.

### Le tableau comparatif global

| Option | Complexité | Coût mensuel* | Scaling | Gestion serveur | Cas d'usage |
|--------|-----------|--------------|---------|----------------|-------------|
| **EC2 + Docker Compose** | Faible | ~15$ | Non | Oui | MVP |
| **EC2 + RDS** | Moyenne | ~50-100$ | Manuel | Oui | Startup sérieuse |
| **App Runner + RDS** | Faible | ~30-80$ | Auto | Non | Petite équipe, vite en prod |
| **ECS Fargate + RDS** | Élevée | ~100-300$ | Auto | Non | Traffic variable, scaling |
| **Amplify** | Faible | ~0-50$ | Auto | Non | Prototypage, fullstack solo |
| **EKS (K8s)** | Très élevée | ~200+$ | Auto | Partiellement | Microservices, grosse échelle |

*Coûts approximatifs pour une app de taille modeste.

### Hors AWS — les alternatives

| Service | Ce que c'est | Quand l'utiliser |
|---------|-------------|-----------------|
| **Railway / Render** | PaaS (Platform as a Service). Tu push ton code, ils déploient. | Side projects, petites apps, pas envie de toucher à AWS |
| **Fly.io** | Containers à la edge (proches des utilisateurs). | API globales, low latency |
| **DigitalOcean App Platform** | PaaS simple, moins cher qu'AWS. | PME, startups qui veulent du simple |
| **GCP Cloud Run** | Équivalent Google de App Runner. Containers serverless. | Déjà sur GCP |
| **Azure Container Apps** | Équivalent Microsoft de App Runner. | Déjà sur Azure |

En entretien, mentionner que des alternatives existent montre que tu ne connais pas qu'un seul fournisseur.

### Ce que le recruteur attend

Pas la réponse parfaite. Il veut voir que tu :
- **Poses des questions** avant de répondre (budget, scale, contraintes, équipe)
- **Connais plusieurs options** et sais les comparer (pas juste "EC2 et c'est tout")
- **Sépares les préoccupations** : le frontend statique n'a pas besoin d'un serveur, la DB doit être managée
- **Sais expliquer les trade-offs** : simplicité vs. contrôle vs. coût vs. scaling
- **Ne proposes pas Kubernetes pour 50 utilisateurs** — mais tu sais expliquer quand K8s fait sens

---

## Scénario 2 — Le site est down en prod

> **"Il est 14h, tu reçois une alerte : le site ne répond plus. Les utilisateurs se plaignent. Qu'est-ce que tu fais ?"**

### La méthode (du plus large au plus précis)

**Étape 1 — Confirmer et délimiter le problème (30 secondes)**
```bash
# Le site répond ?
curl -I https://monsite.com
# Si timeout → problème réseau/DNS/serveur down
# Si 502 → le serveur proxy tourne mais l'app derrière est down
# Si 500 → l'app tourne mais crashe

# C'est juste moi ou tout le monde ?
# Tester depuis un autre réseau / un collègue
```

**Étape 2 — Vérifier l'infra (2 minutes)**
```bash
# Le serveur est up ?
ssh user@serveur
# Si "Connection refused" → le serveur est down ou le port SSH est bloqué
# → Vérifier sur la console AWS : instance running ? Security Group OK ?

# Les ressources sont OK ?
top              # CPU, RAM
df -h            # Disque plein ?
```

**Étape 3 — Vérifier les services (2 minutes)**
```bash
docker ps                        # Les containers tournent ?
docker logs backend --tail 100   # Erreurs récentes ?
systemctl status nginx           # Le reverse proxy tourne ?
```

**Étape 4 — Vérifier les dépendances**
```bash
# La base de données répond ?
docker exec -it db psql -U user -c "SELECT 1;"

# Les services externes répondent ?
curl https://api-externe-quon-utilise.com/health
```

**Étape 5 — Corriger et communiquer**
- Corriger le problème (redémarrer le service, libérer du disque, rollback du dernier deployment...)
- **Communiquer** : prévenir l'équipe, mettre à jour le status page
- Après l'incident : écrire un post-mortem (qu'est-ce qui s'est passé, pourquoi, comment éviter que ça se reproduise)

### Les causes les plus fréquentes

| Symptôme | Cause probable | Fix rapide |
|----------|---------------|-----------|
| Timeout total | Serveur down ou Security Group | Redémarrer l'instance, vérifier les règles réseau |
| 502 Bad Gateway | L'app a crashé derrière le proxy | `docker restart backend`, vérifier les logs |
| 500 Internal Error | Bug dans le code ou DB inaccessible | Logs de l'app, vérifier la connexion DB |
| Site très lent | CPU/RAM saturé, requêtes DB lentes | `top`, vérifier les slow queries |
| Disque plein | Logs qui s'accumulent, images Docker | `df -h`, `docker system prune`, rotation des logs |

### Ce que le recruteur attend

- Une méthode structurée, pas du panique
- Tu commences par vérifier, pas par modifier
- Tu communiques avec l'équipe pendant le debugging
- Tu parles de post-mortem (apprentissage après l'incident)

---

## Scénario 3 — Mettre en place un pipeline CI/CD

> **"L'équipe de 5 devs déploie manuellement en SSH. Ça prend 30 min et ça casse une fois sur trois. Comment tu améliores ça ?"**

### Le problème concret

Aujourd'hui :
1. Un dev finit son code
2. Il se connecte en SSH au serveur
3. Il fait `git pull` sur le serveur
4. Il relance l'app manuellement
5. Il croise les doigts

Problèmes : aucun test avant deployment, pas de rollback possible, un seul dev sait faire la manip, ça casse souvent.

### La solution progressive

**Phase 1 — CI (1-2 jours à mettre en place)**
```yaml
# À chaque push sur main :
Lint → Tests → Build image Docker → Push sur registry
```
- Les devs ont un feedback immédiat : "ton code casse les tests"
- On ne déploie jamais du code qui ne compile pas ou qui ne passe pas les tests
- **Impact :** on arrête de déployer du code cassé

**Phase 2 — CD vers un environnement de staging (3-5 jours)**
```yaml
# Après le CI :
Deploy automatique sur un serveur de staging
```
- Les devs et le product owner testent sur staging avant la prod
- Staging est une copie de la prod (même config, même infra)
- **Impact :** on teste dans des conditions réelles avant la prod

**Phase 3 — CD vers la prod (quand l'équipe est confiante)**
```yaml
# Si staging est OK (tests passent, QA validée) :
Approbation manuelle → Deploy en prod
```
- Un humain valide avant la prod (Continuous Delivery, pas Deployment)
- Rollback automatique si le health check échoue
- **Impact :** deployment en 5 min au lieu de 30, aucune connexion SSH

### Pourquoi pas tout automatiser d'un coup ?

Parce que la confiance se construit progressivement. Si les tests ne couvrent pas assez de cas, un deployment 100% automatique en prod va déployer des bugs plus vite. Phase 1 → Phase 2 → Phase 3 permet à l'équipe de gagner confiance à chaque étape.

### Ce que le recruteur attend

- Tu ne proposes pas "on met Kubernetes" d'emblée
- Tu penses progressif (quick wins d'abord)
- Tu parles de staging (jamais directement en prod)
- Tu mentionnes le rollback

---

## Scénario 4 — Gérer les secrets

> **"Un dev a committé un mot de passe de base de données dans le repo Git. Qu'est-ce que tu fais ?"**

### Réaction immédiate (urgence)

1. **Changer le mot de passe immédiatement** — la priorité absolue. Même si "personne ne l'a vu", on considère qu'il est compromis.
2. **Vérifier l'accès** — quelqu'un a-t-il utilisé ce mot de passe depuis le commit ?
3. **Supprimer du Git** — attention, un simple `git rm` ne suffit PAS. Le mot de passe reste dans l'historique. Il faut réécrire l'historique (`git filter-branch` ou `bfg`), mais c'est lourd. Le plus important reste le point 1 : changer le mot de passe.

### Mettre en place des protections

| Mesure | Ce que ça fait |
|--------|---------------|
| **`.gitignore`** | Ignorer les fichiers `.env`, `credentials.json`, etc. |
| **Pre-commit hook** | Scanner les commits AVANT qu'ils soient poussés (outils : `gitleaks`, `detect-secrets`) |
| **GitHub Secret Scanning** | GitHub détecte automatiquement les secrets committés et te prévient |
| **Variables d'environnement** | Les secrets vivent dans l'env du serveur, pas dans le code |
| **Secrets manager** | AWS Secrets Manager, HashiCorp Vault — stockage sécurisé et centralisé |

### La règle

Le code est **public par défaut** (même un repo privé peut fuiter). Les secrets ne doivent **jamais** être dans le code. Point.

---

## Scénario 5 — Choisir la bonne infra pour chaque projet

> **"On a 4 projets à héberger. Comment tu choisis l'infra pour chacun ?"**

### Projet A : API REST interne avec 1000 requêtes/jour

**Contexte :** API utilisée par une app mobile interne. Peu de traffic, budget minimal, une seule personne pour maintenir.

**Meilleur choix : Lambda + API Gateway**

Pourquoi : très peu de traffic, pas besoin d'un serveur qui tourne 24/7. Lambda = tu paies uniquement quand une requête arrive. Coût : quasi 0€ (Free Tier). API Gateway gère le HTTPS, le rate limiting, et le routage.

**Alternatives possibles :**
- **App Runner** : si l'API est containerisée et que tu veux quelque chose de simple sans devoir adapter le code pour Lambda. Un poil plus cher mais zéro adaptation du code.
- **EC2** : over-kill. Tu paies un serveur 24/7 pour 1000 requêtes/jour, c'est du gaspillage.

### Projet B : SaaS web avec 10 000 utilisateurs/jour

**Contexte :** Application web (React + API + PostgreSQL). Traffic régulier en journée, peu la nuit. Équipe de 5 devs. Besoin de fiabilité.

**Meilleur choix : ECS Fargate + RDS + S3/CloudFront**

```
CloudFront (CDN) → S3 (frontend statique)
ALB → ECS Fargate (API containers, auto-scaling)
       └── RDS PostgreSQL (subnet privé)
```

Pourquoi : traffic régulier, l'app doit tourner en permanence, connexion persistante à la DB. ECS Fargate = pas de serveurs à gérer, auto-scaling pour gérer les pics. RDS = DB managée.

**Alternatives possibles :**
- **EC2 + RDS** : moins cher, mais tu gères les serveurs (updates, Docker, monitoring). Bon choix si le budget est serré et que quelqu'un dans l'équipe sait gérer des serveurs.
- **App Runner + RDS** : plus simple que ECS, mais moins de contrôle sur le réseau (VPC peering, security groups custom). Bon pour une v1 rapide.
- **Lambda** : possible techniquement, mais les cold starts dégradent l'expérience utilisateur, et les connexions DB sont compliquées à gérer (il faut RDS Proxy).

### Projet C : Traitement de fichiers uploadés (redimensionner des images)

**Contexte :** Les utilisateurs uploadent des photos. On doit les redimensionner en 3 tailles et les stocker. Volume variable : parfois 10 uploads/jour, parfois 10 000.

**Meilleur choix : Lambda + S3 (architecture événementielle)**

```
Utilisateur → upload → S3 bucket (originaux)
                         │
                         └── trigger Lambda → resize → S3 bucket (résultats)
```

Pourquoi : événementiel pur. Un fichier arrive dans S3 → Lambda se déclenche automatiquement → traite le fichier → remet le résultat dans S3. Pas besoin de serveur entre les uploads. Scaling automatique (100 uploads en même temps → 100 Lambdas en parallèle).

**Alternatives possibles :**
- **ECS avec une queue SQS** : si le traitement dure >15 min (limite de Lambda) ou nécessite beaucoup de mémoire (>10 Go). SQS = file d'attente, ECS = workers qui consomment la file.
- **Step Functions + Lambda** : si le traitement a plusieurs étapes (resize → watermark → optimise → notify). Step Functions orchestre les Lambdas.

### Projet D : Site vitrine / blog d'entreprise

**Contexte :** Site marketing avec du contenu statique. Pas de backend custom, juste du contenu qui change rarement. Budget quasi nul.

**Meilleur choix : Amplify Hosting (ou Vercel / Netlify)**

Pourquoi : c'est du contenu statique. Aucun besoin de serveur, de container, ou de quoi que ce soit de complexe. Tu push sur Git, le site est déployé automatiquement sur un CDN mondial.

```
Git push → Amplify Hosting → CDN mondial → utilisateurs
```

Coût : gratuit (Free Tier Amplify, ou plan gratuit Vercel/Netlify).

**Alternatives possibles :**
- **S3 + CloudFront** : même résultat, configuration manuelle. Mieux si tu veux tout contrôler côté AWS.
- **EC2 avec nginx** : over-kill absolu. Un serveur 24/7 pour servir des fichiers HTML, c'est du gaspillage d'argent et de temps.

### Le tableau de décision

| Critère | Lambda | App Runner | ECS Fargate | EC2 | Amplify / Vercel |
|---------|--------|-----------|-------------|-----|-----------------|
| Traffic | Sporadique | Constant faible | Variable / fort | Constant | Statique |
| Durée d'exécution | < 15 min | Illimitée | Illimitée | Illimitée | N/A |
| Stateful | Non | Non | Oui | Oui | Non |
| Connexion DB | Compliqué | Facile | Facile | Facile | Non (ou via API) |
| Scaling | Auto, instantané | Auto | Auto (configurable) | Manuel / ASG | Auto (CDN) |
| Gestion serveur | Aucune | Aucune | Aucune | Toi | Aucune |
| Coût faible traffic | ~0€ | ~5-15$/mois | ~20-50$/mois | ~15-30$/mois | ~0€ |
| Coût fort traffic | Peut exploser | Moyen | Prévisible | Prévisible | Faible (CDN) |
| Complexité config | Faible | Très faible | Élevée | Moyenne | Très faible |

### Ce que le recruteur attend

- Tu ne donnes pas la même réponse pour les 4 projets
- Tu justifies par des critères concrets (traffic, durée, coût, état, équipe)
- Tu connais les limites de chaque solution ET les alternatives
- Tu sais que "le meilleur choix" dépend du contexte — il n'y a pas de réponse universelle
- Tu sépares frontend statique / backend / traitements async : chacun a une solution différente

---

## Scénario 6 — Infrastructure as Code : un collègue a modifié l'infra à la main

> **"Ton équipe utilise Terraform. Tu fais `terraform plan` et tu vois des changements que personne n'a fait dans le code. Que se passe-t-il et comment tu gères ?"**

### Ce qui s'est passé

Quelqu'un a modifié l'infra directement dans la console AWS (ajouté un Security Group rule, changé une instance type, etc.) sans passer par Terraform. Le state file de Terraform ne correspond plus à la réalité.

C'est ce qu'on appelle du **drift** (dérive).

### Comment résoudre

**Option A — Importer le changement dans Terraform (si le changement est voulu)**
```bash
# 1. Identifier ce qui a changé
terraform plan
# ~ aws_security_group.web will be updated in-place
#   - ingress rule for port 3306 (added manually)

# 2. Ajouter la règle dans le code Terraform pour qu'elle corresponde à la réalité
# 3. Re-plan → pas de changement → le code et la réalité sont synchronisés
terraform plan
# No changes.
```

**Option B — Forcer le retour au code (si le changement est une erreur)**
```bash
# terraform apply va remettre l'infra dans l'état décrit par le code
terraform apply
# Le changement manuel sera écrasé
```

### Prévenir le problème

- **Règle d'équipe :** on ne touche JAMAIS à la console pour modifier l'infra. Tout passe par le code + pull request.
- **IAM restrictif :** limiter les permissions de modification en console pour les environnements de prod.
- **Drift detection :** lancer `terraform plan` régulièrement (en CI) pour détecter les dérives.

---

## Scénario 7 — Monitoring et alerting

> **"Ton app tourne en prod depuis 3 mois. Le CTO te dit : 'On a des utilisateurs qui se plaignent que c'est lent mais on ne sait pas pourquoi.' Comment tu mets en place du monitoring ?"**

### Étape 1 — Définir ce qu'on veut mesurer

Les 4 signaux dorés (les "Golden Signals" de Google SRE) :

| Signal | Question | Exemple de métrique |
|--------|----------|-------------------|
| **Latency** | C'est rapide ? | Temps de réponse au 95e percentile |
| **Traffic** | Combien de monde ? | Requêtes par seconde |
| **Errors** | Ça marche ? | Taux d'errors 5xx |
| **Saturation** | C'est plein ? | CPU, RAM, disque, connexions DB |

### Étape 2 — Instrumenter l'app

```
App → expose /metrics → Prometheus scrape → Grafana affiche
```

- Ajouter la librairie Prometheus à l'app (pour notre projet : `prometheus-fastapi-instrumentator`)
- Déployer Prometheus + Grafana (docker-compose, c'est le plus simple)

### Étape 3 — Créer les dashboards

Un dashboard par "audience" :
- **Dashboard technique :** latency, errors, CPU, RAM, slow queries DB
- **Dashboard business :** nombre d'utilisateurs actifs, nombre de tâches créées (pour le CTO)

### Étape 4 — Configurer les alertes

Bonnes alertes :
- "Le error rate 5xx dépasse 5% depuis 5 minutes" → **actionnable** (il y a un bug ou un service down)
- "Le response time p95 dépasse 2 secondes depuis 10 minutes" → **actionnable** (performance dégradée)

Mauvaises alertes :
- "CPU à 80%" → **pas actionnable seul** (80% de CPU c'est peut-être normal si l'app tourne bien)
- "1 erreur 404" → **bruit** (un utilisateur a tapé une mauvaise URL, c'est normal)

### Ce que le recruteur attend

- Tu connais les Golden Signals ou un framework similaire
- Tu distingues métriques techniques et business
- Tu sais qu'une alerte doit être actionnable
- Tu ne proposes pas de monitorer 200 métriques d'un coup

---

## Scénario 8 — Blue-green / Canary deployment

> **"Comment tu déploies en prod sans downtime et sans risquer de casser pour tous les utilisateurs ?"**

### Option A — Blue-Green

```
                    ┌─── Blue (v1.0 — actuelle) ◄── 100% du traffic
Load Balancer ──────┤
                    └─── Green (v1.1 — nouvelle) ◄── 0% du traffic
```

1. Tu déploies la v1.1 sur le Green (pendant que Blue sert toujours les users)
2. Tu testes Green (smoke tests, sanity check)
3. Tu bascules le load balancer : Green reçoit 100% du traffic
4. Si ça marche → tu supprimes Blue. Si ça casse → tu rebascules sur Blue en 10 secondes.

**Avantages :** Rollback instantané. Zéro downtime.
**Inconvénients :** Double infra pendant la transition (coût). Problème si la DB a changé de schéma entre v1.0 et v1.1.

### Option B — Canary

```
                    ┌─── v1.0 ◄── 95% du traffic
Load Balancer ──────┤
                    └─── v1.1 ◄── 5% du traffic (les "canaris")
```

1. Tu déploies la v1.1 sur quelques instances
2. Tu envoies 5% du traffic vers la v1.1
3. Tu surveilles les métriques (errors, latency)
4. Si tout va bien → 25% → 50% → 100%. Si ça casse → 0% et rollback.

**Avantages :** Tu détectes les bugs avec un impact limité (5% des utilisateurs).
**Inconvénients :** Plus complexe à mettre en place. Nécessite un bon monitoring pour détecter les problèmes.

### Option C — Rolling Update

C'est ce que fait Kubernetes par défaut. On remplace les instances une par une :

```
Début:    [v1.0] [v1.0] [v1.0] [v1.0]
Étape 1:  [v1.1] [v1.0] [v1.0] [v1.0]
Étape 2:  [v1.1] [v1.1] [v1.0] [v1.0]
Étape 3:  [v1.1] [v1.1] [v1.1] [v1.0]
Fin:      [v1.1] [v1.1] [v1.1] [v1.1]
```

**Avantages :** Simple, natif dans K8s, pas de double infra.
**Inconvénients :** Rollback plus lent. Pendant la transition, deux versions coexistent.

### Lequel choisir ?

| Stratégie | Complexité | Rollback | Cas d'usage |
|-----------|-----------|----------|-------------|
| **Blue-Green** | Moyenne | Instantané | Apps critiques, peu de deployments |
| **Canary** | Élevée | Rapide | Apps à fort traffic, besoin de tester en conditions réelles |
| **Rolling** | Faible | Moyen | La plupart des cas, défaut K8s |
