"""
Script pour sauvegarder un modèle avec ses métadonnées de version
Utiliser ce script lors de l'entraînement pour éviter les problèmes de compatibilité
"""
import joblib
import json
from datetime import datetime
import sklearn
import pandas as pd
import numpy as np
import sys

def save_model_with_metadata(model, input_columns, model_path='models/yield_prediction_model.pkl', 
                             metadata_path='models/model_metadata.json'):
    """
    Sauvegarde un modèle avec ses métadonnées de version
    
    Args:
        model: Le modèle scikit-learn entraîné
        input_columns: Liste des colonnes d'entrée
        model_path: Chemin pour sauvegarder le modèle
        metadata_path: Chemin pour sauvegarder les métadonnées
    """
    
    # Sauvegarder le modèle
    joblib.dump(model, model_path)
    joblib.dump(input_columns, 'models/model_input_columns.pkl')
    
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
    print(f"\nVersions enregistrées :")
    for pkg, version in metadata['package_versions'].items():
        print(f"  - {pkg}: {version}")

def load_model_with_version_check(model_path='models/yield_prediction_model.pkl',
                                  metadata_path='models/model_metadata.json'):
    """
    Charge un modèle et vérifie la compatibilité des versions
    
    Returns:
        model, input_columns, warnings (list)
    """
    warnings = []
    
    # Charger les métadonnées
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Vérifier les versions
        current_sklearn = sklearn.__version__
        saved_sklearn = metadata['package_versions']['scikit-learn']
        
        if current_sklearn != saved_sklearn:
            warnings.append(
                f"⚠️ Version scikit-learn différente! "
                f"Modèle: {saved_sklearn}, Actuel: {current_sklearn}"
            )
        
        # Vérifier numpy
        current_numpy = np.__version__
        saved_numpy = metadata['package_versions']['numpy']
        
        if current_numpy.split('.')[0] != saved_numpy.split('.')[0]:
            warnings.append(
                f"⚠️ Version majeure numpy différente! "
                f"Modèle: {saved_numpy}, Actuel: {current_numpy}"
            )
    
    except FileNotFoundError:
        warnings.append("⚠️ Fichier de métadonnées non trouvé")
    
    # Charger le modèle
    try:
        model = joblib.load(model_path)
        input_columns = joblib.load('models/model_input_columns.pkl')
        return model, input_columns, warnings
    except Exception as e:
        return None, None, warnings + [f"❌ Erreur de chargement: {str(e)}"]

# Exemple d'utilisation
if __name__ == "__main__":
    print("Ce script fournit des fonctions pour sauvegarder/charger des modèles avec vérification de version.")
    print("\nUtilisation dans votre code d'entraînement :")
    print("  from save_model_with_metadata import save_model_with_metadata")
    print("  save_model_with_metadata(model, X.columns.tolist())")
    print("\nUtilisation dans votre application :")
    print("  from save_model_with_metadata import load_model_with_version_check")
    print("  model, cols, warnings = load_model_with_version_check()")
