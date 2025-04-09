import streamlit as st
import json
import requests
import uuid
from cryptography.fernet import Fernet
from datetime import datetime
import hashlib

# Configuration Azure Translator
TRANSLATOR_KEY = "lyxdTbUg0rOF3LUigJrNkiWCAXmpRn5fEPpFR44gFlBx99a5sxDhJQQJ99BDACYeBjFXJ3w3AAAbACOGoB63"
REGION = "eastus"
ENDPOINT = "https://api.cognitive.microsofttranslator.com"

# Chargement des utilisateurs
@st.cache_data
def charger_utilisateurs():
    with open("users.json") as f:
        return json.load(f)

# Journalisation
def log_event(event):
    with open("log_access.txt", "a") as f:
        f.write(f"{datetime.now()} - {event}\n")

# Authentification simple
def verifier_utilisateur(users, username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None

# Traduction Azure
def traduire_texte(text):
    path = '/translate?api-version=3.0'
    params = '&from=en&to=fr'
    url = ENDPOINT + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]['translations'][0]['text']

# Interface Streamlit
st.set_page_config(page_title="SecureNLP", page_icon="🔒")
st.title("🔒 SecureNLP - Traduction Sécurisée")

users = charger_utilisateurs()

# Connexion
with st.sidebar:
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    authentifie = st.button("Se connecter")

if "connected" not in st.session_state:
    st.session_state.connected = False

if authentifie:
    role = verifier_utilisateur(users, username, password)
    if role:
        st.session_state.connected = True
        st.session_state.username = username
        st.session_state.role = role
        st.success(f"Connecté en tant que {username} ({role})")
    else:
        st.error("❌ Identifiants invalides")

if st.session_state.connected:
    st.subheader("🌐 Entrez votre texte en anglais :")
    texte_en = st.text_area("Texte à traduire")
    if st.button("Traduire") and texte_en:
        try:
            texte_fr = traduire_texte(texte_en)
            key = Fernet.generate_key()
            cipher = Fernet(key)
            texte_chiffre = cipher.encrypt(texte_fr.encode()).decode()

            log_event(f"{st.session_state.username} | Traduction | Texte: {texte_en}")

            st.success("📔 Traduction effectuée")
            st.text("Texte chiffré :")
            st.code(texte_chiffre, language="text")

            if st.session_state.role == "scientist":
                texte_dechiffre = cipher.decrypt(texte_chiffre.encode()).decode()
                st.text("Texte déchiffré :")
                st.success(texte_dechiffre)
            else:
                st.info("Seuls les scientist peuvent voir le texte déchiffré.")
        except Exception as e:
            st.error(f"Erreur : {e}")

    # 🔗 Téléchargement du journal log_access.txt
    st.divider()
    with open("log_access.txt", "r") as file:
        st.download_button(
            label="💾 Télécharger le journal des accès",
            data=file.read(),
            file_name="log_access.txt",
            mime="text/plain"
        )
