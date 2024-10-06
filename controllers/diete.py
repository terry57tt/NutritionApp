from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from models.Utilisateur import Utilisateur
from models.Diete import Diete
from models.Aliment import Aliment
from models.Portion import Portion
from datetime import datetime, date
from setup_sql import db
import pdfkit
from urllib.parse import urlparse
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_login import login_required, current_user
from fuzzywuzzy import process
import re
from controllers import app


@app.route('/get_filtered_data_dietes', methods=['POST'])
@login_required
def get_filtered_data_dietes():
    filter_value = request.form.get('filter', '').lower()
    page_number = int(request.form.get('page', 1))
    page_size = int(request.form.get('page_size', 5))

    filtered_data = []

    dietes = Diete.search_by_titre(filter_value)

    dietes_sorted = sorted(dietes, key=lambda x: x.date, reverse=True)

    for diete in dietes_sorted:
        filtered_data.append(diete.jsonformat())

    total_pages = (len(filtered_data) + page_size - 1) // page_size

    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    current_page_data = filtered_data[start_idx:end_idx]

    return jsonify(data=current_page_data, total_pages=total_pages)



@app.route('/get_filtered_data', methods=['POST'])
@login_required
def get_filtered_data():
    filter_value = request.form.get('filter', '').lower()
    selected_categorie = request.form.get('selected_category', '')
    page_number = int(request.form.get('page', 1))
    page_size = int(request.form.get('page_size', 5))

    filtered_data = []

    aliments = Aliment.search_by_titre_and_categorie(filter_value, selected_categorie)

    for aliment in aliments:
        filtered_data.append(aliment.jsonformat())

    # Calculer le nombre total de pages
    total_pages = (len(filtered_data) + page_size - 1) // page_size

    # Récupérer les éléments de la page actuelle
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    current_page_data = filtered_data[start_idx:end_idx]

    # Renvoyer les données filtrées et le nombre total de pages sous forme de réponse JSON
    return jsonify(data=current_page_data, total_pages=total_pages)


@app.route('/dietes')
@login_required
def dietes():
    dietes = Diete.get_all()
    current_date = date.today().isoformat()
    return render_template('diete/dietes.html', dietes=dietes, date=current_date, utilisateur=current_user)


@app.route('/ajouter_diete', methods=['GET', 'POST'])
@login_required
def ajouter_diete():
    titre = request.form['titre']
    date_today = datetime.now()
    diet = Diete(titre_diete=titre, createur=current_user.id, date=date_today)
    db.session.add(diet)
    db.session.commit()
    return redirect(url_for('controllers.creer_diete', id=diet.id))


@app.route('/modifier_diete/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_diete(id):
    return redirect(url_for('controllers.creer_diete', id=id))


@app.route('/supprimer_diete/<int:id>', methods=['GET', 'POST'])
@login_required
def supprimer_diete(id):
    diete_courante = Diete.get_by_id(id)
    portions_liees = diete_courante.portions_associees()
    for portion in portions_liees:
        db.session.delete(portion)
    db.session.delete(diete_courante)
    db.session.commit()
    return redirect(url_for('controllers.dietes'))


@app.route('/voir_diete/<int:id>', methods=['GET', 'POST'])
@login_required
def voir_diete(id):
    diet = Diete.get_by_id(id)

    return render_template('diete/detail_diete.html', root=default_root(), diete=diet)


@app.route('/change_title/<int:id>/<string:title>', methods=['GET', 'POST'])
@login_required
def change_title(id, title):
    diet = Diete.get_by_id(id)
    diet.titre_diete = title
    db.session.commit()
    return redirect(url_for('controllers.dietes'))


@app.route('/changer_diete/<int:id_utilisateur>', methods=['GET', 'POST'])
@login_required
def changer_diete(id_utilisateur):
    utilisateur_courrant = Utilisateur.query.filter_by(id=id_utilisateur).first()
    dietes = Diete.get_all()
    return render_template('diete/changer_diete.html', utilisateur=utilisateur_courrant, dietes=dietes)


@app.route('/choisir_diete/<int:id>/<int:id_utilisateur>', methods=['GET', 'POST'])
@login_required
def choisir_diete(id, id_utilisateur):
    utilisateur_courrant = Utilisateur.query.filter_by(id=id_utilisateur).first()
    utilisateur_courrant.diete = id
    db.session.commit()
    return redirect(url_for('controllers.accueil'))


def default_root():
    parsed_url = urlparse(request.url)
    return parsed_url.scheme + "://" + parsed_url.netloc


@app.route('/print_diete_pdf/<int:id_diete>', methods=['GET', 'POST'])
def print_diete_pdf(id_diete):
    diet = Diete.get_by_id(id_diete)
    out = render_template("diete/diete_pdf.html", root=default_root(), diete=diet, navbar=False,
                          utilisateur=current_user)
    return html_to_pdf(out)


def html_to_pdf(html, filename='diete.pdf', download=False):
    css = ['static/css/pages.css']
    pdf = pdfkit.from_string(html, css=css)
    response = Response(pdf, mimetype='application/pdf')
    if download:
        response.headers.set('Content-Disposition', f'attachment; filename={filename}')
    return response


@app.route('/creer_diete/<int:id>', methods=['GET', 'POST'])
@login_required
def creer_diete(id):
    diete_courante = Diete.get_by_id(id)
    portions_repas = diete_courante.portions_associees()

    aliments = Aliment.get_all()
    return render_template('diete/creer_diete.html', aliments=aliments, diete=diete_courante,
                           portions_repas=portions_repas, user=current_user)


@app.route('/ajouter_aliment_diete/<int:id_aliment>/<int:id_diete>/<int:quantite>/<int:labels>',
           methods=['GET', 'POST'])
@login_required
def ajouter_aliment_diete(id_aliment, id_diete, quantite, labels):
    label_tab = []
    while labels > 0:
        label_tab.append(labels % 10)
        labels = labels // 10

    for label in label_tab:
        nouvelle_portion = Portion(diete=id_diete, aliment=id_aliment, nombre=quantite, label_portion=label)
        db.session.add(nouvelle_portion)

    db.session.commit()

    return redirect(url_for('controllers.creer_diete', id=id_diete))


@app.route('/update_quantity/<int:id_portion>/<int:new_quantity>', methods=['GET', 'POST'])
@login_required
def update_quantity(id_portion, new_quantity):
    portion_courante = Portion.get_by_id(id_portion)
    portion_courante.nombre = new_quantity

    db.session.commit()

    return redirect(url_for('controllers.creer_diete', id=portion_courante.diete))


@app.route('/enlever_aliment_diete/<int:id_portion>/<int:id_diete>', methods=['GET', 'POST'])
@login_required
def enlever_aliment_diete(id_portion, id_diete):
    portion_courante = Portion.get_by_id(id_portion)

    db.session.delete(portion_courante)
    db.session.commit()

    return redirect(url_for('controllers.creer_diete', id=id_diete))


# ----------------- Export dietes ----------------- #

@app.route('/export_csv/<int:id_diete>', methods=['GET', 'POST'])
@login_required
def export_csv(id_diete):
    diet = Diete.get_by_id(id_diete)
    portions = diet.portions_associees()
    csv = "Aliment;Quantite;Repas\n"
    for portion in portions:
        csv += f"{portion.aliment_obj.titre};{portion.nombre};{portion.label_portion}\n"
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     f"attachment; filename={diet.titre_diete}.csv"})


# ----------------- Import dietes ----------------- #

@app.route('/importer_csv', methods=['POST'])
@login_required
def importer_csv():
    # Vérifier que le fichier a été envoyé
    if 'fichier_csv' not in request.files:
        return jsonify({'success': False, 'message': 'Aucun fichier n\'a été envoyé'})
    fichier_csv = request.files['fichier_csv']

    # Vérifier que le fichier est un fichier CSV valide
    if fichier_csv.filename == '':
        return jsonify({'success': False, 'message': 'Aucun fichier n\'a été sélectionné'})

    if fichier_csv.filename.endswith('.csv'):
        df = pd.read_csv(fichier_csv, delimiter=';', encoding='latin1')

        # Vérifier que les colonnes du fichier sont nommées correctement
        if 'Aliment' not in df.columns and 'Quantite' not in df.columns and 'Repas' not in df.columns:
            flash('Erreur dans le chargement du fichier : les colonnes doivent être nommées : Aliment;Quantite;Repas',
                  'danger')
            return jsonify({'success': False,
                            'message': 'Erreur dans le chargement du fichier : les colonnes doivent être nommées : Aliment;Quantite;Repas'})

        # Créer un dictionnaire des aliments existants (titre + id)
        all_aliments = {aliment.titre: aliment for aliment in Aliment.query.all()}

        list_aliments_import = []

        # Pour chaque ligne du fichier, extraire les 3 aliments les plus similaires
        try:
            for index, row in df.iterrows():
                # Si la dernière colonne est vide, cela peut indiquer un mauvais délimiteur
                if pd.isnull(row.iloc[-1]):
                    flash('Erreur dans la lecture de la ligne ' + str(index + 1) + ' : vérifiez le délimiteur',
                          'danger')
                    return jsonify({'success': False, 'message': 'Erreur dans la lecture de la ligne ' + str(
                        index + 1) + ' : vérifiez le délimiteur'})

                # traitement de la colonne 'Quantite'
                # Extraction de la partie numérique de la colonne 'Quantité'
                quantity = str(row['Quantite'])

                numeric_quantity = re.findall(r'\d+\.?\d*', quantity)

                # Si des chiffres sont trouvés, prenez le premier, sinon mettez 0
                if numeric_quantity:
                    numeric_quantity = float(numeric_quantity[0])
                else:
                    numeric_quantity = 0

                # extract 3 most similar aliments
                suggestions = process.extractBests(row['Aliment'], all_aliments.keys(), limit=3)
                list_aliments_import.append(
                    {'aliment': row['Aliment'], 'quantite': numeric_quantity, 'repas': row['Repas'],
                     'suggestions': suggestions})
            return jsonify({'success': True, 'message': 'La diète a été importée avec succès',
                            'liste_aliments': list_aliments_import})
        except Exception as e:
            flash('Erreur dans le chargement du fichier : ' + str(e), 'danger')
            return jsonify({'success': False, 'message': 'Erreur dans le chargement du fichier'})
    else:
        flash('Erreur dans le chargement du fichier : le fichier doit être au format CSV', 'danger')
        return jsonify({'success': True, 'message': 'Erreur dans le chargement du fichier'})


@app.route('/store_diet', methods=['POST'])
@login_required
def store_diet():
    data = request.get_json()  # Use request.get_json() to parse the request data as JSON
    diet_title = data['diet_title']
    aliments = data['aliments']

    nouvelle_diete = Diete(titre_diete=diet_title, createur=current_user.id, date=datetime.now())
    db.session.add(nouvelle_diete)
    db.session.commit()

    for aliment in aliments:
        nouvelle_portion = Portion(
            diete=nouvelle_diete.id,
            aliment=Aliment.query.filter_by(titre=aliment['suggestion']).first().id,
            nombre=aliment['quantite'],
            label_portion=aliment['repas_number']
        )
        db.session.add(nouvelle_portion)

    db.session.commit()

    flash('La diète \"' + diet_title + '\" a été importée avec succès', 'success')
    # Return a JSON object instead of redirecting the user
    return jsonify({'success': True, 'message': 'La diète a été importée avec succès'})


# ----------------- Envoyer dietes ----------------- #
@app.route('/envoyer_mail/<int:id_diete>', methods=['GET', 'POST'])
def envoyer_mail(id_diete):
    diet = Diete.get_by_id(id_diete)
    out = render_template("diete/diete_pdf.html", root=default_root(), diete=diet, navbar=False,
                          utilisateur=current_user)
    pdf = pdfkit.from_string(out, False)

    sender_email = 'terrynutritionapp@gmail.com'
    sender_password = 'qqfpvggfqadsuxkx'
    receiver_email = current_user.mail

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'Diète {diet.titre_diete}'
    msg.attach(
        MIMEText('Bonjour,\n\nVeuillez trouver ci-joint la diète demandée.\n\nCordialement,\n\nTerry Nutrition App',
                 'plain'))

    pdf_attachment = MIMEBase('application', 'octet-stream')
    pdf_attachment.set_payload(pdf)
    encoders.encode_base64(pdf_attachment)
    pdf_attachment.add_header('Content-Disposition', f'attachment; filename=diete.pdf')
    msg.attach(pdf_attachment)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)

    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    flash('La diète a été envoyée par mail avec succès à ' + receiver_email, 'success')
    return redirect(url_for('controllers.accueil'))
