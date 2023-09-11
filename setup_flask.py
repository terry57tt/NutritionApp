import os
import controllers
from flask import Flask
from setup_sql import db

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

with flask_serv_intern.app_context():
        db.create_all()

if __name__ == "__main__":
    flask_serv_intern.run(debug=True)


