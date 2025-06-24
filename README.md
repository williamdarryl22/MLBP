❤️ Prédiction des Maladies Cardiovasculaires avec IA



🧠 Description du projet

Ce projet est une application web interactive construite avec Streamlit qui permet de :

    Évaluer le risque général de maladie cardiovasculaire via un modèle pré-entraîné de classification.

    Identifier les maladies spécifiques probables (ex : angine, ischémie, arythmie, hypertension).

    Fournir des recommandations médicales adaptées.

    Proposer un système de consentement pour enregistrer les données dans un but de recherche future.

L'objectif est de fournir une aide à la prévention, intuitive et pédagogique, fondée sur des données cliniques simples.
📊 Fonctionnalités
✅ Étape 1 : Prédiction du risque général

    Saisie de 6 variables clés (âge, sexe, cholestérol, tension…)

    Prédiction avec un modèle scikit-learn embarqué (joblib)

    Alerte de risque et transition vers l’étape suivante

✅ Étape 2 : Détection de maladies spécifiques

    Analyse ciblée (douleur thoracique, ECG, fréquence cardiaque…)

    Détection multi-pathologies (Angina, Ischemia, Arrhythmia, Hypertension)

    Conseils personnalisés et enregistrement facultatif des données

🛠️ Technologies utilisées
Composant	Description
Streamlit	Framework d’interface web Python
Scikit-learn	Modèle de classification pré-entraîné
Joblib	Sérialisation du modèle ML
Pandas	Manipulation des données
CSV	Stockage local des données utilisateur
Session_state	Gestion de l'état multi-étapes
📂 Structure du projet

📁 project/
├── app.py                   # Script principal Streamlit
├── model_target_predictor(3).pkl  # Modèle ML pré-entraîné
├── user_data.csv            # (optionnel) Base de données utilisateur
├── README.md                # Ce fichier !

🚀 Lancer l'application

streamlit run app.py

🔒 Respect de la vie privée

Les données sont enregistrées localement et uniquement avec le consentement explicite de l’utilisateur. Elles ne sont utilisées que dans un objectif de recherche.
🧬 Auteurs & Contributions

👨‍💻 Darryl Towa
Étudiant Data Scientist – Datasimplifai
LinkedIn
📌 Prochaines améliorations

    ➕ Intégration d’un système de score global par pathologie

    📉 Ajout de visualisations explicatives (ex : courbes ECG, graphiques)

    🌐 Déploiement sur Streamlit Cloud ou Hugging Face Spaces
