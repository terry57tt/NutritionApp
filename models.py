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

class repas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)
    label = db.Column(db.String(255), nullable=True)

    def portions_associees(self):
        return portion.query.join(aliment).filter(portion.repas == self.id).all()

class portion(db.Model):
    repas = db.Column(db.Integer, db.ForeignKey('repas.id'), primary_key=True)
    aliment = db.Column(db.Integer, db.ForeignKey('aliment.id'), primary_key=True)
    nombre = db.Column(db.Integer, nullable=False, server_default='0')
    repas_obj = db.relationship('repas', backref=db.backref('portions'))
    aliment_obj = db.relationship('aliment', backref=db.backref('portions'))

class diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True)
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])

    def repas_associes(self):
        return repas.query.join(estCompose).filter(estCompose.diete == self.id).all()

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

class estCompose(db.Model):
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'), primary_key=True)
    repas = db.Column(db.Integer, db.ForeignKey('repas.id'), primary_key=True)

    diete_obj = db.relationship('diete', backref=db.backref('est_composes'), foreign_keys=[diete])
    repas_obj = db.relationship('repas', backref=db.backref('est_composes'), foreign_keys=[repas])

# dataset creation

'''# création des aliments
a1 = aliment(titre='Pomme', kcal=52, proteines=0.3, glucides=13.8, lipides=0.2, categorie='fruit', photo='pomme.jpg', description='La pomme est le fruit du pommier, arbre fruitier largement cultivé. L espèce la plus cultivée est Malus domestica.', unite=True)
a2 = aliment(titre='Banane', kcal=89, proteines=1.1, glucides=22.4, lipides=0.3, categorie='fruit', photo='banane.jpg', description='La banane est un fruit comestible, produit par diverses espèces de plantes herbacées de la famille des Musaceae.', unite=True)
a3 = aliment(titre='Orange', kcal=47, proteines=0.9, glucides=11.8, lipides=0.2, categorie='fruit', photo='orange.jpg', description='L orange est un agrume, fruit des orangers, des arbres de la famille des Rutaceae.', unite=True)
a4 = aliment(titre='Pain', kcal=266, proteines=8.5, glucides=50.9, lipides=1.1, categorie='feculent', photo='pain.jpg', description='Le pain est un aliment de base traditionnel de nombreuses cultures. Il se présente sous forme de miche, de miettes ou de baguette.', unite=True)

# crétaion des repas
r1 = repas(titre='Galette de riz', type='matin', label='Prise de masse')
r2 = repas(titre='Poulet et brocolis', type='midi', label='Maintien')
r3 = repas(titre='Patate douce poisson', type='soir', label='Sèche')

# le repas 1 est composé de 100g de pomme, 250g de banane et 40g d'orange
p1 = portion(repas=1, aliment=1, nombre=100)
p2 = portion(repas=1, aliment=2, nombre=250)
p3 = portion(repas=1, aliment=3, nombre=40)

# le repas 2 est composé de 100g de pain, 200g de poulet et 100g de brocolis
p4 = portion(repas=2, aliment=4, nombre=100)
p5 = portion(repas=2, aliment=1, nombre=200)
p6 = portion(repas=2, aliment=2, nombre=100)

# le repas 3 est composé de 100g de patate douce, 200g de poisson et 100g de brocolis
p7 = portion(repas=3, aliment=4, nombre=100)
p8 = portion(repas=3, aliment=1, nombre=200)
p9 = portion(repas=3, aliment=2, nombre=100)

# création de la diète
d1 = diete(titre_diete='Diète Pat Sèche 2500', createur=1, date='2020-01-01')
d2 = diete(titre_diete='Diète Pat Pdm 4000', createur=1, date='2020-01-01')

# la diète 1 est composée du repas 1, 2 et 3
e1 = estCompose(diete=1, repas=1)
e2 = estCompose(diete=1, repas=2)
e3 = estCompose(diete=1, repas=3)

# création de l'utilisateur terry tempestini terry57tt@gmail.com
u1 = utilisateur(nom='Tempestini', prenom='Terry', mail='terry57tt@gmail.com', mdp='terry57tt', age=21, taille=180, poids=80, sexe='homme', diete=1)

# ajout des données dans la base de données
db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.add(a4)
db.session.add(r1)
db.session.add(r2)
db.session.add(r3)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.add(p8)
db.session.add(p9)
db.session.add(d1)
db.session.add(d2)
db.session.add(e1)
db.session.add(e2)
db.session.add(e3)
db.session.add(u1)

db.session.commit()'''
