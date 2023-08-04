from flask import render_template, request, redirect, url_for, flash, Response
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from models.Aliment import Aliment
from datetime import datetime, date
from setup_sql import db, UPLOAD_FOLDER
import pdfkit
from urllib.parse import urlparse
import pandas as pd
import os
import uuid

from controllers import app

@app.route('/aliments')
def aliments():
    aliments = Aliment.get_all()
    return render_template('aliment/aliments.html', aliments=aliments)

@app.route('/ajouter_aliment', methods=['GET', 'POST'])
def ajouter_aliment():
    if request.method == 'POST':

        new_aliment = Aliment()

        titre = request.form['titre']
        kcal = int(request.form['kcal']) if request.form['kcal'] else None
        proteines = int(request.form['proteines']) if request.form['proteines'] else None
        glucides = int(request.form['glucides']) if request.form['glucides'] else None
        lipides = int(request.form['lipides']) if request.form['lipides'] else None
        categorie = request.form['categorie']

        photo = ''
        fichier = request.files['fichier_photo']
        if fichier.filename != '':
            if fichier.filename.endswith(('.jpg', '.jpeg', '.png')):  # Utilisez tuple pour les extensions valides

                unique_id = str(uuid.uuid4().hex)
                extension = os.path.splitext(fichier.filename)[1]
                nouveau_nom_fichier = f"{unique_id}{extension}"
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                path = os.path.join(UPLOAD_FOLDER, nouveau_nom_fichier)
                fichier.save(path)
                photo = nouveau_nom_fichier
            else :
                flash('Erreur dans le chargement de la photo (formats jpg, jpeg ou png uniquement)', 'danger')

        description = request.form['description']
        unite = request.form['unite']

        new_aliment.titre = titre
        new_aliment.kcal = kcal
        new_aliment.proteines = proteines
        new_aliment.glucides = glucides
        new_aliment.lipides = lipides
        new_aliment.categorie = categorie
        new_aliment.photo = photo
        new_aliment.description = description
        new_aliment.unite = unite

        db.session.add(new_aliment)
        db.session.commit()

        flash('L\'aliment a été ajouté avec succès', 'success')
        return redirect('/aliments')

    return render_template('ajouter_aliment.html')

@app.route('/modifier_aliment/<int:id>', methods=['GET', 'POST'])
def modifier_aliment(id):
    aliment_courant = Aliment.get_by_id(id)
    return render_template('aliment/modifier_aliment.html', aliment=aliment_courant)

@app.route('/modifier_aliment_post/<int:id>', methods=['GET', 'POST'])
def modifier_aliment_post(id):
    aliment_courant = Aliment.get_by_id(id)
    if request.method == 'POST':
        aliment_courant.titre = request.form['titre']
        aliment_courant.kcal = int(request.form['kcal']) if request.form['kcal'] else None
        aliment_courant.proteines = int(request.form['proteines']) if request.form['proteines'] else None
        aliment_courant.glucides = int(request.form['glucides']) if request.form['glucides'] else None
        aliment_courant.lipides = int(request.form['lipides']) if request.form['lipides'] else None
        aliment_courant.categorie = request.form['categorie']
        fichier = request.files['fichier_photo']

        if fichier.filename != '':
            if fichier.filename.endswith(('.jpg', '.jpeg', '.png')):  # Utilisez tuple pour les extensions valides
                if os.path.exists(os.path.join(UPLOAD_FOLDER, aliment_courant.photo)):
                    os.remove(os.path.join(UPLOAD_FOLDER, aliment_courant.photo))

                unique_id = str(uuid.uuid4().hex)
                extension = os.path.splitext(fichier.filename)[1]
                nouveau_nom_fichier = f"{unique_id}{extension}"
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                path = os.path.join(UPLOAD_FOLDER, nouveau_nom_fichier)
                fichier.save(path)
                aliment_courant.photo = nouveau_nom_fichier
            else :
                flash('Erreur dans le chargement de la photo (formats jpg, jpeg ou png uniquement)', 'danger')

        aliment_courant.description = request.form['description']
        aliment_courant.unite = request.form['unite']

        db.session.commit()

        flash('L\'aliment a été modifié avec succès', 'success')
        return redirect(url_for('controllers.aliments'))

    return render_template('aliment/modifier_aliment.html', aliment=aliment_courant)

@app.route('/supprimer_aliment/<int:id>', methods=['GET', 'POST'])
def supprimer_aliment(id):
    Aliment.get_by_id(id).delete()
    db.session.commit()
    return redirect(url_for('controllers.aliments'))

@app.route('/valider_aliment/<int:id>', methods=['GET', 'POST'])
def valider_aliment(id):
    aliment_courant = Aliment.get_by_id(id)
    aliment_courant.valide = 1
    db.session.commit()
    return redirect(url_for('controllers.aliments'))

@app.route('/invalider_aliment/<int:id>', methods=['GET', 'POST'])
def invalider_aliment(id):
    aliment_courant = Aliment.get_by_id(id)
    aliment_courant.valide = 0
    db.session.commit()
    return redirect(url_for('controllers.aliments'))

# ----------------- Export aliments ----------------- #

@app.route('/export_csv_aliment', methods=['GET', 'POST'])
def export_csv_aliment():
    aliments = Aliment.get_all()
    csv = "titre,kcal,proteines,glucides,lipides,categorie,photo,description,unite\n"
    for aliment_courant in aliments:
        csv += f"{aliment_courant.titre},{aliment_courant.kcal},{aliment_courant.proteines},{aliment_courant.glucides},{aliment_courant.lipides},{aliment_courant.categorie},{aliment_courant.photo},{aliment_courant.description},{aliment_courant.unite}\n"
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                    f"attachment; filename=aliments.csv"})

# ----------------- Import aliments ----------------- #

@app.route('/importer_csv_aliment', methods=['POST'])
def importer_csv_aliment():
    fichier = request.files['fichier_aliment']
    if fichier.filename.endswith('.csv'):
        df = pd.read_csv(fichier)

        if 'titre' not in df.columns or 'kcal' not in df.columns or 'proteines' not in df.columns or 'glucides' not in df.columns or 'lipides' not in df.columns or 'categorie' not in df.columns or 'photo' not in df.columns or 'description' not in df.columns or 'unite' not in df.columns:
            flash('Erreur dans le chargement du fichier : les colonnes doivent être nommées "titre", "kcal", "proteines", "glucides", "lipides", "categorie", "photo", "description" et "unite"', 'warning')
            return redirect(url_for('controllers.aliments'))

        for index, row in df.iterrows():
            aliment_courant = Aliment.query.filter_by(titre=row['titre']).first()
            
            try:
                if aliment_courant is None:
                    aliment_courant = Aliment(titre=row['titre'], kcal=round(float(row['kcal']), 0), proteines=round(float(row['proteines']), 0), glucides=round(float(row['glucides']), 0), lipides=round(float(row['lipides']), 0), categorie=row['categorie'], photo=row['photo'], description=row['description'], unite=row['unite'])
                    db.session.add(aliment_courant)
                else:
                    aliment_courant.titre=row['titre']
                    aliment_courant.kcal=round(float(row['kcal']), 0)
                    aliment_courant.proteines=round(float(row['proteines']), 0)
                    aliment_courant.glucides=round(float(row['glucides']), 0)
                    aliment_courant.lipides=round(float(row['lipides']), 0)
                    aliment_courant.categorie=row['categorie']
                    aliment_courant.photo=row['photo']
                    aliment_courant.description=row['description']
                    aliment_courant.unite=row['unite']
            except:
                flash('Erreur dans la lecture du fichier : ' + row['titre'] + ' (voir ligne ' + str(index + 2) + ')', 'danger')
                return redirect(url_for('controllers.aliments'))
        db.session.commit()

        flash('Les aliments ont été importés avec succès', 'success')
    else:
        flash('Erreur dans le chargement du fichier', 'danger')
    return redirect(url_for('controllers.aliments'))