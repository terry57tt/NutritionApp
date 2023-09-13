from flask import render_template, request, Response
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from flask import redirect, url_for
from setup_sql import db
from datetime import date
from flask_login import login_required, current_user

from controllers import app

@app.route('/suivi', methods=['GET', 'POST'])
@login_required
def suivi():
    utilisateur_courrant = current_user
    today = date.today().isoformat()
    return render_template('suivi/suivi.html', utilisateur=utilisateur_courrant, today=today)