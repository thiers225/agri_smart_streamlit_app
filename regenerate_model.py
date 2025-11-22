"""
Script pour régénérer le modèle de prédiction de rendement avec la version actuelle de scikit-learn
"""
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

print("Création d'un modèle de démonstration compatible avec scikit-learn 1.7.2...")

# Créer des données d'exemple pour entraîner un modèle de base
np.random.seed(42)
n_samples = 100

# Générer des données synthétiques
data = {
    'PL_HT': np.random.randint(100, 250, n_samples),
    'E_HT': np.random.randint(50, 150, n_samples),
    'DY_SK': np.random.randint(45, 85, n_samples),
    'AEZONE': np.random.choice(['Forest/Transitional', 'Moist Savanna'], n_samples),
    'RUST': np.random.randint(1, 6, n_samples),
    'BLIGHT': np.random.randint(1, 6, n_samples),
}

# Générer des rendements basés sur une formule simple
df = pd.DataFrame(data)
df['YIELD'] = (
    df['PL_HT'] * 10 + 
    df['E_HT'] * 8 - 
    df['DY_SK'] * 5 - 
    df['RUST'] * 100 - 
    df['BLIGHT'] * 100 + 
    np.random.normal(3000, 500, n_samples)
)

# Séparer features et target
X = df.drop('YIELD', axis=1)
y = df['YIELD']

# Définir les colonnes numériques et catégorielles
numeric_features = ['PL_HT', 'E_HT', 'DY_SK', 'RUST', 'BLIGHT']
categorical_features = ['AEZONE']

# Créer le preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
    ],
    remainder='drop'
)

# Créer le pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Entraîner le modèle
print("Entraînement du modèle...")
model.fit(X, y)

# Sauvegarder le modèle avec métadonnées
from save_model_with_metadata import save_model_with_metadata

print("\nSauvegarde du modèle avec métadonnées...")
save_model_with_metadata(model, X.columns.tolist())

print(f"\n✅ Modèle régénéré avec succès!")
print(f"Score R² sur les données d'entraînement : {model.score(X, y):.3f}")
