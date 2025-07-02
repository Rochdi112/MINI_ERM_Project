# 🛠️ MINI_ERM_Project — ERP Technique pour MIF Maroc

Ce projet est un **Mini-ERP Web** développé avec Django, TailwindCSS, HTMX et WeasyPrint, conçu pour la **gestion des interventions techniques** de l’entreprise **MIF Maroc**.

---

## 📦 Fonctionnalités principales

- 🧾 Gestion des clients, techniciens, matériels
- 📅 Planification des interventions (correctives et préventives)
- 📄 Rapports d’intervention exportables en PDF
- 📊 Tableau de bord synthétique avec KPIs
- 🔒 Authentification et rôles (à implémenter)

---

## 📁 Structure du projet

```

MINI\_ERM\_Project/
├── config/              # Paramètres Django
├── core/                # Dashboard global
├── app\_clients/         # Module clients
├── app\_techniciens/     # Module techniciens
├── app\_materiels/       # Module matériels
├── app\_interventions/   # Module interventions
├── app\_rapports/        # Module rapports PDF
├── templates/           # Templates HTML (HTMX + Tailwind)
├── static/              # Fichiers CSS / JS
├── media/               # Dossiers fichiers PDF générés
├── docs/                # Documentation et captures
└── manage.py

````

---

## 🚀 Installation locale (Windows / Linux / MacOS)

```bash
git clone https://github.com/Rochdi112/MINI_ERM_Project.git
cd MINI_ERM_Project

python -m venv venv
# Windows :
venv\Scripts\activate
# Linux / Mac :
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

---

## ⚙️ Déploiement (Render ou Railway)

### 📄 Fichier `Procfile`

```
web: gunicorn config.wsgi --log-file -
```

### ✅ Dépendances déployées dans `requirements.txt`

* Django
* WeasyPrint
* Gunicorn
* Psycopg2 (si PostgreSQL utilisé)

---

## 📄 Documentation

* [`docs/manuel_utilisateur.md`](docs/manuel_utilisateur.md)
* [`docs/manuel_deploiement.md`](docs/manuel_deploiement.md)
* [`docs/captures/`](docs/captures/) — captures du dashboard, PDF, etc.

---

## 🧠 Auteur

**Rochdi Sabir** — Étudiant ingénieur DLTI (5e année)
**Projet de Fin d’Études – MIF Maroc** – 2025

---

## ✅ Statut

✅ MVP fonctionnel codé et structuré
🛠️ Préparation à la soutenance en cours
📤 Déploiement prévu sur [Render.com](https://render.com)

````

---
