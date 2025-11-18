import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# ============================================================
# CONFIGURATION GÉNÉRALE
# ============================================================
st.set_page_config(
    page_title="AGRI-SMART 🌽",
    page_icon="🌱",
    layout="wide"
)

st.sidebar.title("🌱 AGRI-SMART")

choice = st.sidebar.radio(
    "Choisissez un module :",
    ["🌾 Prédiction du rendement", "🌿 Détection des maladies du maïs"]
)

# ============================================================
# 📁 CHEMINS DES MODELES
# ============================================================
YIELD_MODEL_PATH = "models/agri_smart_yield_model.pkl"   # Ton modèle XGBoost
B3_MODEL_PATH = "models/efficientnet_b3_maize.keras"     # Ton modèle B3

# Chargement modèle rendement (XGBoost ou RandomForest)
try:
    yield_model = joblib.load(YIELD_MODEL_PATH)
except:
    yield_model = None

# Chargement modèle EfficientNet-B3
try:
    disease_model = tf.keras.models.load_model(B3_MODEL_PATH)
except:
    disease_model = None


# ============================================================
# LISTE DES CLASSES (MODEL B3)
# ============================================================
CLASS_NAMES = [
    "Chenille légionnaire (Fall Armyworm)",
    "Sauterelle (Grasshopper)",
    "Feuille saine (Healthy)",
    "Charançon / Coléoptère (Leaf Beetle)",
    "Brûlure foliaire (Leaf Blight)",
    "Tache foliaire (Leaf Spot)",
    "Virus strié du maïs (Streak Virus)"
]

# CONSEILS AGRONOMIQUES
ADVICE = {
    CLASS_NAMES[0]: "Inspecter les plants voisins, appliquer des biopesticides (Bt).",
    CLASS_NAMES[1]: "Utiliser des filets anti-insectes ou pulvériser du neem.",
    CLASS_NAMES[2]: "Aucun problème détecté. Continuer un suivi régulier.",
    CLASS_NAMES[3]: "Enlever manuellement les insectes et surveiller la fertilité du sol.",
    CLASS_NAMES[4]: "Améliorer l'aération, éviter l’arrosage par aspersion.",
    CLASS_NAMES[5]: "Traiter avec un fongicide à base de cuivre.",
    CLASS_NAMES[6]: "Retirer les plants infectés pour éviter la propagation."
}

# ============================================================
# 🔧 FONCTIONS UTILITAIRES
# ============================================================

def preprocess_image(uploaded_file):
    img = image.load_img(uploaded_file, target_size=(300, 300))
    img_arr = image.img_to_array(img) / 255.0
    img_arr = np.expand_dims(img_arr, axis=0)
    return img, img_arr


# ============================================================
# 🌾 MODULE 1 — PRÉDICTION DU RENDEMENT (VERSION ORIGINALE)
# ============================================================
if choice == "🌾 Prédiction du rendement":

    st.title("AGRI-SMART : Prédiction du rendement du maïs")
    st.markdown("""
    Cette application prédit le **rendement estimé (t/ha)** à partir de paramètres agronomiques.
    Renseignez les valeurs ci-dessous et cliquez sur **Prédire**.
    """)

    # === Champs manuels (ORIGINAUX) ===
    st.subheader("🧩 Données d’entrée")
    col1, col2 = st.columns(2)

    with col1:
        pl_ht = st.number_input("Hauteur moyenne des plantes (PL_HT)", 100.0, 300.0, 170.0)
        e_ht = st.number_input("Hauteur moyenne des épis (E_HT)", 50.0, 200.0, 90.0)
        e_harv = st.number_input("Nombre d’épis récoltés (E_HARV)", 10, 50, 25)

    with col2:
        blight = st.slider("Indice de brûlure foliaire (BLIGHT)", 1, 9, 3)
        curv = st.number_input("Indice morphologique (CURV)", 0.5, 2.0, 1.2)

    # === Préparation dataframe ===
    input_data = pd.DataFrame({
        "PL_HT": [pl_ht],
        "E_HT": [e_ht],
        "E_HARV": [e_harv],
        "BLIGHT": [blight],
        "CURV": [curv]
    })

    # === Prédiction ===
    if st.button("🔍 Prédire le rendement"):
        if yield_model is None:
            st.error("❌ Modèle de rendement non trouvé.")
        else:
            prediction = yield_model.predict(input_data)[0]
            st.success(f"🌽 **Rendement estimé : {prediction:.2f} t/ha**")
            st.caption("Modèle XGBoost — Données Côte d'Ivoire (IITA).")


# ============================================================
# 🌿 MODULE 2 — DÉTECTION DES MALADIES (EFFNET-B3)
# ============================================================
else:

    st.title("AGRI-SMART: Détection de maladies du maïs")
    st.write("Téléchargez une image de feuille pour analyser son état.")

    uploaded_image = st.file_uploader("📤 Importer une image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:

        img, img_array = preprocess_image(uploaded_image)
        st.image(img, caption="Image téléchargée", use_column_width=True)

        if st.button("🔍 Lancer la détection"):

            if disease_model is None:
                st.error(" Modèle EfficientNet-B3 introuvable.")
            else:
                preds = disease_model.predict(img_array)
                idx = np.argmax(preds)
                confidence = float(np.max(preds))

                disease = CLASS_NAMES[idx]

                st.subheader("🧪 Résultat de la détection")
                st.success(f"**Maladie détectée : {disease}**")
                st.write(f"🔎 **Confiance du modèle : {confidence:.2%}**")

                # Probabilités
                st.subheader("📊 Probabilités par classe")
                st.bar_chart({CLASS_NAMES[i]: float(preds[0][i]) for i in range(len(CLASS_NAMES))})

                # Conseil
                st.info(f"📝 **Conseil agronomique :** {ADVICE[disease]}")



# Footer
st.sidebar.markdown("---")
st.sidebar.write("© 2025 — Projet AGRI-SMART")
