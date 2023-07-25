from setup_sql import db

class Aliment(db.Model):
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
        return Aliment.query.get(id)

    def get_all():
        return Aliment.query.order_by(Aliment.titre).all()
    
    def delete(self):
        db.session.delete(self)