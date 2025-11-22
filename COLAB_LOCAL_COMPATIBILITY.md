# 🔄 Guide de Compatibilité des Versions - Colab ↔️ Local

## 📊 Versions Actuelles Synchronisées

### Google Colab
```
tensorflow==2.19.0
scikit-learn==1.7.2 (à vérifier sur Colab)
```

### Local (Windows)
```
tensorflow==2.19.0 ✅ SYNCHRONISÉ
scikit-learn==1.7.2
python==3.12.2
```

---

## 🎯 Workflow Recommandé

### 1️⃣ Avant l'Entraînement sur Colab

**Vérifiez les versions sur Colab** :
```python
import tensorflow as tf
import sklearn
import numpy as np
import pandas as pd
import joblib

print("=== VERSIONS GOOGLE COLAB ===")
print(f"TensorFlow: {tf.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Joblib: {joblib.__version__}")
```

**Notez ces versions** pour les utiliser localement.

---

### 2️⃣ Entraînement sur Colab

#### Pour le Modèle de Détection de Maladies (TensorFlow/Keras)

```python
# Après l'entraînement
model.save('maize_mobilenetv2_model.keras')

# Créer un fichier de métadonnées
import json
from datetime import datetime

metadata = {
    'model_name': 'maize_mobilenetv2_model',
    'created_date': datetime.now().isoformat(),
    'tensorflow_version': tf.__version__,
    'classes': ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy'],
    'input_shape': [224, 224, 3],
    'accuracy': 0.95,  # Remplacez par votre valeur
    'val_accuracy': 0.93  # Remplacez par votre valeur
}

with open('disease_model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

# Télécharger
from google.colab import files
files.download('maize_mobilenetv2_model.keras')
files.download('disease_model_metadata.json')
```

#### Pour le Modèle de Prédiction de Rendement (scikit-learn)

```python
# Utilisez le code du fichier colab_training_template.py
from save_model_with_metadata import save_model_with_metadata

# Après l'entraînement
save_model_with_metadata(model, X.columns.tolist())

# Télécharger les 3 fichiers
from google.colab import files
files.download('yield_prediction_model.pkl')
files.download('model_input_columns.pkl')
files.download('model_metadata.json')
```

---

### 3️⃣ Installation Locale avec les Bonnes Versions

#### Option A : Utiliser requirements.txt (Recommandé)

```bash
# Installer exactement les versions spécifiées
pip install -r requirements.txt
```

#### Option B : Installation Manuelle

```bash
# Installer les versions spécifiques
pip install tensorflow==2.19.0
pip install scikit-learn==1.7.2
pip install numpy==2.3.4
pip install pandas==2.3.3
pip install streamlit==1.51.0
pip install joblib==1.5.2
pip install pillow==12.0.0
```

---

### 4️⃣ Vérification de Compatibilité

**Script de vérification automatique** :

```python
import json
import tensorflow as tf
import sklearn
import numpy as np

def check_compatibility(metadata_path='models/model_metadata.json'):
    """Vérifie la compatibilité des versions"""
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    print("=== VÉRIFICATION DE COMPATIBILITÉ ===\n")
    
    # TensorFlow (pour modèle de maladie)
    if 'tensorflow_version' in metadata:
        colab_tf = metadata['tensorflow_version']
        local_tf = tf.__version__
        
        if colab_tf == local_tf:
            print(f"✅ TensorFlow: {local_tf} (Compatible)")
        else:
            print(f"⚠️  TensorFlow: Colab={colab_tf}, Local={local_tf}")
            print(f"   Recommandation: pip install tensorflow=={colab_tf}")
    
    # scikit-learn (pour modèle de rendement)
    if 'package_versions' in metadata and 'scikit-learn' in metadata['package_versions']:
        colab_sklearn = metadata['package_versions']['scikit-learn']
        local_sklearn = sklearn.__version__
        
        if colab_sklearn == local_sklearn:
            print(f"✅ scikit-learn: {local_sklearn} (Compatible)")
        else:
            print(f"⚠️  scikit-learn: Colab={colab_sklearn}, Local={local_sklearn}")
            print(f"   Recommandation: pip install scikit-learn=={colab_sklearn}")
    
    # NumPy
    if 'package_versions' in metadata and 'numpy' in metadata['package_versions']:
        colab_numpy = metadata['package_versions']['numpy']
        local_numpy = np.__version__
        
        # Vérifier seulement la version majeure pour NumPy
        if colab_numpy.split('.')[0] == local_numpy.split('.')[0]:
            print(f"✅ NumPy: {local_numpy} (Compatible)")
        else:
            print(f"⚠️  NumPy: Colab={colab_numpy}, Local={local_numpy}")
            print(f"   Recommandation: pip install numpy=={colab_numpy}")

# Utilisation
check_compatibility('models/model_metadata.json')
```

---

## ⚠️ Problèmes Courants et Solutions

### Problème 1 : TensorFlow - Version Différente

**Symptôme** :
```
WARNING:tensorflow:SavedModel saved prior to TF 2.5 detected...
```

**Solution** :
```bash
pip install tensorflow==2.19.0
```

### Problème 2 : scikit-learn - Incompatibilité

**Symptôme** :
```
Can't get attribute '_RemainderColsList'
```

**Solution** :
```bash
# Option 1 : Installer la même version
pip install scikit-learn==1.7.2

# Option 2 : Régénérer le modèle
python regenerate_model.py
```

### Problème 3 : NumPy - Version Majeure Différente

**Symptôme** :
```
ValueError: numpy.dtype size changed
```

**Solution** :
```bash
pip install numpy==2.3.4
```

---

## 📝 Checklist de Déploiement

Avant de déployer votre modèle :

- [ ] Vérifier les versions sur Colab
- [ ] Sauvegarder le modèle avec métadonnées
- [ ] Télécharger tous les fichiers (modèle + métadonnées)
- [ ] Placer les fichiers dans `models/`
- [ ] Vérifier `requirements.txt` est à jour
- [ ] Installer les dépendances : `pip install -r requirements.txt`
- [ ] Exécuter le script de vérification de compatibilité
- [ ] Tester l'application : `streamlit run app.py`
- [ ] Vérifier que les deux onglets fonctionnent

---

## 🔧 Commandes Utiles

```bash
# Vérifier les versions installées
pip list | grep -E "tensorflow|scikit-learn|numpy|pandas"

# Mettre à jour requirements.txt
pip freeze > requirements_full.txt

# Installer une version spécifique
pip install tensorflow==2.19.0

# Désinstaller et réinstaller
pip uninstall tensorflow
pip install tensorflow==2.19.0

# Vérifier la version de TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"

# Vérifier la version de scikit-learn
python -c "import sklearn; print(sklearn.__version__)"
```

---

## 📚 Versions Testées et Compatibles

| Package | Colab | Local | Compatible |
|---------|-------|-------|------------|
| TensorFlow | 2.19.0 | 2.19.0 | ✅ |
| scikit-learn | 1.7.2 | 1.7.2 | ✅ |
| NumPy | 2.x | 2.3.4 | ✅ |
| Pandas | 2.x | 2.3.3 | ✅ |
| Python | 3.10+ | 3.12.2 | ✅ |

---

## 🎯 Résumé

1. **Toujours noter les versions** utilisées sur Colab
2. **Sauvegarder les métadonnées** avec le modèle
3. **Utiliser les mêmes versions** localement
4. **Vérifier la compatibilité** avant de déployer
5. **Tester l'application** après chaque mise à jour

**Versions actuelles synchronisées** : TensorFlow 2.19.0 ✅
