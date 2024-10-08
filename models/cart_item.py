from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    product = db.relationship('Product', backref='cart_items', lazy=True)
    cart = db.relationship('Cart', backref=backref('cart_items', lazy='dynamic'))
