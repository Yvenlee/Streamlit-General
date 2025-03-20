import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Énergies Renouvelables vs Fossiles", page_icon="⚡", layout="wide")


# Charger les données avec mise en cache
@st.cache_data
def load_data():
    df = pd.read_csv('datasets/World Energy Consumption.csv')
    return df

df = load_data()

# Interface utilisateur avec une barre latérale
st.sidebar.title("Navigation")
st.sidebar.subheader("Sélectionnez l'année et la plage")
year_range = st.sidebar.slider("📅 Sélectionnez une plage d'années :", 1995, 2020, (2000, 2020))
year_selected = st.sidebar.slider("📅 Sélectionnez une année pour la carte et les camemberts :", 1995, 2020, 2020)

# Titre principal
st.title("⚡ Énergies Renouvelables vs Fossiles")
st.markdown("L'évolution de la part des énergies renouvelables et fossiles dans le monde de 1995 à 2020")

# 📌 Filtrer les données en fonction de la plage d'années sélectionnée
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
df_renewables = df_filtered.groupby('year')['renewables_share_elec'].mean()
df_fossil = df_filtered.groupby('year')['fossil_share_elec'].mean()

# 📈 Graphique d'évolution des énergies renouvelables vs fossiles
st.subheader("📈 Évolution des Parts d'Électricité Renouvelable vs Fossile (%)")
st.line_chart(pd.DataFrame({"Renouvelables (%)": df_renewables, "Fossiles (%)": df_fossil}))

# 🌍 Carte interactive des énergies renouvelables
st.subheader("🌍 Part des Énergies Renouvelables par Pays")

# 🔹 Filtrer les données pour l'année sélectionnée
df_year = df[df["year"] == year_selected]

# 🌍 Création de la carte interactive avec Plotly
fig = px.choropleth(
    df_year,
    locations="iso_code",
    color="renewables_share_elec",
    hover_name="country",
    color_continuous_scale="YlGnBu",
    title=f"Part des énergies renouvelables en {year_selected}",
    labels={'renewables_share_elec': 'Part (%)'},
    template="plotly_dark"
)

# Personnalisation de la carte pour un rendu esthétique
fig.update_geos(
    visible=True,
    showcoastlines=True,
    coastlinecolor="black",
    coastlinewidth=1,
    projection_type="natural earth",
    lakecolor="rgb(255, 255, 255)",
    showland=True,
    landcolor="rgb(243, 243, 243)"
)

# Affichage de la carte
st.plotly_chart(fig, use_container_width=True)

# 🥧 Graphiques en camembert interactifs
st.subheader(f"🥧 Répartition des Sources d'Électricité - {year_selected}")

# 📌 Filtrer les données pour l'année sélectionnée
df_year = df[df['year'] == year_selected]

# 📌 Fonction pour calculer les moyennes des parts d'énergies
def get_renewable_shares(df):
    return [df['solar_share_elec'].mean(), df['wind_share_elec'].mean(), df['hydro_share_elec'].mean()]

def get_fossil_shares(df):
    return [df['coal_share_elec'].mean(), df['oil_share_elec'].mean(), df['gas_share_elec'].mean()]

# 📌 Récupérer les valeurs moyennes
shares_renewable = get_renewable_shares(df_year)
shares_fossil = get_fossil_shares(df_year)

# 📌 Définition des sources et couleurs
sources_renewable, colors_renewable = ['Solaire', 'Éolien', 'Hydroélectrique'], ['gold', 'lightblue', 'green']
sources_fossil, colors_fossil = ['Charbon', 'Pétrole', 'Gaz'], ['black', 'brown', 'gray']

# 🔹 Fonction pour créer des camemberts Plotly
def create_pie_chart(labels, values, title, colors):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, textinfo='percent+label', marker=dict(colors=colors))])
    fig.update_layout(title=title, title_x=0.5, template="plotly_dark")
    return fig

# Création des camemberts et affichage dynamiquement en fonction de l'année sélectionnée
fig_renewable = create_pie_chart(sources_renewable, shares_renewable, f"Répartition des Énergies Renouvelables - {year_selected}", colors_renewable)
fig_fossil = create_pie_chart(sources_fossil, shares_fossil, f"Répartition des Énergies Fossiles - {year_selected}", colors_fossil)

# Affichage des camemberts
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_renewable, use_container_width=True)
with col2:
    st.plotly_chart(fig_fossil, use_container_width=True)

# 📊 Ajouter le graphique de dispersion pour PIB et énergies
st.subheader("📊 Relation entre le PIB moyen et la part des énergies renouvelables et fossiles")

# Calculer le PIB moyen et la part moyenne des énergies renouvelables et non renouvelables par pays
df_avg = df.groupby('country', as_index=False).agg({
    'gdp': 'mean',
    'renewables_share_elec': 'mean',
    'fossil_share_elec': 'mean'
})

# Supprimer les valeurs aberrantes (PIB nul ou NaN)
df_avg = df_avg.dropna(subset=['gdp', 'renewables_share_elec', 'fossil_share_elec'])
df_avg = df_avg[df_avg['gdp'] > 0]

# Créer le graphique de dispersion avec Plotly
fig_scatter = go.Figure()

# Ajouter les énergies renouvelables
fig_scatter.add_trace(go.Scatter(
    x=df_avg['gdp'],
    y=df_avg['renewables_share_elec'],
    mode='markers',
    marker=dict(color='darkblue', size=12, opacity=0.6, line=dict(width=1, color='black')),
    name='Énergies Renouvelables'
))

# Ajouter les énergies fossiles
fig_scatter.add_trace(go.Scatter(
    x=df_avg['gdp'],
    y=df_avg['fossil_share_elec'],
    mode='markers',
    marker=dict(color='red', size=12, opacity=0.6, line=dict(width=1, color='black')),
    name='Énergies Fossiles'
))

# Ajouter une ligne horizontale à 100% pour la référence
fig_scatter.add_trace(go.Scatter(
    x=[min(df_avg['gdp']), max(df_avg['gdp'])],
    y=[100, 100],
    mode='lines',
    line=dict(dash='dash', color='gray'),
    name='100% Électricité'
))

# Paramètres du graphique
fig_scatter.update_layout(
    title="Relation entre le PIB moyen et la part des énergies renouvelables et fossiles",
    xaxis_title="PIB moyen (en $)",
    yaxis_title="Part de l'électricité (%)",
    xaxis=dict(type='log'),
    template='plotly_dark',
    hovermode='closest',
    showlegend=True,
)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig_scatter, use_container_width=True)

# 📝 Explications et contexte
st.markdown("""
    ### Contexte:
    Projet étudiant réalisé dans le cadre d'un cours d'Analyse de Données. L'objectif est d'analyser l'évolution de la part des énergies renouvelables et fossiles dans le monde de 1995 à 2020.
            Cette étude montre qu'entre 1995 et 2020 il y a eu une augmentation de la part des énergies renouvelables dans la production d'électricité mondiale.
            Très légèrement, la part des énergies fossiles a diminué, mais reste majoritaire dans la production d'électricité.
            Les changements sont possibles et "l'argent" n'est pas un facteur freinant.

    📈 **Graphique d'évolution**: Ce graphique montre l'évolution de la part des énergies renouvelables et fossiles à l'échelle mondiale.
    
    🌍 **Carte interactive**: Visualisez la part des énergies renouvelables par pays en fonction de l'année sélectionnée.
    
    🥧 **Camemberts**: Les camemberts vous permettent de visualiser la répartition des différentes sources d'énergies (renouvelables et fossiles) pour chaque année sélectionnée.
    
    📊 **Relation PIB et Énergies**: Ce graphique montre la relation entre le PIB moyen par pays et la part d'énergies renouvelables et fossiles.
""")
