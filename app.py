import streamlit as st
import pandas as pd
import joblib
import os

# Charger le modèle sauvegardé pour prédire la colonne `target`
model = joblib.load('model_target_predictor(3).pkl')

# Vérification du modèle
try:
    model.classes_
    st.success("Le modèle est chargé et prêt à prédire.")
except AttributeError:
    st.error("Le modèle n'est pas ajusté. Vérifiez la sauvegarde du modèle.")

# Recommandations spécifiques aux maladies
RECOMMENDATIONS = {
    "Angina": "Évitez les efforts physiques excessifs et consultez un cardiologue.",
    "Ischemia": "Adoptez un régime pauvre en graisses saturées et en cholestérol. Consultez un spécialiste.",
    "Arrhythmia": "Surveillez votre fréquence cardiaque et évitez les stimulants comme la caféine.",
    "Hypertension": "Réduisez la consommation de sel, pratiquez une activité physique régulière, et surveillez votre tension artérielle."
}

# Fonction pour prédire les maladies spécifiques
def predict_specific_diseases(inputs):
    diseases = []
    if inputs['cp'] == 3:  # Angine
        diseases.append("Angina")
    if inputs['exang'] == 1 or inputs['oldpeak'] > 2.0:  # Ischémie
        diseases.append("Ischemia")
    if inputs['restecg'] == 1 or inputs['thalach'] < 100:  # Arythmie
        diseases.append("Arrhythmia")
    if inputs['trestbps'] > 140:  # Hypertension
        diseases.append("Hypertension")
    return diseases

# Fonction pour enregistrer les données utilisateur
def save_user_data(data, filename="user_data.csv"):
    if os.path.exists(filename):
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        updated_data = data
    updated_data.to_csv(filename, index=False)

# Initialiser l'état de l'application
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # Par défaut, commencer à l'étape 1

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = pd.DataFrame()

# Interface Streamlit
st.title("Prédiction des Maladies Cardiovasculaires")

# Étape 1 : Vérification du risque général
if st.session_state['step'] == 1:
    st.header("Étape 1 : Vérification du risque général")
    
    # Entrée des paramètres de base
    st.session_state['age'] = st.number_input("Âge", min_value=1, max_value=120, step=1)
    st.session_state['sex'] = st.selectbox("Sexe", [0, 1], format_func=lambda x: "Femme" if x == 0 else "Homme")
    st.session_state['trestbps'] = st.number_input("Pression artérielle au repos (mm Hg)", min_value=80, max_value=200, step=1)
    st.session_state['chol'] = st.number_input("Cholestérol sérique (mg/dl)", min_value=100, max_value=400, step=1)
    st.session_state['thalach'] = st.number_input("Fréquence cardiaque maximale", min_value=50, max_value=250, step=1)
    st.session_state['fbs'] = st.selectbox("Glycémie à jeun > 120 mg/dl ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
    
    if st.button("Vérifier le risque"):
        # Préparation des données pour la prédiction
        input_data = pd.DataFrame([{
            'age': st.session_state['age'], 
            'sex': st.session_state['sex'], 
            'trestbps': st.session_state['trestbps'],
            'chol': st.session_state['chol'], 
            'thalach': st.session_state['thalach'], 
            'fbs': st.session_state['fbs']
        }])
        risk_prediction = model.predict(input_data)[0]

        if risk_prediction == 0:
            st.success("Vous n'avez pas de risque de maladie cardiovasculaire.")
        else:
            st.warning("Risque détecté ! Passons à l'étape 2.")
            st.session_state['step'] = 2  # Passer à l'étape 2

# Étape 2 : Identification des maladies spécifiques
if st.session_state['step'] == 2:
    st.header("Étape 2 : Identification des maladies spécifiques")
    
    # Entrée des paramètres spécifiques
    cp = st.selectbox("Type de douleur thoracique", [0, 1, 2, 3])
    restecg = st.selectbox("Résultat de l'ECG au repos", [0, 1, 2])
    exang = st.selectbox("Angine induite par exercice ?", [0, 1], format_func=lambda x: "Non" if x == 0 else "Oui")
    oldpeak = st.number_input("Dépression ST", min_value=0.0, max_value=10.0, step=0.1)
    
    if st.button("Identifier les maladies spécifiques"):
        # Identification des maladies spécifiques
        diseases = predict_specific_diseases({
            'cp': cp, 
            'restecg': restecg, 
            'exang': exang,
            'oldpeak': oldpeak, 
            'trestbps': st.session_state['trestbps'], 
            'thalach': st.session_state['thalach']
        })
        st.subheader("Maladies potentielles :")
        for disease in diseases:
            st.write(f"- {disease}: {RECOMMENDATIONS[disease]}")
        
        # Demande de consentement pour enregistrer les données
        consent = st.radio(
            "Acceptez-vous d'enregistrer vos données pour des recherches futures ?",
            ('Oui', 'Non')
        )
        if consent == 'Oui':
            user_data = pd.DataFrame([{
                'age': st.session_state['age'], 
                'sex': st.session_state['sex'], 
                'trestbps': st.session_state['trestbps'],
                'chol': st.session_state['chol'], 
                'thalach': st.session_state['thalach'], 
                'fbs': st.session_state['fbs'],
                'cp': cp,
                'restecg': restecg,
                'exang': exang,
                'oldpeak': oldpeak,
                'diseases': ", ".join(diseases)
            }])
            save_user_data(user_data)
            st.success("Vos données ont été enregistrées avec succès !")
        else:
            st.info("Vos données n'ont pas été enregistrées.")
