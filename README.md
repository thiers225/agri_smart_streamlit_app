# 🌾 AGRI-SMART — Système intelligent de prévision et de recommandation agricole basé sur l’IA et la Data Science

> **Projet académique et de recherche appliquée — Master Big Data & Intelligence Artificielle (2024–2025)**  
> Auteur : **N’DRI N’da Yao Thierry**

---

## 📘 Présentation du projet

**AGRI-SMART** est un système intelligent de prévision et de recommandation agricole basé sur l’intelligence artificielle et la science des données.  
Son objectif est de contribuer à la **productivité et à la résilience de l’agriculture ivoirienne**, à travers :

1. 🌽 **La prédiction du rendement du maïs** à partir de données agronomiques historiques  
2. 🌿 **La détection automatisée de maladies du maïs** à partir d’images de feuilles  
3. ☁️ **L’intégration cloud et IA** pour centraliser, traiter et valoriser les données agricoles

---

## 🎯 Objectifs

### 🎯 Objectif principal
> Développer un système intelligent capable d’optimiser la productivité du maïs en Côte d’Ivoire  
> grâce à l’IA, la data science et le cloud computing.

### 🧩 Objectifs spécifiques
- Déployer une **infrastructure cloud multi-source** pour le stockage et le traitement des données agricoles (Data Lakehouse + ELT)
- Développer un **modèle de prédiction du rendement** (Random Forest / XGBoost)
- Concevoir un **modèle de détection de maladies du maïs** (CNN / EfficientNet)
- Intégrer le tout dans une **application Streamlit** pour une utilisation simple et interactive

---

## 🌍 Contexte

L’agriculture représente **23 % du PIB** et **43,5 % des emplois** en Côte d’Ivoire.  
Cependant, le secteur reste vulnérable :
- aux aléas climatiques ☁️  
- aux maladies et parasites 🪲  
- et à la faible digitalisation des pratiques agricoles ⚙️  

**AGRI-SMART** s’inscrit dans la volonté de numériser ce secteur vital, en apportant une solution **locale, intelligente et open-source**.

---

## 🧠 Données utilisées

### 📊 Données tabulaires — rendement et variables agronomiques
Provenant de l’**IITA (International Institute of Tropical Agriculture)** :
- *Grain Yield and Agronomic Traits of International Maize Trials – Côte d’Ivoire (1989–1999)*
- Variables : `PL_HT`, `E_HT`, `E_HARV`, `BLIGHT`, `STRIGA`, `BORER`, `YIELD`, `CURV`

### 🖼️ Données images — détection de maladies
Dataset Kaggle :  
[📁 Corn or Maize Leaf Disease (PlantVillage/PlantDoc)](https://www.kaggle.com/code/mdismielhossenabir/corn-or-maize-leaf-disease)

| Classe | Description | Nombre d’images |
|---------|--------------|----------------|
| 🌿 Healthy | Feuilles saines | 1 162 |
| 🍂 Blight | Brûlure foliaire | 1 146 |
| 🟤 Common Rust | Rouille commune | 1 306 |
| ⚫ Gray Leaf Spot | Tache grise des feuilles | 574 |

---

## 🧮 Modélisation & résultats

### 🌽 Prédiction du rendement
| Modèle | RMSE ↓ | R² ↑ |
|---------|--------|------|
| Régression linéaire | 732.95 | 0.598 |
| Random Forest | 675.28 | 0.659 |
| **XGBoost** | **638.43** | **0.695** ✅ |

### 🦠 Détection de maladies (images)
| Modèle | Précision (%) | Rappel (%) | F1-score |
|---------|----------------|-------------|-----------|
| CNN simple | 86.4 | 85.7 | 86.0 |
| **EfficientNetB0** | **92.8** | **91.6** | **92.2** ✅ |

---

## 💻 Application Streamlit

L’application **AGRI-SMART App** est une interface interactive en deux volets :
1. 🌾 **Prédiction du rendement**
2. 🦠 **Détection de maladies (analyse d’image)**

### ⚙️ Lancer localement

```bash
# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Streamlit
cd streamlit_app
streamlit run app.py
```

➡️ **Ouvrir dans le navigateur :** [http://localhost:8501](http://localhost:8501)

## ⚙️ Technologies principales

| Domaine | Outils / Librairies |
|----------|----------------------|
| **Langage** | Python 3.12 |
| **Data** | pandas, numpy |
| **Machine Learning** | scikit-learn, XGBoost |
| **Deep Learning (images)** | TensorFlow, Keras, EfficientNet |
| **Visualisation** | matplotlib, seaborn |
| **Application Web** | Streamlit |
| **Cloud (optionnel)** | Google Cloud, GCS, Airflow |
| **Versioning** | Git & GitHub |

## 📈 Résultats attendus

- ✅ **Modèle fiable de prédiction du rendement**
- ✅ **Modèle CNN performant pour la détection de maladies**
- ✅ **Application Streamlit interactive et intuitive**
- ✅ **Documentation et pipeline reproductibles**
