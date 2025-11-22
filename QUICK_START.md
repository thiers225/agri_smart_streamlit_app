# 📋 GUIDE RAPIDE - Gestion des Versions

## 🎯 Résumé en 30 secondes

Vous avez maintenant un système complet pour gérer les versions entre Google Colab et votre environnement local.

### Versions Actuelles
```
TensorFlow:    2.19.0 ✅ (synchronisé avec Colab)
scikit-learn:  1.7.2
NumPy:         2.1.3
Python:        3.12.2
```

---

## 🚀 Démarrage Rapide

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Vérifier la compatibilité
```bash
python check_compatibility.py
```

### 3. Lancer l'application
```bash
streamlit run app.py
```

---

## 📚 Documentation Disponible

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **[VERSION_SYNC_SUMMARY.md](VERSION_SYNC_SUMMARY.md)** | Résumé de la synchronisation | ⭐ Commencez ici |
| **[COLAB_LOCAL_COMPATIBILITY.md](COLAB_LOCAL_COMPATIBILITY.md)** | Guide Colab ↔️ Local | Avant d'entraîner sur Colab |
| **[VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)** | Gestion complète des versions | Pour comprendre en profondeur |
| **[RESOLUTION_SUMMARY.md](RESOLUTION_SUMMARY.md)** | Résolution du problème initial | Pour référence historique |
| **[README.md](README.md)** | Documentation du projet | Vue d'ensemble du projet |

---

## 🔧 Scripts Utiles

| Script | Description | Commande |
|--------|-------------|----------|
| **check_compatibility.py** | Vérifier les versions | `python check_compatibility.py` |
| **regenerate_model.py** | Régénérer le modèle | `python regenerate_model.py` |
| **save_model_with_metadata.py** | Sauvegarder avec métadonnées | Importer dans votre code |
| **colab_training_template.py** | Template pour Colab | Copier dans votre notebook |

---

## ⚡ Commandes Essentielles

```bash
# Vérifier les versions installées
pip list | grep -E "tensorflow|scikit-learn|numpy"

# Installer une version spécifique
pip install tensorflow==2.19.0

# Mettre à jour requirements.txt
pip freeze > requirements.txt

# Vérifier TensorFlow
python -c "import tensorflow as tf; print(tf.__version__)"

# Lancer l'application
streamlit run app.py
```

---

## 🎓 Workflow Recommandé

### Sur Google Colab (Entraînement)
1. Vérifier les versions (voir `COLAB_LOCAL_COMPATIBILITY.md`)
2. Entraîner le modèle
3. Sauvegarder avec métadonnées (voir `colab_training_template.py`)
4. Télécharger les fichiers

### En Local (Déploiement)
1. Placer les fichiers dans `models/`
2. Vérifier la compatibilité : `python check_compatibility.py`
3. Installer les dépendances : `pip install -r requirements.txt`
4. Tester : `streamlit run app.py`

---

## ❓ FAQ Rapide

### Q: Le modèle ne se charge pas ?
**R:** Exécutez `python check_compatibility.py` pour identifier le problème.

### Q: Versions différentes entre Colab et local ?
**R:** Consultez `COLAB_LOCAL_COMPATIBILITY.md` section "Solutions".

### Q: Comment enregistrer les versions ?
**R:** Utilisez `save_model_with_metadata.py` lors de l'entraînement.

### Q: Erreur "Can't get attribute" ?
**R:** Incompatibilité scikit-learn. Régénérez : `python regenerate_model.py`

---

## 📞 Aide Supplémentaire

- **Problème de compatibilité** → `COLAB_LOCAL_COMPATIBILITY.md`
- **Gestion des versions** → `VERSION_MANAGEMENT.md`
- **Résolution d'erreurs** → `RESOLUTION_SUMMARY.md`
- **Documentation complète** → `README.md`

---

**Dernière mise à jour** : 2025-11-22  
**Statut** : ✅ Prêt pour la production
