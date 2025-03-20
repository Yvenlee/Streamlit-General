import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analyse des Accidents", layout="wide")

st.title("📊 Analyse des Accidents et des Équipements de Sécurité")

# Contexte : présentation du tableau de bord et des objectifs de l'analyse
st.write("""
    Dans le cadre d'un projet scolaire j'ai réalisé **ma toute prmière analyse de données** sur les accidents de la route en France.
""")

# Résumé : objectifs de l'analyse
st.write("""
    L'objectif de ce tableau de bord est de fournir une vision claire et concise de l'impact de différents facteurs 
    sur la survenue des accidents. 
    Cela peut aider à mieux comprendre les risques, à informer les décisions en matière de sécurité routière, 
    et à mettre en place des politiques de prévention plus ciblées.
""")

@st.cache_data
def load_and_clean_data():
    characteristic_df = pd.read_csv('datasets/caracteristics.csv', encoding='ISO-8859-1')
    users_df = pd.read_csv('datasets/users.csv', encoding='ISO-8859-1')

    for df in [characteristic_df, users_df]:
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

    return characteristic_df, users_df

characteristic_df, users_df = load_and_clean_data()

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    st.subheader("🦺 Répartition des équipements de sécurité")
    
    equipment_mapping = {
        1: 'Ceinture',
        2: 'Casque',
        3: 'Dispositif pour enfants',
        4: 'Équipement réfléchissant',
        9: 'Autre'
    }
    
    users_df['secu'] = users_df['secu'].map(equipment_mapping)
    equipment_usage = users_df['secu'].value_counts().reset_index()
    equipment_usage.columns = ['Équipement', 'Nombre']

    fig1 = px.pie(equipment_usage, names='Équipement', values='Nombre', 
                  title='Répartition des équipements de sécurité', 
                  color_discrete_sequence=px.colors.qualitative.Set2)
    
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.subheader("⚠️ Gravité des accidents selon l'équipement")
    
    users_df['secu'] = users_df['secu'].map({
        1: 'Ceinture',
        2: 'Casque',
        3: 'Dispositif pour enfants',
        4: 'Équipement réfléchissant',
        9: 'Autre'
    })

    if 'grav' in users_df.columns:
        gravite_mapping = {
            1: 'Indemne',
            2: 'Tué',
            3: 'Blessé hospitalisé',
            4: 'Blessé léger'
        }
        users_df['grav'] = users_df['grav'].map(gravite_mapping)

        fig2 = px.histogram(users_df, x='grav', color='secu', barmode='group',
                            title="Impact des équipements sur la gravité des accidents",
                            labels={'grav': 'Gravité de l\'accident', 'secu': 'Équipement de sécurité'})
        
        st.plotly_chart(fig2, use_container_width=True)

with row2_col1:
    st.subheader("👶👨‍🦳 Distribution des personnes par tranche d'âge")

    users_df['age'] = 2022 - users_df['an_nais']
    users_df = users_df.dropna(subset=['age'])

    fig3 = px.histogram(users_df, x='age', nbins=20, 
                        title="Distribution des âges des personnes impliquées dans les accidents",
                        labels={'age': 'Âge'},
                        color_discrete_sequence=['skyblue'])

    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    st.subheader("🚻 Répartition des sexes des personnes impliquées dans les accidents")

    users_df['sexe'] = users_df['sexe'].replace({1: 'Homme', 2: 'Femme'})
    sex_percentage = users_df['sexe'].value_counts().reset_index()
    sex_percentage.columns = ['Sexe', 'Nombre']

    fig4 = px.pie(sex_percentage, names='Sexe', values='Nombre', 
                  title="Répartition des sexes des personnes impliquées dans les accidents",
                  color_discrete_sequence=['blue', 'pink'])

    st.plotly_chart(fig4, use_container_width=True)

st.write("""
    ### Résumé des observations :
    
    - La grande majorité des accidents sont réalisés par des automobilistes équipés de la ceinture de sécurité **au moment de l'impact**.
    - Les **accidents graves** sont moins fréquents parmi ceux qui portent des équipements de sécurité.
    - La **répartition par âge** montre une concentration des accidents parmi les jeunes adultes et les personnes âgées.
    - En ce qui concerne le **sexe**, les hommes sont plus souvent impliqués dans des accidents.

    Ces résultats peuvent aider à identifier les zones de prévention les plus urgentes et à ajuster les stratégies de sécurité routière pour réduire les risques d'accidents.
""")
