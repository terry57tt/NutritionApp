from setup_sql import db
from models.Aliment import Aliment

class Portion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diete = db.Column(db.Integer, db.ForeignKey('diete.id'))
    aliment = db.Column(db.Integer, db.ForeignKey('aliment.id'))
    nombre = db.Column(db.Integer, nullable=False, server_default='0')
    label_portion = db.Column(db.Integer, nullable=False, server_default='0') # 1=matin, 2=collation matin, 3=midi, 4=collation aprem, 5=soir, 6=collation soir
    diete_obj = db.relationship('Diete', backref=db.backref('portions'))
    aliment_obj = db.relationship('Aliment', backref=db.backref('portions'))

    def get_by_id(id):
        return Portion.query.get(id)
    
    def get_all():
        return Portion.query.order_by(Portion.label_portion, Aliment.titre).all()

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