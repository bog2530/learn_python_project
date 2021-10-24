import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Сдесь храняться основные настройки сервера

        Ключевые аргументы:
        SQLALCHEMY_DATABASE_URI: путь до базы данных (sql_lite)
        SQLALCHEMY_TRACK_MODIFICATIONS: изменения в SQL не отслеживаются
        SECRET_KEY: секретный ключ
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'python_learn'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'books')
    ALLOWED_EXTENSIONS = {'pdf'}
