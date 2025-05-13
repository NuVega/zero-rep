from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import  app, models, forms, bcrypt, db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm


@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Введены неверные данные', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.password.data:
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Профиль обновлён', 'success')
        return redirect(url_for('account'))

    # Подставим текущие значения
    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('edit_profile.html', form=form)
