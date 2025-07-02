@echo off
SETLOCAL
echo [🔧] Vérification du projet Django MINI_ERM_Project...

:: Activation de l'environnement virtuel
echo [🐍] Activation de l'environnement Python...
call venv\Scripts\activate

:: Vérification des dépendances
echo [📦] Installation des dépendances...
pip install -r requirements.txt

:: Migrations
echo [🔁] Application des migrations...
python manage.py migrate

:: Lancement des tests automatiques
echo [🧪] Lancement des tests unitaires...
python manage.py test tests/

:: Lancement du serveur local
echo [🚀] Lancement du serveur local...
start http://127.0.0.1:8000/
python manage.py runserver

ENDLOCAL
pause
