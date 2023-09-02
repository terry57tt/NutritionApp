from flask import render_template, request, Response
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from flask import redirect, url_for
from setup_sql import db
from datetime import date

from controllers import app

@app.route('/suivi', methods=['GET', 'POST'])
def suivi():
    utilisateur_courrant = Utilisateur.get_by_id(1)
    today = date.today().isoformat()
    return render_template('suivi/suivi.html', utilisateur=utilisateur_courrant, today=today)