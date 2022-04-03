import os 
from datetime import timedelta



# -------------------- Config Class --------------------
class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')


    REMEMBER_COOKIE_NAME = 'Flask_Blog' 
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=30)


    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')

    MAIL_USE_TLS = False
    MAIL_USE_SSL = False

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# -------------------- End of Config Class --------------------