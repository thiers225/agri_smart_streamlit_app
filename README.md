# 🌽 AGRI SMART - Assistant Intelligent Maïs

Application Streamlit pour la détection de maladies du maïs et la prédiction de rendement.

## 📋 Versions des Packages

Versions actuelles (enregistrées le 2025-11-22) :
- **Python**: 3.12.2
- **scikit-learn**: 1.7.2
- **tensorflow**: 2.20.0
- **streamlit**: 1.51.0
- **numpy**: 2.3.4
- **pandas**: 2.3.3
- **joblib**: 1.5.2
- **pillow**: 12.0.0

## 🚀 Installation

### 1. Cloner le projet
```bash
cd agri_smart_streamlit_app
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur à l'adresse `http://localhost:8501`

## 📁 Structure du Projet

```
agri_smart_streamlit_app/
├── app.py                          # Application Streamlit principale
├── requirements.txt                # Dépendances Python
├── regenerate_model.py             # Script pour régénérer le modèle
├── save_model_with_metadata.py     # Utilitaire de sauvegarde avec métadonnées
├── VERSION_MANAGEMENT.md           # Guide de gestion des versions
├── models/
│   ├── maize_mobilenetv2_model.keras      # Modèle de détection de maladies
│   ├── yield_prediction_model.pkl         # Modèle de prédiction de rendement
│   ├── model_input_columns.pkl            # Colonnes d'entrée du modèle
│   └── model_metadata.json                # Métadonnées du modèle (versions)
└── README.md
```

## 🔧 Résolution de Problèmes

### ⚠️ Erreur "Can't get attribute '_RemainderColsList'"

Cette erreur indique une incompatibilité de version de scikit-learn.

**Solution 1 : Régénérer le modèle**
```bash
python regenerate_model.py
```

**Solution 2 : Installer la version exacte**
```bash
pip install scikit-learn==1.7.2
```

### ⚠️ Le modèle ne se charge pas

1. Vérifiez que les fichiers existent dans `models/` :
   - `yield_prediction_model.pkl`
   - `model_input_columns.pkl`

2. Vérifiez les versions dans `models/model_metadata.json`

3. Régénérez le modèle si nécessaire

## 🔄 Workflow de Développement

### Pour Entraîner un Nouveau Modèle

1. **Entraînez votre modèle** (dans Google Colab ou localement)

2. **Sauvegardez avec métadonnées** :
```python
from save_model_with_metadata import save_model_with_metadata

# Après l'entraînement
save_model_with_metadata(model, X.columns.tolist())
```

3. **Vérifiez les métadonnées** :
```bash
cat models/model_metadata.json
```

### Pour Déployer

1. **Vérifiez les versions** :
```bash
pip list | grep -E "scikit-learn|tensorflow|streamlit"
```

2. **Testez localement** :
```bash
streamlit run app.py
```

3. **Vérifiez que les deux onglets fonctionnent** :
   - 🦠 Détection de Maladies
   - 📈 Prédiction de Rendement

## 📊 Fonctionnalités

### 🦠 Détection de Maladies
- Upload d'image de feuille de maïs
- Détection de 4 classes :
  - Helminthosporiose (Blight)
  - Rouille Commune (Common Rust)
  - Tache Grise (Gray Leaf Spot)
  - Saine (Healthy)
- Affichage de la confiance et des probabilités détaillées
- Seuil de confiance à 60%

### 📈 Prédiction de Rendement
- Entrée de caractéristiques agronomiques :
  - Hauteur de la plante (cm)
  - Hauteur de l'épi (cm)
  - Jours jusqu'à l'apparition des soies
  - Zone agro-écologique
  - Scores de rouille et d'helminthosporiose
- Prédiction du rendement en kg/ha

## 🛠️ Commandes Utiles

```bash
# Voir les versions installées
pip list

# Mettre à jour requirements.txt
pip freeze > requirements.txt

# Régénérer le modèle
python regenerate_model.py

# Tester le chargement du modèle
python -c "from save_model_with_metadata import load_model_with_version_check; m, c, w = load_model_with_version_check(); print(w)"

# Nettoyer le cache Streamlit
streamlit cache clear
```

## 📚 Documentation

- [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) - Guide complet de gestion des versions
- [save_model_with_metadata.py](save_model_with_metadata.py) - Utilitaire de sauvegarde

## 👨‍💻 Développeur

Projet AGRI SMART - Mémoire eBIHAR

## 📝 Notes

- Le modèle de rendement actuel est basé sur des données synthétiques pour démonstration
- Pour un modèle de production, réentraînez avec vos données réelles
- Assurez-vous toujours que les versions de packages correspondent entre l'entraînement et le déploiement
