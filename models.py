from app import db
from sqlalchemy.sql import func

class aliment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=True)
    kcal = db.Column(db.Integer, nullable=True)
    proteines = db.Column(db.Integer, nullable=True)
    glucides = db.Column(db.Integer, nullable=True)
    lipides = db.Column(db.Integer, nullable=True)
    categorie = db.Column(db.String(255), nullable=True) # légume, fruit, féculent...
    photo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    unite = db.Column(db.Boolean, nullable=True)

class portion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))
    aliment = db.Column(db.Integer, db.ForeignKey('aliment.id'))
    nombre = db.Column(db.Integer, nullable=False, server_default='0') # qtt en g ou nb de portions
    label_portion = db.Column(db.Integer, nullable=False, server_default='0') # 1=matin, 2=collation matin, 3=midi, 4=collation aprem, 5=soir, 6=collation soir
    diete_obj = db.relationship('diete', backref=db.backref('portions'))
    aliment_obj = db.relationship('aliment', backref=db.backref('portions'))

    def unite(self):
        return self.aliment_obj.unite

    def proteines_portion(self):
        if self.unite():
            return round(self.aliment_obj.proteines * self.nombre)
        else:
            return round(self.aliment_obj.proteines * self.nombre * 0.01)
        
    def kcal_portion(self):
        if self.unite():
            return round(self.aliment_obj.kcal * self.nombre)
        else:
            return round(self.aliment_obj.kcal * self.nombre * 0.01)

class diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True) # nom de la diete
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])
    
    def portions_associees(self):
        return portion.query.filter(portion.diete == self.id).order_by(portion.label_portion).all()
    
    def total_kcal(self):
        return sum([portion.kcal_portion() for portion in self.portions_associees()])
    
    def total_proteines(self):
        return sum([portion.proteines_portion() for portion in self.portions_associees()])

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
