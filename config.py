import os

basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'Th0rHamm3rH1t5H4rD!1'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'seidh.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')

UPLOAD_FOLDER = 'tmp'

#app = Flask(__name__)
