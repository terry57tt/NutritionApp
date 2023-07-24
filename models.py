from app import db
from sqlalchemy.sql import func

class aliment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=True, unique=True)
    kcal = db.Column(db.Integer, nullable=True, server_default='0')
    proteines = db.Column(db.Integer, nullable=True, server_default='0')
    glucides = db.Column(db.Integer, nullable=True, server_default='0')
    lipides = db.Column(db.Integer, nullable=True, server_default='0')
    categorie = db.Column(db.String(255), nullable=True, server_default="Autre") # légume, fruit, féculent...
    photo = db.Column(db.String(255), nullable=True, server_default='')
    description = db.Column(db.String(255), nullable=True, server_default='')
    unite = db.Column(db.Integer, nullable=True, server_default='0') # 0 = 100g, 1 = 1 unité, 2 = mL
    valide = db.Column(db.Integer, nullable=True, server_default='0') # 0 = non validé, 1 = validé

    def get_by_id(id):
        return aliment.query.get(id)

    def get_all():
        return aliment.query.order_by(aliment.titre).all()
    
    def delete(self):
        db.session.delete(self)

class portion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))
    aliment = db.Column(db.Integer, db.ForeignKey('aliment.id'))
    nombre = db.Column(db.Integer, nullable=False, server_default='0')
    label_portion = db.Column(db.Integer, nullable=False, server_default='0') # 1=matin, 2=collation matin, 3=midi, 4=collation aprem, 5=soir, 6=collation soir
    diete_obj = db.relationship('diete', backref=db.backref('portions'))
    aliment_obj = db.relationship('aliment', backref=db.backref('portions'))

    def get_by_id(id):
        return portion.query.get(id)
    
    def get_all():
        return portion.query.order_by(portion.label_portion, aliment.titre).all()

    def unite(self):
        return self.aliment_obj.unite

    def kcal_portion(self):
        if self.unite() == 1: # si l'aliment est en unité (kcal * nombre)
            return round(self.aliment_obj.kcal * self.nombre)
        else: # aliment == 0 (kcal * nombre * 0.01 * 100g) ; aliment == 2 (kcal * nombre * 0.01 * 100mL) 
            return round(self.aliment_obj.kcal * self.nombre * 0.01)
        
    def proteines_portion(self):
        if self.unite() == 1:
            return round(self.aliment_obj.proteines * self.nombre)
        else:
            return round(self.aliment_obj.proteines * self.nombre * 0.01)
        
    def glucides_portion(self):
        if self.unite() == 1:
            return round(self.aliment_obj.glucides * self.nombre)
        else:
            return round(self.aliment_obj.glucides * self.nombre * 0.01)
        
    def lipides_portion(self):
        if self.unite() == 1:
            return round(self.aliment_obj.lipides * self.nombre)
        else:
            return round(self.aliment_obj.lipides * self.nombre * 0.01)
        

class diete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_diete = db.Column(db.String(255), nullable=True) # nom de la diete
    createur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)

    createur_obj = db.relationship('utilisateur', backref=db.backref('dietes'), foreign_keys=[createur])
    
    def get_by_id(id):
        return diete.query.get(id)
    
    def get_all():
        return diete.query.order_by(diete.date.desc()).all()
    
    def portions_associees(self):
        return portion.query.join(aliment).filter(portion.diete == self.id).order_by(portion.label_portion, aliment.titre).all()
    
    def total_kcal(self):
        return sum([portion.kcal_portion() for portion in self.portions_associees()])
    
    def total_proteines(self):
        return sum([portion.proteines_portion() for portion in self.portions_associees()])
    
    def total_glucides(self):
        return sum([portion.glucides_portion() for portion in self.portions_associees()])
    
    def total_lipides(self):
        return sum([portion.lipides_portion() for portion in self.portions_associees()])
    

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

    def get_by_id(id):
        return utilisateur.query.get(id)
    
    def get_all():
        return utilisateur.query.order_by(utilisateur.nom).all()

    def mail_partie1(self):
        return self.mail.split('@')[0]
    
    def mail_partie2(self):
        return self.mail.split('@')[1]
