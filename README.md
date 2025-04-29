# Projet : Système de Recommandation de Films

Ce projet implémente un système complet de recommandation de films utilisant des modèles de filtrage collaboratif.\
Il inclut un backend à l'aide de FastAPI, une base de données gérée avec DuckDB, et une interface utilisateur interactive construite avec Streamlit.

## Fonctionnalités Principales

### 1. Backend avec FastAPI
- **Recommandations personnalisées** : Génération de recommandations basées sur l'historique d'évaluations d'un utilisateur.
- **Statistiques dynamiques** : Analyse des films en fonction de genres, années ou autres filtres.
- **Santé de l'API** : Endpoint pour vérifier la disponibilité de l'API.

### 2. Gestion de la base de données avec DuckDB
- **Chargement des données** : Importation des évaluations et des métadonnées des films depuis des fichiers CSV. Les fichiers csv sont issus de Kaggle / TMDB.
- **Exportation** : Sauvegarde de la base de données au format CSV pour des besoins d'analyse supplémentaires. Et génération des scripts SQL pour la création des tables et leur chargement.
- **Gestion des genres** : Extraction et transformation des données sur les genres des films.

### 3. Interface utilisateur avec Streamlit
- **Recommandations dynamiques** : Interface interactive pour demander et afficher les recommandations.
- **Visualisation de données** : Graphiques interactifs (barres, diagrammes circulaires) pour analyser les genres et les évaluations.
- **Filtres avancés** : Filtrage des statistiques par genre et année de sortie.

---

## Prérequis

Assurez-vous que Docker soit installé sur votre machine :
- **Version de docker compose 2.30 minimum** 

---

## Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/thomassalaun/homeflix.git
   cd homeflix
   ```
2. **Préparation du jeux de données**

   Les conteneurs vont utiliser un volume mappé sur un répertoire de la machine hôte.\
   Dans ce répertoire, nous copierons les fichier csv. A l'issue du démarrage des conteneurs, nous trouverons dans ce répertoire:
   - la base de données DuckDB
   - un sous répertoire nommé **export** contenant le dump de la base de données, les scripts de création et de chargement des tables.

   Sous linux:
   ```bash
      mkdir /tmp/mon_repertoire
      cp data/*.csv /tmp/mon_repertoire
   ```
4. **Préparation du fichier d'environnement**   
   Docker va utiliser ce fichier pour interpoler le contenu de la variable MOUNT_MOINT dans le fichier docker-compose.yml .\
   Créer un fichier demo.env dans le répertoire courant contenant :
    MOUNT_POINT=/tmp/mon_repertoire

---

## Fonctionnement & utilisation

### 1. Fonctionnement

Dans le répertoire du projet homeflix, lancez la commande suivante :
```bash
docker compose --env-file ./demo.env up 
```

Docker va tout d'abord démarrer le conteneur **homeflix-db** qui est en charge de créer la base de données DuckDB, les tables, et charger les données depuis les fichiers csv.\
Ensuite, Docker démarrera le service homeflix-backend lorsque le conteneur **homeflix-db** aura terminé sa tâche.\
Et enfin, Docker démarrera le service homeflix-frontend lorsque le conteneur **homeflix-backend** répondra sur l'api /healthy .

### 2. Utiliser l’interface utilisateur Streamlit
Dans un navigateur ,accédez à l'interface via [http://localhost:8081](http://localhost:8081).

---

## Points Clés du Code

### 1. Généralités
Dans le répertoire data: les données csv.\

Dans le répertoire database: les scripts permettant de créer la base de données, charger et exporter les données.\

Dans le répertoire backend: les scripts pour interroger la base de données, et exposer des apis pour le service frontend.\

Dans le répertoire frontend: les scripts pour l'interface homme machine.

Dans le répertoire Dockerfiles: Les fichiers dockerfile pour créer les images des 3 services cités ci-dessus.

Dans le répertoire racine, le fichier docker-compose qui crée , ochestre les différents services, crée le volume et le réseau pour le fonctionnement des différents services.

Les fichiers **requirements*.txt* ont été freezés afin d'installer les versions spécifiques des packages, et non les dernières versions qui pourraient apparaitre et ne plus faire fonctionner le projet.

### 2. RecommenderChunkSystem
Le système de recommandation utilise la bibliothèque **Surprise** pour construire un modèle SVD (Singular Value Decomposition) basé sur les évaluations utilisateur.

### 3. API Endpoints
- **/movie/{movie_id}** : Récupérer les informations d’un film.
- **/recommendations/{user_id}** : Obtenir des recommandations pour un utilisateur.
- **/statistics/{genre}/{year}** : Filtrer les statistiques par genre et année.
- **/genres/distribution** : Obtenir la distribution des genres.

### 4. Visualisations Streamlit
Les graphiques interactifs sont créés avec **Plotly Express** pour un rendu dynamique et intuitif.

---

## Auteurs

Thomas SALAÜN @thomassalaun

Théo JUGEAU @the0jug0

Sofia-Maitri BUDE @sofia-maitri

