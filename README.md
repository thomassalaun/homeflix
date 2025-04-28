# Projet : Système de Recommandation de Films

Ce projet implémente un système complet de recommandation de films utilisant des modèles de filtrage collaboratif. Il inclut un backend à l'aide de FastAPI, une base de données gérée avec DuckDB, et une interface utilisateur interactive construite avec Streamlit.

## Fonctionnalités Principales

### 1. Backend avec FastAPI
- **Recommandations personnalisées** : Génération de recommandations basées sur l'historique d'évaluations d'un utilisateur.
- **Statistiques dynamiques** : Analyse des films en fonction de genres, années ou autres filtres.
- **Santé de l'API** : Endpoint pour vérifier la disponibilité de l'API.

### 2. Gestion de la base de données avec DuckDB
- **Chargement des données** : Importation des évaluations et des métadonnées des films depuis des fichiers CSV. Les fichiers csv sont issus de Kaggle ou de TMDB.
- **Exportation** : Sauvegarde de la base de données au format CSV pour des besoins d'analyse supplémentaires.
- **Gestion des genres** : Extraction et transformation des données sur les genres des films.

### 3. Interface utilisateur avec Streamlit
- **Recommandations dynamiques** : Interface interactive pour demander et afficher les recommandations.
- **Visualisation de données** : Graphiques interactifs (barres, diagrammes circulaires) pour analyser les genres et les évaluations.
- **Filtres avancés** : Filtrage des statistiques par genre et année de sortie.

---

## Prérequis

Assurez-vous que les outils suivants sont installés sur votre machine :

- **Python 3.9 ou ultérieur**
- **Pip**
- **Docker** (optionnel, pour l’exécution dans un conteneur)

---

## Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/projet-recommendation-films.git
   cd projet-recommendation-films
   ```

2. **Lancer le docker compose**
   ```bash
   docker compose up --build
   ```

---

## Utilisation

### 1. Démarrer l’API FastAPI

```bash
uvicorn main:app --reload
```
L'API sera accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Utiliser l’interface utilisateur Streamlit

Dans un terminal distinct :
```bash
streamlit run app.py
```
Accédez à l'interface utilisateur via [http://localhost:8501](http://localhost:8501).

---

## Points Clés du Code

### 1. RecommenderChunkSystem
Le système de recommandation utilise la bibliothèque **Surprise** pour construire un modèle SVD (Singular Value Decomposition) basé sur les évaluations utilisateur.

### 2. API Endpoints
- **/movie/{movie_id}** : Récupérer les informations d’un film.
- **/recommendations/{user_id}** : Obtenir des recommandations pour un utilisateur.
- **/statistics/{genre}/{year}** : Filtrer les statistiques par genre et année.
- **/genres/distribution** : Obtenir la distribution des genres.

### 3. Visualisations Streamlit
Les graphiques interactifs sont créés avec **Plotly Express** pour un rendu dynamique et intuitif.

---

## Auteurs

Thomas SALAÜN @thomassalaun
Théo JUGEAU @the0jug0
Sofia-Maitri BUDE @sofia-maitri

