from flask import render_template, request, Response
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from flask import redirect, url_for
from setup_sql import db
import os

from controllers import app

@app.route('/')
def accueil():
    utilisateur_courrant = Utilisateur.get_by_id(1)
    if utilisateur_courrant is not None:
        if utilisateur_courrant.diete is not None:
            diet = Diete.get_by_id(utilisateur_courrant.diete)
        else :
            diet = None
        return render_template('accueil/accueil.html', utilisateur=utilisateur_courrant, diete=diet, breadcrumb=[{'title': 'Accueil', 'url': '/'}])
    else:
        return "Vous devez créer un utilisateur : <a href='/init'>Créer un utilisateur</a>"

@app.route('/init')
def init():
    db.drop_all()
    db.create_all()

    nouvel_utilisateur = Utilisateur(nom='Tempestini',
                                     prenom='Terry',
                                     mail='terry57tt@gmail.com',
                                     age=20,
                                     taille=170,
                                     poids=66,
                                     sexe='homme')

    db.session.add(nouvel_utilisateur)
    db.session.commit()

    return redirect(url_for('controllers.accueil'))

@app.route('/data_reader')
def data_reader():
    import pandas as pd

    csv = "titre,kcal,proteines,glucides,lipides,categorie,photo,description,unite\n"
    for file in os.listdir('static/excel'):
        if file.endswith('.xlsx'):
            df = pd.read_excel('static/excel/' + file, sheet_name='composition abrégée')
            obj = df.iloc[3,0]
            titre = obj.replace(',', '')
            obj_kcal = df.iloc[8,1]
            kcal = obj_kcal.replace(',', '.')
            obj_proteines = df.iloc[9,1]
            proteines = obj_proteines.replace(',', '.')
            obj_glucides = df.iloc[10,1]
            glucides = obj_glucides.replace(',', '.')
            obj_lipides = df.iloc[11,1]
            lipides = obj_lipides.replace(',', '.')
            csv += f"{titre},{kcal},{proteines},{glucides},{lipides},Autre, , ,0\n"

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                    f"attachment; filename=aliments.csv"})


