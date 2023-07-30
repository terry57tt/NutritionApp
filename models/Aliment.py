from setup_sql import db, MAX_RESULTS

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
        return Aliment.query.order_by(Aliment.titre).limit(MAX_RESULTS).all()
    
    def delete(self):
        db.session.delete(self)

    def jsonformat(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'kcal': self.kcal,
            'proteines': self.proteines,
            'glucides': self.glucides,
            'lipides': self.lipides,
            'categorie': self.categorie,
            'photo': self.photo,
            'description': self.description,
            'unite': self.unite,
            'valide': self.valide
        }
    
    def search_by_titre(filter_value):
        return Aliment.query.filter(Aliment.titre.like('%' + filter_value + '%')).limit(MAX_RESULTS).all()
    
    def search_by_categorie(filter_value):
        return Aliment.query.filter(Aliment.categorie.like('%' + filter_value + '%')).limit(MAX_RESULTS).all()
    
    def search_by_titre_and_categorie(titre_filter, categorie_filter):
        return Aliment.query.filter(
            Aliment.titre.like('%' + titre_filter + '%'),
            Aliment.categorie.like('%' + categorie_filter + '%')
        ).limit(MAX_RESULTS).all()