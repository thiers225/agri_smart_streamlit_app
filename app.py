import streamlit as st
import pandas as pd
import joblib

# === Chargement du modèle ===
MODEL_PATH = "agri_smart_yield_model.pkl"
model = joblib.load(MODEL_PATH)

# === Configuration de la page ===
st.set_page_config(
    page_title="AGRI-SMART 🌾 - Prédiction du rendement du maïs",
    page_icon="🌽",
    layout="centered"
)

# === Titre et description ===
st.title("🌾 AGRI-SMART — Prédiction du rendement du maïs")
st.markdown("""
Cette application prédit le **rendement estimé (t/ha)** à partir de paramètres agronomiques mesurés sur le terrain.
Renseignez les valeurs ci-dessous et cliquez sur **Prédire**.
""")

# === Saisie des variables ===
st.subheader("🧩 Données d’entrée")
pl_ht = st.number_input("Hauteur moyenne des plantes (PL_HT)", 100.0, 300.0, 170.0)
e_ht = st.number_input("Hauteur moyenne des épis (E_HT)", 50.0, 200.0, 90.0)
e_harv = st.number_input("Nombre d’épis récoltés (E_HARV)", 10, 50, 25)
blight = st.slider("Indice de brûlure foliaire (BLIGHT)", 1, 9, 3)
curv = st.number_input("Indice morphologique (CURV)", 0.5, 2.0, 1.2)

# === Préparation des données ===
input_data = pd.DataFrame({
    "PL_HT": [pl_ht],
    "E_HT": [e_ht],
    "E_HARV": [e_harv],
    "BLIGHT": [blight],
    "CURV": [curv]
})

# === Prédiction ===
if st.button("🔍 Prédire le rendement"):
    prediction = model.predict(input_data)[0]
    st.success(f"🌽 **Rendement estimé : {prediction:.2f} t/ha**")

    # Analyse complémentaire
    st.caption("Modèle utilisé : XGBoost entraîné sur données Côte d’Ivoire (IITA).")