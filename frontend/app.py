import streamlit as st
from utils import get_recommendations, get_movie, fetch_genre_distribution, fetch_stats
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Recommandations de Films", layout="wide")
st.title("🎬 Système de Recommandation de Films")

# Création des onglets
tab1, tab2, tab3 = st.tabs(["🔍 Recommandations", "📊 Statistiques", "📈 Statistiques dynamiques"])

# Onglet 1 : Recommandations
with tab1:
    st.header("Obtenez des recommandations personnalisées")
    user_id = st.number_input("Entrez votre ID utilisateur", min_value=1, step=1)
    top_n = st.slider("Nombre de recommandations", 1, 20, 5)

    if st.button("Recommander"):
        with st.spinner("Chargement des recommandations..."):
            try:
                recos = get_recommendations(user_id, top_n)
                if recos:
                    df = pd.DataFrame(recos)
                    st.success(f"{len(df)} recommandations pour l'utilisateur {user_id}")
                    st.dataframe(df[['title', 'genres', 'release_date', 'predicted_rating']])
                else:
                    st.warning("Aucune recommandation disponible.")
            except Exception as e:
                st.error(f"Erreur lors du chargement des recommandations : {e}")

# Onglet 2 : Statistiques
with tab2:
    st.header("Statistiques sur les films")
    st.subheader("📈 Exemple fictif de distribution des notes")

    # Exemple fictif de distribution
    data = {
        "note": [1, 2, 3, 4, 5],
        "nombre de films": [100, 250, 500, 300, 200]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x="note", y="nombre de films", title="Distribution des notes moyennes")
    st.plotly_chart(fig)

    st.subheader("🎭 Distribution des genres")
    if st.button("Afficher la distribution des genres"):
        with st.spinner("Chargement de la distribution des genres..."):
            try:
                genre_data = fetch_genre_distribution()
                if genre_data:
                    df_genres = pd.DataFrame(genre_data)

                    # Diagramme circulaire
                    st.plotly_chart(
                        px.pie(df_genres, names='genre', values='count',
                               title='Répartition des genres dans la base de films')
                    )

                    # Diagramme en barres
                    st.plotly_chart(
                        px.bar(df_genres.head(15), x='genre', y='count',
                               title='Top 15 genres les plus fréquents',
                               labels={'count': 'Nombre de films'})
                    )
                else:
                    st.warning("Aucune donnée de genre trouvée.")
            except Exception as e:
                st.error(f"Erreur lors du chargement des genres : {e}")

# Onglet 3 : Statistiques dynamiques
with tab3:
    st.header("📊 Statistiques dynamiques")
    col1, col2 = st.columns(2)

    with col1:
        genre_input = st.text_input("Filtrer par genre (ex: 12, 14, 16, 18, 27, 28, 35, 36, 37 ...)")
    with col2:
        year_input = st.number_input("Filtrer par année", min_value=1900, max_value=2025, step=1, value=2025)

    if st.button("Afficher les statistiques"):
        with st.spinner("Chargement des statistiques..."):
            try:
                year_val = int(year_input) if year_input > 0 else None
                stats = fetch_stats(genre_input or None, year_val)
                if stats:
                    df_stats = pd.DataFrame(stats)
                    st.dataframe(df_stats[['title', 'genres', 'release_date', 'average_rating', 'num_ratings']])

                    st.plotly_chart(
                        px.bar(df_stats, x="title", y="average_rating",
                               title="Top 20 films par note moyenne",
                               labels={'average_rating': 'Note moyenne', 'title': 'Titre de film'},
                               height=500)
                    )
                else:
                    st.warning("Aucune donnée trouvée avec ces filtres.")
            except Exception as e:
                st.error(f"Erreur lors du chargement des statistiques : {e}")
