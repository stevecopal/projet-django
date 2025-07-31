## decription du projet

Projet de blog Django avec fonctionnalités de connexion, inscription, réinitialisation de mot de passe, gestion d'articles, commentaires, catégories et utilisateurs.

## Prérequis
- Python 3.12.3
- PostgreSQL
- Node.js et npm

## Installation
1. Cloner le dépôt :

   https://github.com/stevecopal/projet-django.git

   cd copalnews

Créer et activer un environnement virtuel :

python3 -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate  # Windows

Installer les dépendances Python :

pip install -r requirements.txt

Configurer la base de données PostgreSQL :

Créer une base de données blog_db.

Ajouter un fichier .env avec :

textSECRET_KEY=ta-cle-secrete

DB_NAME=blog_db

DB_USER=ton-utilisateur

DB_PASSWORD=ton-mot-de-passe

DB_HOST=localhost

DB_PORT=5432



Appliquer les migrations :

python3 manage.py makemigrations

python3 manage.py migrate

Créer un superutilisateur :

python3 manage.py create_admin

Installer les dépendances Tailwind CSS :

npm install

Compiler Tailwind CSS :

npm run build:css

Lancer le serveur :

python3 manage.py runserver

Accéder au site : http://127.0.0.1:8000

Scripts npm

npm run build:css : Compiler Tailwind CSS.

npm run watch:css : Compiler Tailwind CSS en mode surveillance.