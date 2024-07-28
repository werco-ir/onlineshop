from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from passlib.hash import sha256_crypt
from extentions import db
from models.user import User

app = Blueprint("user", __name__)


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        register = request.form.get('register', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        address = request.form.get('address', None)

        if register != None:
            user = User.query.filter(User.username == username).first()
            if user != None:
                flash("Choose another username.")
                return redirect(url_for("user.login"))

            user = User(username=username, password=sha256_crypt.encrypt(password), email=email, phone=phone,
                        address=address)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect(url_for('user.dashboard'))
        else:
            user = User.query.filter(User.username == username).first()
            if user == None:
                flash('Username or password is incorrect !')
                return redirect(url_for("user.login"))

            if sha256_crypt.verify(password, user.password):
                login_user(user)
                return redirect(url_for('user.dashboard'))
            else:
                flash('Password is incorrect !')
                return redirect(url_for("user.login"))
        return 'done'


@app.route('/user/login', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        register = request.form.get('register', None)
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')

        if register != None:
            user = User(username=username, password=sha256_crypt.encrypt(password), email=email, phone=phone,
                        address=address)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            return redirect('/user/dashboard')
        return 'done'


@app.route('/user/dashboard', methods=['GET'])
def dashboard():
    return "this is dashboard"