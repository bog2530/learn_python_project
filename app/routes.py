"""Основной модуль роутинга."""
# -*- coding: utf-8 -*-
from flask import flash, redirect, render_template, url_for

from flask_login import current_user

from app import app, db # noqa
from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
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
