"""
📝 Code à ajouter à votre notebook Google Colab pour l'entraînement du modèle

Ajoutez ces cellules à la fin de votre notebook maize_yield_prediction.ipynb
"""

# ============================================================================
# CELLULE 1 : Installer les packages nécessaires (si pas déjà fait)
# ============================================================================
"""
!pip install scikit-learn joblib pandas numpy
"""

# ============================================================================
# CELLULE 2 : Fonction de sauvegarde avec métadonnées
# ============================================================================
"""
import joblib
import json
from datetime import datetime
import sklearn
import pandas as pd
import numpy as np
import sys

def save_model_with_metadata(model, input_columns, model_path='yield_prediction_model.pkl', 
                             metadata_path='model_metadata.json'):
    '''
    Sauvegarde un modèle avec ses métadonnées de version
    '''
    
    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    joblib.dump(input_columns, 'model_input_columns.pkl')
    
    # Créer les métadonnées
    metadata = {
        'model_version': '1.0.0',
        'created_date': datetime.now().isoformat(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'package_versions': {
            'scikit-learn': sklearn.__version__,
            'joblib': joblib.__version__,
            'pandas': pd.__version__,
            'numpy': np.__version__
        },
        'input_columns': input_columns,
        'model_type': type(model).__name__
    }
    
    # Sauvegarder les métadonnées
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Modèle sauvegardé : {model_path}")
    print(f"✅ Métadonnées sauvegardées : {metadata_path}")
    print(f"\\nVersions enregistrées :")
    for pkg, version in metadata['package_versions'].items():
        print(f"  - {pkg}: {version}")
    
    return metadata
"""

# ============================================================================
# CELLULE 3 : Sauvegarder le modèle après l'entraînement
# ============================================================================
"""
# Après avoir entraîné votre modèle (remplacez 'model' et 'X' par vos variables)
# model = votre_pipeline_ou_modele
# X = votre_dataframe_de_features

# Sauvegarder avec métadonnées
metadata = save_model_with_metadata(
    model=model,
    input_columns=X.columns.tolist()
)

# Afficher les métadonnées
print("\\n" + "="*50)
print("MÉTADONNÉES DU MODÈLE")
print("="*50)
import json
print(json.dumps(metadata, indent=2))
"""

# ============================================================================
# CELLULE 4 : Télécharger les fichiers depuis Colab
# ============================================================================
"""
# Télécharger les fichiers
from google.colab import files

print("Téléchargement des fichiers...")
files.download('yield_prediction_model.pkl')
files.download('model_input_columns.pkl')
files.download('model_metadata.json')

print("✅ Tous les fichiers ont été téléchargés!")
print("\\n📁 Placez ces 3 fichiers dans le dossier 'models/' de votre application Streamlit")
"""

# ============================================================================
# CELLULE 5 : Créer un fichier requirements.txt pour Colab
# ============================================================================
"""
# Enregistrer les versions utilisées pour l'entraînement
import sklearn, joblib, pandas, numpy, tensorflow

versions_text = f'''# Versions utilisées pour l'entraînement du modèle
# Généré le {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

scikit-learn=={sklearn.__version__}
joblib=={joblib.__version__}
pandas=={pandas.__version__}
numpy=={numpy.__version__}
'''

# Si vous utilisez TensorFlow
try:
    versions_text += f'tensorflow=={tensorflow.__version__}\\n'
except:
    pass

with open('requirements_training.txt', 'w') as f:
    f.write(versions_text)

print(versions_text)
print("\\n✅ Fichier requirements_training.txt créé")

# Télécharger
files.download('requirements_training.txt')
"""

# ============================================================================
# EXEMPLE COMPLET D'UTILISATION
# ============================================================================
"""
# Voici un exemple complet de la fin de votre notebook :

# 1. Entraîner le modèle
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

model = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X_train, y_train)

# 2. Évaluer le modèle
from sklearn.metrics import r2_score, mean_absolute_error

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"R² Score: {r2:.3f}")
print(f"MAE: {mae:.2f}")

# 3. Sauvegarder avec métadonnées
metadata = save_model_with_metadata(
    model=model,
    input_columns=X.columns.tolist()
)

# Ajouter les métriques aux métadonnées
metadata['performance'] = {
    'r2_score': float(r2),
    'mae': float(mae)
}

with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

# 4. Télécharger tous les fichiers
from google.colab import files
files.download('yield_prediction_model.pkl')
files.download('model_input_columns.pkl')
files.download('model_metadata.json')
"""

print(__doc__)
