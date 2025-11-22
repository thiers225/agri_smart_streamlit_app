"""
Script de vérification de compatibilité des versions
Vérifie que les versions locales correspondent aux versions utilisées pour l'entraînement
"""
import json
import os
import sys

def check_compatibility():
    """Vérifie la compatibilité des versions entre Colab et Local"""
    
    print("=" * 60)
    print("🔍 VÉRIFICATION DE COMPATIBILITÉ DES VERSIONS")
    print("=" * 60)
    print()
    
    # Importer les packages
    try:
        import tensorflow as tf
        import sklearn
        import numpy as np
        import pandas as pd
        import joblib
        import streamlit as st
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Installez les dépendances: pip install -r requirements.txt")
        return False
    
    # Versions locales
    local_versions = {
        'tensorflow': tf.__version__,
        'scikit-learn': sklearn.__version__,
        'numpy': np.__version__,
        'pandas': pd.__version__,
        'joblib': joblib.__version__,
        'streamlit': st.__version__,
        'python': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
    
    print("📦 VERSIONS LOCALES")
    print("-" * 60)
    for pkg, version in local_versions.items():
        print(f"  {pkg:15s} : {version}")
    print()
    
    # Vérifier les métadonnées du modèle de rendement
    metadata_path = 'models/model_metadata.json'
    if os.path.exists(metadata_path):
        print("📊 VÉRIFICATION MODÈLE DE RENDEMENT")
        print("-" * 60)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        if 'package_versions' in metadata:
            all_compatible = True
            
            for pkg, colab_version in metadata['package_versions'].items():
                local_version = local_versions.get(pkg, 'N/A')
                
                if pkg == 'numpy':
                    # Pour NumPy, vérifier seulement la version majeure
                    compatible = colab_version.split('.')[0] == local_version.split('.')[0]
                else:
                    compatible = colab_version == local_version
                
                status = "✅" if compatible else "⚠️ "
                print(f"  {status} {pkg:15s} : Colab={colab_version:10s} Local={local_version}")
                
                if not compatible:
                    all_compatible = False
                    print(f"     → Recommandation: pip install {pkg}=={colab_version}")
            
            print()
            if all_compatible:
                print("✅ Toutes les versions sont compatibles!")
            else:
                print("⚠️  Certaines versions diffèrent. Voir recommandations ci-dessus.")
        else:
            print("  ℹ️  Pas de métadonnées de versions trouvées")
        print()
    else:
        print(f"⚠️  Fichier de métadonnées non trouvé: {metadata_path}")
        print("   Régénérez le modèle avec: python regenerate_model.py")
        print()
    
    # Vérifier les métadonnées du modèle de maladie
    disease_metadata_path = 'models/disease_model_metadata.json'
    if os.path.exists(disease_metadata_path):
        print("🦠 VÉRIFICATION MODÈLE DE DÉTECTION DE MALADIES")
        print("-" * 60)
        
        with open(disease_metadata_path, 'r', encoding='utf-8') as f:
            disease_metadata = json.load(f)
        
        if 'tensorflow_version' in disease_metadata:
            colab_tf = disease_metadata['tensorflow_version']
            local_tf = local_versions['tensorflow']
            
            compatible = colab_tf == local_tf
            status = "✅" if compatible else "⚠️ "
            
            print(f"  {status} TensorFlow    : Colab={colab_tf:10s} Local={local_tf}")
            
            if not compatible:
                print(f"     → Recommandation: pip install tensorflow=={colab_tf}")
            else:
                print("  ✅ Version TensorFlow compatible!")
        print()
    else:
        print("ℹ️  Métadonnées du modèle de maladie non trouvées")
        print(f"   Créez le fichier: {disease_metadata_path}")
        print()
    
    # Vérifier que les fichiers de modèle existent
    print("📁 VÉRIFICATION DES FICHIERS DE MODÈLE")
    print("-" * 60)
    
    required_files = [
        'models/maize_mobilenetv2_model.keras',
        'models/yield_prediction_model.pkl',
        'models/model_input_columns.pkl'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            all_files_exist = False
    
    print()
    
    if all_files_exist:
        print("✅ Tous les fichiers de modèle sont présents!")
    else:
        print("❌ Certains fichiers de modèle sont manquants.")
        print("   Téléchargez-les depuis Google Colab ou régénérez-les.")
    
    print()
    print("=" * 60)
    print("🎯 RÉSUMÉ")
    print("=" * 60)
    
    # Vérifier requirements.txt
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt existe")
        print("   Pour installer: pip install -r requirements.txt")
    else:
        print("⚠️  requirements.txt non trouvé")
    
    print()
    print("📚 Pour plus d'informations, consultez:")
    print("   - COLAB_LOCAL_COMPATIBILITY.md")
    print("   - VERSION_MANAGEMENT.md")
    print()
    
    return True

if __name__ == "__main__":
    check_compatibility()
