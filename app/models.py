"""Основной модуль модели приложения"""
from datetime import datetime

from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login # noqa


class User(UserMixin, db.Model):
    """Модель пользователи. """

    id = db.Column(db.Integer, primary_key=True) # noqa
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self) -> None:
        return '<User {}>'.format(self.username)

    def set_password(self, password) -> str:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id) -> None: # noqa
    return User.query.get(int(id))


class BookWord(db.Model):
    """many to many Book and Word"""
    id = db.Column(db.Integer, primary_key=True) # noqa
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))


class Book(db.Model):
    """Книга распарсенный объект формата PDF

        title: Заголовок книги
        input_book_path: путь где лежит исходный файл
        text: отпарсенный текст
        date_created: дата загрузки книги
        user_id: id пользователя загрузившего книгу"""
    id = db.Column(db.Integer, primary_key=True) # noqa
    title = db.Column(db.String(60), index=True, unique=True)
    input_book_path = db.Column(db.String(120), unique=True)
    text = db.Column(db.Text())
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Отношения
    user = db.relationship('User', backref='books', lazy='dynamic')
    words = db.relationship(
        'Word', secondary=BookWord, lazy='subquery', backref=db.backref('words', lazy=True))

    def __repr__(self) -> None:
        return f'<Book id: {self.id} title: {self.title}>'


class Word(db.Model):
    """Объект слово (или словосочетание)
        base_text: текст слова на родном языке"""
    id = db.Column(db.Integer, primary_key=True) # noqa
    base_text = db.Column(db.String(120), index=True)


class Translation(db.Model):
    """Объект является одним из вариантов перевода объекта "Word"
        translate: перевод слова
        word_id: id слова которое переводят"""
    id = db.Column(db.Integer, primary_key=True) # noqa
    translate = db.Column(db.String(120), index=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    # Отношения
    word = db.relationship('Word', backref='translations', lazy='dynamic')


class DictionaryWord(db.Model):
    """Модель словарь слов. """
    id = db.Column(db.Integer, primary_key=True) # noqa
    word_id = db.Column(db.Integer, db.ForeignKey('dictionary.id'))
    dictionary_id = db.Column(db.Integer, db.ForeignKey('word.id'))


class Dictionary(db.Model):
    """Модель словарь."""
    id = db.Column(db.Integer, primary_key=True) # noqa
    name = db.Column(db.String(120))  # не знаю сколько символов
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='dictionaries', lazy='dynamic')
    words = db.relationship(
        'Word', secondary=DictionaryWord, lazy='subquery', backref=db.backref('words', lazy=True))

    def __repr__(self) -> None:
        return f'<Dictionary: {self.id} name: {self.name}>'


class Sentence(db.Model):
    """Модель предложения.

        Ключевые аргументы:
        base_text - текст предложения
        translate_text - перевод предложения"""
    id = db.Column(db.Integer, primary_key=True) # noqa
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    base_text = db.Column(db.Text())
    translate_text = db.Column(db.Text())
    book = db.relationship(
        'Book', backref='sentences', lazy='dynamic')

    def __repr__(self) -> None:
        return f'<Sentence: {self.id} text: {self.name}, translate: {self.translate_text}>'
