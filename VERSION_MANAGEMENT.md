# Guide de Gestion des Versions - Projet AGRI SMART

## 📦 Versions des Packages

Les versions actuelles sont enregistrées dans `requirements.txt` :
- **scikit-learn**: 1.7.2
- **tensorflow**: 2.20.0
- **streamlit**: 1.51.0
- **numpy**: 2.3.4
- **pandas**: 2.3.3
- **joblib**: 1.5.2
- **pillow**: 12.0.0

## ⚠️ Problème d'Incompatibilité Rencontré

### Le Problème
Le modèle `yield_prediction_model.pkl` a été créé avec une version plus ancienne de scikit-learn. Lors du chargement avec scikit-learn 1.7.2, l'erreur suivante est apparue :
```
Can't get attribute '_RemainderColsList' on <module 'sklearn.compose._column_transformer'>
```

### Pourquoi cela arrive ?
Les modèles scikit-learn sérialisés avec `joblib` ou `pickle` contiennent des références aux structures internes de la bibliothèque. Quand ces structures changent entre versions, le modèle devient incompatible.

## ✅ Solutions pour Éviter ce Problème

### Solution 1 : Toujours Entraîner et Déployer avec les Mêmes Versions
1. **Enregistrez les versions** après l'entraînement :
   ```bash
   pip freeze > requirements_training.txt
   ```

2. **Installez les mêmes versions** en production :
   ```bash
   pip install -r requirements_training.txt
   ```

### Solution 2 : Régénérer le Modèle (Ce que nous avons fait)
Si vous mettez à jour scikit-learn, régénérez le modèle :
```bash
python regenerate_model.py
```

### Solution 3 : Utiliser des Formats Plus Robustes
Pour les projets futurs, considérez :

#### Option A : ONNX (Recommandé pour la production)
```python
# Entraînement
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, n_features]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Chargement
import onnxruntime as rt
sess = rt.InferenceSession("model.onnx")
```

#### Option B : Skops (Plus simple)
```python
# Entraînement
import skops.io as sio
sio.dump(model, "model.skops")

# Chargement
model = sio.load("model.skops", trusted=True)
```

### Solution 4 : Versioning des Modèles avec Métadonnées
Créez un fichier `model_metadata.json` :
```json
{
  "model_version": "1.0.0",
  "created_date": "2025-11-22",
  "sklearn_version": "1.7.2",
  "python_version": "3.12",
  "features": ["PL_HT", "E_HT", "DY_SK", "AEZONE", "RUST", "BLIGHT"],
  "performance": {
    "r2_score": 0.911,
    "mae": 234.5
  }
}
```

## 🔄 Workflow Recommandé

### Pour l'Entraînement (Google Colab)
1. Entraînez le modèle
2. Enregistrez les versions :
   ```python
   import sklearn, joblib, pandas, numpy
   versions = {
       'sklearn': sklearn.__version__,
       'joblib': joblib.__version__,
       'pandas': pandas.__version__,
       'numpy': numpy.__version__
   }
   joblib.dump(versions, 'models/package_versions.pkl')
   ```
3. Téléchargez le modèle ET les versions

### Pour le Déploiement (Streamlit)
1. Vérifiez les versions avant de charger :
   ```python
   saved_versions = joblib.load('models/package_versions.pkl')
   current_sklearn = sklearn.__version__
   
   if saved_versions['sklearn'] != current_sklearn:
       st.warning(f"⚠️ Version mismatch! Model: {saved_versions['sklearn']}, Current: {current_sklearn}")
   ```

2. Si incompatible, régénérez ou installez la bonne version

## 📝 Checklist de Déploiement

- [ ] Vérifier que `requirements.txt` est à jour
- [ ] Tester le chargement du modèle localement
- [ ] Vérifier les versions de packages
- [ ] Documenter les performances du modèle
- [ ] Créer un backup du modèle fonctionnel

## 🛠️ Commandes Utiles

```bash
# Voir les versions installées
pip list

# Enregistrer toutes les versions
pip freeze > requirements_full.txt

# Installer des versions spécifiques
pip install scikit-learn==1.7.2

# Créer un environnement virtuel propre
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 📚 Ressources
- [Scikit-learn Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Skops Documentation](https://skops.readthedocs.io/)
- [ONNX for Scikit-learn](https://onnx.ai/sklearn-onnx/)
