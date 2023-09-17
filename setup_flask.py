import os
import controllers
from flask import Flask
from setup_sql import db
from flask_login import LoginManager
from models.Utilisateur import Utilisateur
from flask_mail import Mail
from flask_session import Session

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/upload/'
size_limit_mo = 10

basedir = os.path.abspath(os.path.dirname(__file__))

flask_serv_intern = Flask(__name__,
                              static_folder="static",
                              template_folder='templates')

flask_serv_intern.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
flask_serv_intern.secret_key = 'secret_key'

flask_serv_intern.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_serv_intern.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_serv_intern.config['MAX_CONTENT_LENGTH'] = size_limit_mo * 1024 * 1024
flask_serv_intern.jinja_env.add_extension('jinja2.ext.do')

db.init_app(flask_serv_intern)

flask_serv_intern.register_blueprint(controllers.app)

# Setup the Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(flask_serv_intern)
login_manager.login_view = 'controllers.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

# Setup Mail Configurations
flask_serv_intern.config['MAIL_SERVER'] = 'smtp.gmail.com'
flask_serv_intern.config['MAIL_PORT'] = 465
flask_serv_intern.config['MAIL_USE_SSL'] = True
flask_serv_intern.config['MAIL_USERNAME'] = 'terrynutritionapp@gmail.com'
flask_serv_intern.config['MAIL_PASSWORD'] = 'qqfpvggfqadsuxkx'
mail = Mail(flask_serv_intern)

# Setup Cookies Configurations
flask_serv_intern.config['COOKIES_SECRET_KEY'] = 'secret_key'
flask_serv_intern.config['COOKIES_EXPIRE_TIME'] = 60 * 60 * 24 * 7
Session(flask_serv_intern)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

with flask_serv_intern.app_context():
        db.create_all()

if __name__ == "__main__":
    flask_serv_intern.run(debug=True)