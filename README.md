# <img title="NutritionApp logo" alt="Logo de NutritionApp" src="./.res-readme/logo_app.svg" style="height: 65px; width: 65px; vertical-align: middle" width="65" height="65" >Projet de gestion des programmes alimentaires 

## NutritionApp

**Créateur** :  
TEMPESTINI Terry <<terry57tt@gmail.com>>  

## Description du projet

**Application Web** qui permet de gérer ses **programmes alimentaires**, de suivres ses **calories** et ses **macros**.

## Installation du projet
Au root du projet veuillez effectuer ces commandes pour installer et lancer l'application
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

## De temps en temps
```bash
pip freeze > requirements.txt
```

## Lancement du projet
Après avoir installé le projet vous pouvez le lancer en étant au root du projet avec
```bash
source venv/bin/activate
export FLASK_APP=setup_flask
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

## Lancement des tests
Dans le root du projet :
```bash
source venv/bin/activate
pytest
```
