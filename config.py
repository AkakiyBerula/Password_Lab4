import os
basedir = os.path.abspath(os.path.dirname(__file__))


WTF_CSRF_ENABLED = True
SECRET_KEY = "secretkey"

RECAPTCHA_PUBLIC_KEY = "6LcI6yEjAAAAALFm0sXu5fJS7yPfLt98Gz9VMCFn"
RECAPTCHA_PRIVATE_KEY = "6LcI6yEjAAAAADhd7NpdvF6qD-8wYkpp4WNbGMnD"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'vlad5dyakun@gmail.com'
MAIL_PASSWORD = 'txllkyvyukajvuhe'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

SQLALCHEMY_DATABASE_URI = r'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATORS = False