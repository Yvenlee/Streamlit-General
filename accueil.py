import streamlit as st

st.set_page_config(page_title="Portfolio - Yvenlee Vonin--Kabel", layout="wide")

st.title("**Yvenlee Vonin--Kabel**")
st.subheader("Bienvenue sur mon portfolio personnel !")

st.markdown("""
---

### À propos de moi

Passionné par l'exploration et l'analyse des données, j'aime transformer des informations complexes en solutions concrètes. Mon objectif est de participer à des projets innovants tout en développant mes compétences en :

- **Python**, **Machine Learning**, **Deep Learning**
- **Analyse et visualisation de données**
- **Nettoyage**, **modélisation**, et **interprétation des données**

---

### Pourquoi me choisir ?

-  Finaliste **d’un Hackathon organisé par mon école avec Engie**
-  Excellent **esprit d’équipe** et forte **adaptabilité**
-  Véritable **enthousiasme pour les projets data-driven**

N'hésitez pas à consulter mes projets ci-contre (Petite flèche en haut à gauche sur mobile) ou à me contacter !

---
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📞 Téléphone")
    st.write("+33 7 70 20 42 25")

with col2:
    st.subheader("📧 E-mail")
    st.write("yvenlycee@gmail.com")
