"""Основной модуль роутинга."""
# -*- coding: utf-8 -*-
import os

from flask import flash, redirect, render_template, request, url_for

from flask_login import current_user, login_required, login_user, logout_user

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db # noqa
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User

from config import Config


@app.route('/')
@app.route('/index')
@login_required
def index() -> None:
    posts = ["Hello, World!"]
    return render_template("index.html", title='Home Page', posts=posts)


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
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        file_pdf = request.files['file']
        if file_pdf and allowed_file(file_pdf.filename):
            filename = secure_filename(file_pdf.filename)
            file_pdf.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            flash('File added')
        else:
            flash('File is not a pdf')
    return render_template('upload.html', form=form)
