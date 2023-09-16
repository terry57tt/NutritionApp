from flask import render_template, request, Response
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from flask import redirect, url_for
from setup_sql import db
from datetime import date
from flask_login import login_required, current_user
from models.Suivi import Suivi

from controllers import app

@app.route('/suivi', methods=['GET', 'POST'])
@login_required
def suivi():
    today = date.today().isoformat()
    suivis = Suivi.filter_by_personne(current_user.id)
    return render_template('suivi/suivi.html', utilisateur=current_user, today=today, suivis=suivis)

@app.route('/ajouter_suivi', methods=['GET', 'POST'])
@login_required
def ajouter_suivi():
    if request.method == 'POST':
        date = request.form['date']
        poids = request.form['poids']        
        taux_masse_grasse = request.form['taux_masse_grasse']
        bras = request.form['bras']
        epaules = request.form['epaules']
        poitrine = request.form['poitrine']
        tour_taille = request.form['tour_taille']
        cuisses = request.form['cuisses']
        mollets = request.form['mollets']

        suivi = Suivi.filter_by_date_and_personne(date, current_user.id)
        if suivi:
            new_suivi = suivi[0]
            new_suivi.poids = poids
            if taux_masse_grasse:
                new_suivi.taux_masse_grasse = taux_masse_grasse
            if tour_taille:
                new_suivi.tour_taille = tour_taille
            if cuisses:
                new_suivi.cuisses = cuisses
            if mollets:
                new_suivi.mollets = mollets
            if bras:
                new_suivi.bras = bras
            if epaules:
                new_suivi.epaules = epaules
            if poitrine:
                new_suivi.poitrine = poitrine
        else:
            suivi = Suivi(date=date, poids=poids, taux_masse_grasse=taux_masse_grasse, bras=bras, epaules=epaules, poitrine=poitrine, tour_taille=tour_taille, cuisses=cuisses, mollets=mollets, personne=current_user.id)
            db.session.add(suivi)
        db.session.commit()
    return redirect(url_for('controllers.suivi'))