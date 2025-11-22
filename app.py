import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd
import joblib
import time
import os

# Set page config
st.set_page_config(
    page_title="Assistant Intelligent Maïs",
    page_icon="🌽",
    layout="centered"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stSuccess {
        background-color: #dff0d8;
        color: #3c763d;
    }
    .stError {
        background-color: #f2dede;
        color: #a94442;
    }
    h1 {
        color: #2E7D32;
        text-align: center;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Header
st.title("🌽 Assistant Intelligent Maïs")

# Tabs
tab1, tab2 = st.tabs(["🦠 Détection de Maladies", "📈 Prédiction de Rendement"])

# --- TAB 1: DISEASE DETECTION ---
with tab1:
    st.markdown("### Analyse de Santé des Plantes par IA")
    st.markdown("Téléchargez une photo de feuille de maïs pour détecter des maladies comme la Rouille, l'Helminthosporiose ou la Tache Grise.")

    # Load Model
    @st.cache_resource
    def load_disease_model():
        try:
            model = tf.keras.models.load_model('models/maize_mobilenetv2_model.keras')
            return model
        except Exception as e:
            return None

    disease_model = load_disease_model()

    if disease_model is None:
        st.error("⚠️ Modèle de maladie non trouvé ! Veuillez entraîner le modèle (`maize_disease_training_efficientnet.ipynb`) et placer 'maize_disease_model.keras' dans ce répertoire.")
    else:
        st.success("✅ Modèle de maladie chargé !")

    # Class Names (Must match training order)
    CLASS_NAMES = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']
    CLASS_TRANSLATIONS = {
        'Blight': 'Helminthosporiose (Blight)',
        'Common_Rust': 'Rouille Commune',
        'Gray_Leaf_Spot': 'Tache Grise (Gray Leaf Spot)',
        'Healthy': 'Saine'
    }

    # File Uploader
    uploaded_file = st.file_uploader("Choisissez une image de feuille...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display Image
        image = Image.open(uploaded_file)
        st.image(image, caption='Image de feuille téléchargée', use_container_width=True)
        
        if st.button("Analyser la feuille"):
            if disease_model is None:
                st.error("Impossible d'analyser sans modèle chargé.")
            else:
                with st.spinner('Analyse de l\'image en cours...'):
                    # Preprocess
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    img = image.resize((224, 224))
                    img_array = np.array(img)
                    img_array = img_array / 255.0  # Normalize
                    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

                    # Predict
                    predictions = disease_model.predict(img_array)
                    predicted_class_en = CLASS_NAMES[np.argmax(predictions[0])]
                    predicted_class_fr = CLASS_TRANSLATIONS.get(predicted_class_en, predicted_class_en)
                    confidence = 100 * np.max(predictions[0])
                    
                    time.sleep(1) # UX delay

                    # Threshold check
                    if confidence < 60:
                        st.warning(f"⚠️ **Image non reconnue** (Confiance : {confidence:.2f}%)")
                        st.markdown("Le modèle n'est pas assez sûr. Assurez-vous qu'il s'agit bien d'une feuille de maïs.")
                    else:
                        # Display Result
                        st.markdown(f"""
                        <div class="prediction-box">
                            <h2 style="color: #1B5E20; font-weight: bold;">Résultat : <span style="color: #2E7D32;">{predicted_class_fr}</span></h2>
                            <p style="color: #333;">Confiance : <strong>{confidence:.2f}%</strong></p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Additional Info based on class
                        if predicted_class_en == 'Healthy':
                            st.info(f"La plante semble saine ! (Confiance: {confidence:.2f}%)")
                        elif predicted_class_en == 'Blight':
                            st.warning(f"⚠️ Helminthosporiose détectée ({confidence:.2f}%). Envisagez d'utiliser des fongicides et des hybrides résistants.")
                        elif predicted_class_en == 'Common_Rust':
                            st.warning(f"⚠️ Rouille commune détectée ({confidence:.2f}%). Cherchez des pustules sur les feuilles.")
                        elif predicted_class_en == 'Gray_Leaf_Spot':
                            st.warning(f"⚠️ Tache grise détectée ({confidence:.2f}%). Cela peut réduire considérablement le rendement.")
                        
                        # Probability breakdown
                        with st.expander("Voir les détails de la détection"):
                            probs = predictions[0]
                            df_probs = pd.DataFrame({
                                'Maladie': [CLASS_TRANSLATIONS.get(c, c) for c in CLASS_NAMES],
                                'Confiance (%)': probs * 100
                            })
                            st.bar_chart(df_probs.set_index('Maladie'))

# --- TAB 2: YIELD PREDICTION ---
with tab2:
    st.markdown("### 🌾 Estimateur de Rendement du Maïs")
    st.markdown("Entrez les caractéristiques agronomiques pour prédire le rendement attendu (kg/ha).")

    # Load Yield Model
    @st.cache_resource
    def load_yield_model():
        try:
            model = joblib.load('models/yield_prediction_model.pkl')
            cols = joblib.load('models/model_input_columns.pkl')
            return model, cols, None
        except Exception as e:
            return None, None, str(e)

    yield_model, input_cols, error = load_yield_model()

    if yield_model is None:
        st.warning("⚠️ Modèle de rendement non trouvé. Veuillez exécuter `maize_yield_prediction.ipynb` pour générer 'yield_prediction_model.pkl'.")
        if error:
            st.error(f"Erreur détaillée : {error}")
        # Mock interface for demonstration
        st.info("Affichage de l'interface de démonstration (la prédiction sera simulée)")
    else:
        st.success("✅ Modèle de rendement chargé !")
    
    with st.form("yield_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            pl_ht = st.number_input("Hauteur de la plante (cm)", min_value=50, max_value=300, value=180)
            e_ht = st.number_input("Hauteur de l'épi (cm)", min_value=20, max_value=200, value=90)
            dy_sk = st.number_input("Jours jusqu'à l'apparition des soies (jours)", min_value=40, max_value=100, value=60)
        
        with col2:
            aezone = st.selectbox("Zone Agro-écologique", ["Forest/Transitional", "Moist Savanna"])
            rust_score = st.slider("Score de Rouille (1-5)", 1, 5, 2)
            blight_score = st.slider("Score d'Helminthosporiose (1-5)", 1, 5, 2)

        # Advanced/Hidden inputs (using defaults if model exists)
        # We create a DataFrame with all required columns
        
        submit_yield = st.form_submit_button("Prédire le Rendement")

    if submit_yield:
        if yield_model is not None and input_cols is not None:
            # Create input dataframe with 0s
            input_data = pd.DataFrame(0, index=[0], columns=input_cols)
            
            # Fill known values
            if 'PL_HT' in input_cols: input_data['PL_HT'] = pl_ht
            if 'E_HT' in input_cols: input_data['E_HT'] = e_ht
            if 'DY_SK' in input_cols: input_data['DY_SK'] = dy_sk
            if 'AEZONE' in input_cols: input_data['AEZONE'] = aezone # Pipeline handles encoding
            if 'RUST' in input_cols: input_data['RUST'] = rust_score
            if 'BLIGHT' in input_cols: input_data['BLIGHT'] = blight_score
            
            # Predict
            try:
                prediction = yield_model.predict(input_data)[0]
                st.markdown(f"""
                <div class="prediction-box">
                    <h2 style="color: #1B5E20; font-weight: bold;">Rendement Prédit</h2>
                    <h1 style="color: #2E7D32;">{prediction:,.2f} kg/ha</h1>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
        else:
            # Simulation for demo
            simulated_yield = (pl_ht * 10) + (e_ht * 5) - (dy_sk * 2) + 3000
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="color: #1B5E20; font-weight: bold;">Rendement Prédit (Démo)</h2>
                <h1 style="color: #2E7D32;">{simulated_yield:,.2f} kg/ha</h1>
                <p style="color: gray; font-size: 0.8em;">*Modèle non chargé, utilisation d'une formule heuristique</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("Développé pour le projet AGRI SMART")
