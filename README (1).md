# SecureNLP - Traduction Sécurisée

SecureNLP est une application Streamlit qui permet de traduire un texte de l'anglais vers le français à l'aide de l'API Azure Translator, tout en assurant la sécurité des données traitées via :
- Une authentification utilisateur (admin / analyste)
- Un chiffrement du texte traduit
- Un contrôle d'accès selon les rôles
- Un système de journalisation

---

## 🌐 Fonctionnalités

- 🔑 Authentification avec `users.json`
- 🔍 Traduction EN → FR avec Azure Translator
- 🔒 Chiffrement Fernet du texte traduit
- 📃 Journalisation dans `log_access.txt`
- 🔓 Rôles :
  - `admin` : accès au texte déchiffré
  - `analyste` : accès uniquement au texte chiffré
- 📄 Téléchargement du journal depuis l'app
- 🔐 Bouton de déconnexion

---

## 📁 Structure du projet

```
secure-nlp-app/
├── app.py                 # Code principal Streamlit
├── users.json             # Utilisateurs et rôles
├── log_access.txt         # Journal d'activité (généré automatiquement)
├── requirements.txt       # Dépendances Python
└── .streamlit/
    └── secrets.toml       # Clés API Azure (optionnel)
```

---

## 🚀 Déploiement

### 1. Clonnage du projet ou uploader sur GitHub
### 2. Aller sur [streamlit.io/cloud](https://streamlit.io/cloud)
### 3. Choisir le repo GitHub
### 4. Définir le fichier à exécuter : `app.py`

### 5. Ajouter le fichier `.streamlit/secrets.toml` :
```toml
TRANSLATOR_KEY = "VOTRE_CLE"
REGION = "eastus"
```

### 6. Lancer l’app !

---

## 📊 Exemple de `users.json`
```json
{
  "scientist": {
    "password": "secure123",
    "role": "scientist"
  },
  "analyste": {
    "password": "lectureonly",
    "role": "analyste"
  }
}
```

---

## 🛡️ Sécurité

- Clé API non stockée dans le code : utilisation de `st.secrets`
- Texte traduit chiffré avec Fernet
- Accès conditionné par rôle utilisateur
- Fichier log créé et téléchargeable

---

## 🚫 Limites & Pistes futures

- La clé Fernet est générée à chaque session (non stockée)
- Intégration future possible avec Azure Key Vault pour stocker la clé
- Possibilité d'ajouter des sessions persistantes ou tokens JWT

---

## 📆 Projet éducatif SecureNLP (2025)
Projet réalisé dans le cadre du module cybersécurité IA. L'objectif était de créer un pipeline NLP sécurisé orienté traduction et conformité aux principes de sécurité :
- Confidentialité
- Contrôle d'accès
- Journalisation
