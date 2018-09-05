import os

CSRF_ENABLED = True
SECRET_KEY = 'djfbvkdfnjvnj239p[QqlkxmQLKMo2j340sdcjwd2'

# DB_HOST = os.environ.get('DB_HOST')
# DB_PORT = os.environ.get('DB_PORT')
# DB_USER = os.environ.get('DB_USER')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')
# DB_NAME = os.environ.get('DB_NAME')

basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')

# SQLALCHEMY_DATABASE_URI = 'postgres://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME

# email server
MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'alexkoritsa'
MAIL_PASSWORD = 'qwertyqwertyqwerty'
