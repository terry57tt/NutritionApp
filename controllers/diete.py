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

from controllers import app

@app.route('/t', methods=['GET', 'POST'])
def t():
    diete = Diete.get_by_id(1)
    return render_template('aliment/test.html', diete=diete)

@app.route('/get_filtered_data_dietes', methods=['POST'])
def get_filtered_data_dietes():
    filter_value = request.form.get('filter', '').lower()
    page_number = int(request.form.get('page', 1))
    page_size = int(request.form.get('page_size', 5))

    filtered_data = []

    dietes = Diete.search_by_titre(filter_value)
    
    for diete in dietes:
        filtered_data.append(diete.jsonformat())

    total_pages = (len(filtered_data) + page_size - 1) // page_size

    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    current_page_data = filtered_data[start_idx:end_idx]

    return jsonify(data=current_page_data, total_pages=total_pages)

@app.route('/get_filtered_data', methods=['POST'])
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
def dietes():
    dietes = Diete.get_all()
    current_date = date.today().isoformat()
    utilisateur_courrant = Utilisateur.query.filter_by(id=1).first()
    return render_template('diete/dietes.html', dietes=dietes, date=current_date, utilisateur=utilisateur_courrant)

@app.route('/ajouter_diete', methods=['GET', 'POST'])
def ajouter_diete():
    createur_id = 1
    titre = request.form['titre']
    date_today = datetime.now()
    diet = Diete(titre_diete=titre, createur=createur_id, date=date_today)
    db.session.add(diet)
    db.session.commit()
    return redirect(url_for('controllers.creer_diete', id = diet.id))

@app.route('/modifier_diete/<int:id>', methods=['GET', 'POST'])
def modifier_diete(id):
    return redirect(url_for('controllers.creer_diete', id = id))

@app.route('/supprimer_diete/<int:id>', methods=['GET', 'POST'])
def supprimer_diete(id):
    diete_courante = Diete.get_by_id(id)
    portions_liees = diete_courante.portions_associees()
    for portion in portions_liees:
        db.session.delete(portion)
    db.session.delete(diete_courante)
    db.session.commit()
    return redirect(url_for('controllers.dietes'))

@app.route('/voir_diete/<int:id>', methods=['GET', 'POST'])
def voir_diete(id):
    diet = Diete.get_by_id(id)
    return render_template('diete/detail_diete.html', root = default_root(), diete=diet)

@app.route('/change_title/<int:id>/<string:title>', methods=['GET', 'POST'])
def change_title(id, title):
    diet = Diete.get_by_id(id)
    diet.titre_diete = title
    db.session.commit()
    return redirect(url_for('controllers.dietes'))

@app.route('/changer_diete/<int:id_utilisateur>', methods=['GET', 'POST'])
def changer_diete(id_utilisateur):
    utilisateur_courrant = Utilisateur.query.filter_by(id=id_utilisateur).first()
    dietes = Diete.get_all()
    return render_template('diete/changer_diete.html', utilisateur=utilisateur_courrant, dietes=dietes)

@app.route('/choisir_diete/<int:id>/<int:id_utilisateur>', methods=['GET', 'POST'])
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
    utilisateur_courrant = Utilisateur.query.filter_by(id=1).first()
    diet = Diete.get_by_id(id_diete)
    out = render_template("diete/diete_pdf.html", root = default_root(), diete=diet, navbar=False, utilisateur=utilisateur_courrant)
    return html_to_pdf(out)

def html_to_pdf(html,filename='diete.pdf',download=False):
    pdf = pdfkit.from_string(html, False)
    response = Response(pdf, mimetype='application/pdf')
    if download :
        response.headers.set('Content-Disposition', f'attachment; filename={filename}')
    return response

@app.route('/creer_diete/<int:id>', methods=['GET', 'POST'])
def creer_diete(id):
    diete_courante = Diete.get_by_id(id)
    portions_repas = diete_courante.portions_associees()

    aliments = Aliment.get_all()
    return render_template('diete/creer_diete.html', aliments=aliments, diete=diete_courante, portions_repas=portions_repas)
 
@app.route('/ajouter_aliment_diete/<int:id_aliment>/<int:id_diete>/<int:quantite>/<int:label>', methods=['GET', 'POST'])
def ajouter_aliment_diete(id_aliment, id_diete, quantite, label):
    
    nouvelle_portion = Portion(diete=id_diete, aliment=id_aliment, nombre=quantite, label_portion=label)
    
    db.session.add(nouvelle_portion)
    db.session.commit()

    return redirect(url_for('controllers.creer_diete', id=id_diete))

@app.route('/enlever_aliment_diete/<int:id_portion>/<int:id_diete>', methods=['GET', 'POST'])
def enlever_aliment_diete(id_portion, id_diete):
    portion_courante = Portion.get_by_id(id_portion)    

    db.session.delete(portion_courante)    
    db.session.commit()

    return redirect(url_for('controllers.creer_diete', id=id_diete))

# ----------------- Export dietes ----------------- #

@app.route('/export_csv/<int:id_diete>', methods=['GET', 'POST'])
def export_csv(id_diete):
    diet = Diete.get_by_id(id_diete)
    portions = diet.portions_associees()
    csv = "Aliment,Quantité,Repas\n"
    for portion in portions:
        csv += f"{portion.aliment_obj.titre},{portion.nombre},{portion.label_portion}\n"
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                    f"attachment; filename={diet.titre_diete}.csv"})

# ----------------- Import dietes ----------------- #

@app.route('/importer_csv', methods=['POST'])
def importer_csv():
    fichier = request.files['fichier_csv']
    if fichier.filename.endswith('.csv'):
        
        df = pd.read_csv(fichier)
        nouvelle_diete = Diete(titre_diete=fichier.filename, createur=1, date=datetime.now())
        db.session.add(nouvelle_diete)
        db.session.commit()

        if 'Aliment' not in df.columns or 'Quantité' not in df.columns or 'Repas' not in df.columns:
            flash('Erreur dans le chargement du fichier : les colonnes doivent être nommées "Aliment", "Quantité" et "Repas"', 'warning')
            return redirect(url_for('controllers.dietes'))

        for index, row in df.iterrows():
            aliment_courant = Aliment.query.filter_by(titre=row['Aliment']).first()
            if aliment_courant is None:
                aliment_courant = Aliment(titre=row['Aliment'], kcal=0, proteines=0, glucides=0, lipides=0, categorie='', photo='', description='', unite=0)
                db.session.add(aliment_courant)
                db.session.commit()
            nouvelle_portion = Portion(diete=nouvelle_diete.id, aliment=aliment_courant.id, nombre=row['Quantité'], label_portion=row['Repas'])
            db.session.add(nouvelle_portion)
            db.session.commit()
        
        flash('La diète a été importée avec succès', 'success')
    else:
        flash('Erreur dans le chargement du fichier', 'danger')
        
    return redirect(url_for('controllers.dietes'))

@app.route('/envoyer_mail/<int:id_diete>', methods=['GET', 'POST'])
def envoyer_mail(id_diete):
    utilisateur_courrant = Utilisateur.query.filter_by(id=1).first()
    diet = Diete.get_by_id(id_diete)
    out = render_template("diete/diete_pdf.html", root = default_root(), diete=diet, navbar=False, utilisateur=utilisateur_courrant)
    pdf = pdfkit.from_string(out, False)

    sender_email = 'terrynutritionapp@gmail.com'
    sender_password = 'qqfpvggfqadsuxkx'
    receiver_email = utilisateur_courrant.mail

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'Diète {diet.titre_diete}'
    msg.attach(MIMEText('Bonjour,\n\nVeuillez trouver ci-joint la diète demandée.\n\nCordialement,\n\nTerry Nutrition App', 'plain'))
    
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