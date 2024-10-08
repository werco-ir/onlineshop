from sqlalchemy import *
from extentions import db
from sqlalchemy.orm import backref


class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=backref('carts', lazy='dynamic'))


    def total_price(self):
        total = 0
        for item in self.cart_items:
            t = item.price * item.quantity
            total += t
        return total


    def get_status_persion(self):
        if self.status == "pending":
            return "در انتظار پرداخت(سبد خرید)"
        elif self.status == "paid":
            return "پرداخت شده"
        elif self.status == "sent":
            return "ارسال شده"
        elif self.status == "rejected":
            return "رد شده"


