import streamlit as st

st.set_page_config(page_title="Portfolio - Recherche de Stage", layout="wide")

st.title("**YVENLEE VONIN--KABEL**")

st.subheader("Bienvenue sur mon portfolio !")

st.write("""
    Bonjour et bienvenue sur mon portfolio ! 👋

    Actuellement à la recherche d'un stage **Data Science / Analyse de Données**. 
    - **Durée** : 6 mois
    - **Rythme** : 2 semaines en entreprise, 1 semaine à l'école
    - **Disponibilité** : ASAP
    
    J'adore explorer et analyser des données pour résoudre des problèmes et aider à prendre des décisions plus éclairées. Mon but, c'est de participer à des projets intéressants où je peux apprendre encore plus tout en apportant mes compétences à l’équipe.
    
    **Mon profil** :
    - Compétences en : Python, Machine Learning, Deep Learning, Analyse de Données
    - Méthodologies : Nettoyage de données, Visualisation, Modélisation

    J'ai hâte de discuter avec vous et d'apporter ma contribution à vos projets ! 🚀

    ### Pourquoi me choisir ?
         
    - **Passion pour l'analyse de données**
    - **Finaliste d'un Hackaton organisé par mon école et lié à Engie**
    - **Esprit d'équipe** et **adaptabilité**

    N'hésitez pas à explorer mes projets et à me contacter si vous souhaitez en savoir plus !
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📞 Mon numéro de téléphone")
    st.write("+33 7 70 20 42 25")

with col2:
    st.subheader("📧 Mon e-mail")
    st.write("yvenlycee@gmail.com")
