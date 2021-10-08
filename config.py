import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
        Сдель храняться основные настройки сервера
        SQLALCHEMY_DATABASE_URI: путь до базы данных (sql_lite)
        SQLALCHEMY_TRACK_MODIFICATIONS: изменения в SQL не отслеживаются
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
