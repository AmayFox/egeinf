from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask_login import LoginManager, AnonymousUserMixin


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/photos/uploads')
UPLOAD_FOLDER_FOR_PROG = os.path.join(APP_ROOT, 'static/tasks')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS_FOR_PROGRAMMING = set(['txt'])

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_FOR_RPOG'] = UPLOAD_FOLDER_FOR_PROG


class AnonymousUser(AnonymousUserMixin):
    @property
    def date_format(self):
        return 'YYYY-MM-DD'

    @property
    def has_premium_features(self):
        return False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "api.LoginPage"
login_manager.anonymous_user = AnonymousUser

db = SQLAlchemy(app)

mail = Mail()
mail.init_app(app)


from flask import render_template
from web.api.routes import api
from web import db
from web.api.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


app.register_blueprint(api, url_prefix='/')


# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html')


@app.route('/error/right', methods=['GET'])
def error_right():
    return render_template('errors/right.html')
