from app import db
from sqlalchemy.sql import func

class aliment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=True)
    kcal = db.Column(db.Integer, nullable=True)
    proteines = db.Column(db.Integer, nullable=True)
    glucides = db.Column(db.Integer, nullable=True)
    lipides = db.Column(db.Integer, nullable=True)
    categorie = db.Column(db.String(255), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    unite = db.Column(db.Boolean, nullable=True)

class portion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))
    aliment = db.Column(db.Integer, db.ForeignKey('aliment.id'))
    nombre = db.Column(db.Integer, nullable=False, server_default='0')
    label_portion = db.Column(db.String(255), nullable=True)
    diete_obj = db.relationship('diete', backref=db.backref('portions'))
    aliment_obj = db.relationship('aliment', backref=db.backref('portions'))

class diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True)
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])
    
    def portions_associees(self):
        return portion.query.filter(portion.diete == self.id).all()

class utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=True)
    prenom = db.Column(db.String(255), nullable=True)
    mail = db.Column(db.String(255), nullable=True)
    mdp = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    taille = db.Column(db.Integer, nullable=True)
    poids = db.Column(db.Integer, nullable=True)
    sexe = db.Column(db.String(255), nullable=True)
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))

    diete_obj = db.relationship('diete', backref=db.backref('utilisateurs'), foreign_keys=[diete])

# dataset creation

'''# création des aliments
a1 = aliment(titre='Pomme', kcal=52, proteines=0.3, glucides=13.8, lipides=0.2, categorie='fruit', photo='pomme.jpg', description='La pomme est le fruit du pommier, arbre fruitier largement cultivé. L espèce la plus cultivée est Malus domestica.', unite=True)
a2 = aliment(titre='Banane', kcal=89, proteines=1.1, glucides=22.4, lipides=0.3, categorie='fruit', photo='banane.jpg', description='La banane est un fruit comestible, produit par diverses espèces de plantes herbacées de la famille des Musaceae.', unite=True)
a3 = aliment(titre='Orange', kcal=47, proteines=0.9, glucides=11.8, lipides=0.2, categorie='fruit', photo='orange.jpg', description='L orange est un agrume, fruit des orangers, des arbres de la famille des Rutaceae.', unite=True)
a4 = aliment(titre='Pain', kcal=266, proteines=8.5, glucides=50.9, lipides=1.1, categorie='feculent', photo='pain.jpg', description='Le pain est un aliment de base traditionnel de nombreuses cultures. Il se présente sous forme de miche, de miettes ou de baguette.', unite=True)

# création de la diète
d1 = diete(titre_diete='Diète Pat Sèche 2500', createur=1, date='2020-01-01')
d2 = diete(titre_diete='Diète Pat Pdm 4000', createur=1, date='2020-01-01')

# création des portions
p1 = portion(diete=1, aliment=1, nombre=1, label_portion='matin')
p2 = portion(diete=1, aliment=2, nombre=1, label_portion='matin')
p3 = portion(diete=1, aliment=3, nombre=1, label_portion='midi')
p4 = portion(diete=1, aliment=4, nombre=1, label_portion='midi')
p5 = portion(diete=1, aliment=1, nombre=1, label_portion='soir')
p6 = portion(diete=1, aliment=2, nombre=1, label_portion='soir')

p7 = portion(diete=2, aliment=1, nombre=1, label_portion='matin')
p8 = portion(diete=2, aliment=2, nombre=1, label_portion='matin')
p9 = portion(diete=2, aliment=3, nombre=1, label_portion='midi')
p10 = portion(diete=2, aliment=4, nombre=1, label_portion='midi')
p11 = portion(diete=2, aliment=1, nombre=1, label_portion='soir')
p12 = portion(diete=2, aliment=2, nombre=1, label_portion='soir')

# création de l'utilisateur terry tempestini terry57tt@gmail.com
u1 = utilisateur(nom='Tempestini', prenom='Terry', mail='terry57tt@gmail.com', mdp='terry57tt', age=21, taille=180, poids=80, sexe='homme', diete=1)

# ajout des données dans la base de données
db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.add(a4)
db.session.add(d1)
db.session.add(d2)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.add(p8)
db.session.add(p9)
db.session.add(p10)
db.session.add(p11)
db.session.add(p12)
db.session.add(u1)

db.session.commit()'''
