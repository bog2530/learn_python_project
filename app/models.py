"""
    Основной модуль модели приложения
"""
from datetime import datetime

from app import db


class User(db.Model):
    """
        Пользователь приложения
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self) -> None:
        return '<User {}>'.format(self.username)


class Book(db.Model):
    """
        Книга распарсенный объект формата PDF

        title: Заголовок книги
        input_book_path: путь где лежит исходный файл
        text: отпарсенный текст
        date_created: дата загрузки книги
        user_id: id пользователя загрузившего книгу
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    title = db.Column(db.String(60), index=True, unique=True)
    input_book_path = db.Column(db.String(120), unique=True)
    text = db.Column(db.String(2000))  # Вот тут не знаю сколько символов??
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Отношения
    user = db.relationship('User', backref='books', lazy='dynamic')

    def __repr__(self) -> None:
        return f'<Book id: {self.id} title: {self.title}>'


class Word(db.Model):
    """
        Объект слово (или словосочетание)
        base_text: текст слова на родном языке
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    base_text = db.Column(db.String(120), index=True)


class BookWord(db.Model):
    """
        many to many Book and Word
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    # не знаю как тут в модели прописать backref для связующихся объектов


class Translation(db.Model):
    """
        Объект является одним из вариантов перевода объекта "Word"
    """
    id = db.Column(db.Integer, primary_key=True) # noqa
    translate = db.Column(db.String(120), index=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    # Отношения
    word = db.relationship('Word', backref='translations', lazy='dynamic')
