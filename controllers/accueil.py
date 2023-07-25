from flask import render_template, request
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from flask import redirect, url_for

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