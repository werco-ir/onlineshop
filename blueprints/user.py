from flask import Blueprint, render_template, request, redirect, url_for, flash, json
from flask_login import login_user, login_required, current_user,logout_user
from passlib.hash import sha256_crypt
from extentions import db
from models.cart import Cart
from models.payment import Payment
from models.product import Product
from models.user import User
from models.cart_item import CartItem
import requests

app = Blueprint("user", __name__)


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('user.dashboard'))
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
                flash("نام کاربری دیگری انتخاب کنید.")
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
                flash('نام کاربری یا رمزعبور اشتباه است.')
                return redirect(url_for("user.login"))

            if sha256_crypt.verify(password, user.password):
                login_user(user)
                return redirect(url_for('user.dashboard'))
            else:
                flash('رمزعبور اشتباه است.')
                return redirect(url_for("user.login"))


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


@app.route('/user/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        return render_template('user/dashboard.html')
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)
        phone = request.form.get('phone', None)
        address = request.form.get('address', None)

        if current_user.username != username:
            user = User.query.filter(User.username == username).first()
            if user != None:
                flash("نام کاربری از قبل انتخاب شده است!")
                return redirect(url_for("user.dashboard"))
            else:
                current_user.username = username
        if password != None:
            current_user.password = sha256_crypt.encrypt(password)

        current_user.email = email
        current_user.phone = phone
        current_user.address = address
        db.session.commit()
        flash("تغییرات با موفقیت انجام شد.")

        return redirect(url_for('user.dashboard'))


@app.route('/add-to-cart', methods=['GET'])
@login_required
def add_to_cart():
    id = request.args.get('id')
    product = Product.query.filter(Product.id == id).first_or_404()

    cart = current_user.carts.filter(Cart.status == "pending").first()
    if cart == None:
        cart = Cart()
        current_user.carts.append(cart)
        db.session.add(cart)

    cart_item = cart.cart_items.filter(CartItem.product == product).first()
    if cart_item == None:
        item = CartItem(quantity=1)
        item.price = product.price
        item.cart = cart
        item.product = product
        db.session.add(item)
    else:
        cart_item.quantity += 1

    db.session.commit()

    return redirect(url_for('user.cart'))





@app.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("از حساب کاربری خارج شدید.")
    return redirect("/")

@app.route('/remove-from-cart', methods=['GET'])
@login_required
def remove_from_cart():
    id = request.args.get('id')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)
    db.session.commit()

    return redirect(url_for('user.cart'))


@app.route('/cart', methods=['GET'])
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status == "pending").first()
    return render_template('user/cart.html', cart=cart)


@app.route('/payment', methods=['GET'])
@login_required
def payment():
    r = requests.post("https://payment.zarinpal.com/pg/v4/payment/request.json",
                      data={
                          'merchant_id': '73a4c8d3-8e5a-4909-827e-fd3e0b1574c4',
                          'amount': 10000,
                          'callback_url': 'http://localhost:5000/verify',
                          'description': 'Transaction description'

                      })
    print(r.text)
    return "ok"


@app.route('/user/dashboard/order/<id>', methods=['GET'])
@login_required
def order(id):
    cart = current_user.carts.filter(Cart.id == id).first_or_404()
    return render_template('user/order.html', cart=cart)
