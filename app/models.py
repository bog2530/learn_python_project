"""
    Основной модуль модели приложения
"""
from app import db


class User(db.Model):
    """
        Класс модели приложения
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self) -> None:
        return '<User {}>'.format(self.username)
