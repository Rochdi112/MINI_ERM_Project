# Manuel de Déploiement – MINI_ERM_Project

## 📦 Prérequis
- Python 3.10+
- Node.js & npm
- PostgreSQL ou SQLite
- WeasyPrint installé

## 🚀 Déploiement sur Render (ou Railway)

### 1. Fichiers nécessaires
- `Procfile` : contient
```
web: gunicorn config.wsgi --log-file -
```

### 2. Variables d’environnement
- `DJANGO_SECRET_KEY`
- `DEBUG=FALSE`
- `ALLOWED_HOSTS=*`
- `DATABASE_URL` si PostgreSQL

### 3. Build command
```bash
pip install -r requirements.txt
python manage.py migrate
npm install
npx tailwindcss -i ./input.css -o ./static/css/tailwind.css
```

### 4. Commande de lancement
```bash
gunicorn config.wsgi
```

## 🔁 MAJ continue (CI/CD)
- GitHub Actions peut être configuré (optionnel)

---

**Remarque :** Pour environnement local, utilisez `python manage.py runserver`.