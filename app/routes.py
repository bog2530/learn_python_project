"""Основной модуль роутинга."""
# -*- coding: utf-8 -*-
import os
import uuid
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import Book, Sentence, Translation, User, Word
from app.parser import open_pdf, split_into_sentences, split_into_words
from app.translator import translate
from config import Config


@app.route('/')
@app.route('/books')
@login_required
def books() -> None:
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter(Book.user_id == current_user.id).order_by(Book.date_created.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'])
    return render_template("index.html", title='Books', books=books)


@app.route('/register', methods=['GET', 'POST'])
def register() -> None:
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('books')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('books'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        file_pdf = request.files['file']
        if file_pdf and allowed_file(file_pdf.filename):
            filename = secure_filename(f'{uuid.uuid4()}.pdf')
            file_pdf.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            file_path = os.path.abspath(f'books/{filename}')
            title_author = f'{form.author.data} - {form.title.data}'
            date_created = datetime.now()
            text = open_pdf(file_path)
            flash('File added')
            book = Book(
                user_id=current_user.id, input_book_path=file_path,
                text=text, title=title_author, date_created=date_created)
            db.session.add(book)
            db.session.flush()
            split_sentences = split_into_sentences(text)
            split_words = split_into_words(text)
            for sentence in split_sentences:
                translation_sentence = translate(sentence)
                sentence_db = Sentence(base_text=sentence, translate_text=translation_sentence, book_id=book.id)
                db.session.add(sentence_db)
                db.session.flush()
            for word in split_words:
                word_db = Word(base_text=word)
                db.session.add(word_db)
                db.session.flush()
                word_db.b_words.append(book)
                translation_word = translate(word)
                translation = Translation(translate=translation_word, word_id=word_db.id)
                db.session.add(translation)
                db.session.commit()
        else:
            flash('File is not a pdf')
    return render_template('upload.html', form=form)


@app.route('/books/<int:id>/del')
@login_required
def book_delete(id):
    try:
        book_del = Book.query.filter(Book.user_id == current_user.id, Book.id == id).first()
        db.session.delete(book_del)
        db.session.commit()
        flash(f'File deleted: {book_del.title}')
    except Exception:
        flash('File cannot be deleted')
    return redirect(url_for('books'))


@app.route('/books/<int:id>/sentences/')
@login_required
def sentence(id):
    page = request.args.get('page', 1, type=int)
    sentences = Sentence.query.join(Book).filter(Book.id == id, Book.user_id == current_user.id).paginate(
        page, app.config['POSTS_PER_PAGE'])
    return render_template("sentence.html", title='Home Page', sentences=sentences, id=id)


@app.route('/books/<int:id>/words')
@login_required
def words(id):
    page = request.args.get('page', 1, type=int)
    words = Word.query.join(Book.words).filter(Book.id == id, Book.user_id == current_user.id).paginate(
        page, app.config['POSTS_PER_PAGE'])
    return render_template("word.html", title='Home Page', words=words, id=id)
