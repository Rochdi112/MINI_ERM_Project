@echo off
echo ========================================
echo Initialisation de l'environnement Python
echo ========================================
python -m venv venv
call venv\Scripts\activate

echo =============================
echo Installation des dépendances
echo =============================
pip install --upgrade pip
pip install -r requirements.txt

echo =============================
echo Installation des packages npm
echo =============================
npm install

echo =============================
echo Compilation Tailwind CSS
echo =============================
npx tailwindcss -i ./input.css -o ./static/css/tailwind.css

echo =============================
echo Migration de la base de données
echo =============================
python manage.py makemigrations
python manage.py migrate

echo =============================
echo Lancement du serveur local
echo =============================
python manage.py runserver

pause