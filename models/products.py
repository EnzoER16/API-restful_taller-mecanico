from models.db import db

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, productName, price, stock):
        self.productName = productName
        self.price = price
        self.stock = stock

    def serialize(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'price': self.price,
            'stock': self.stock
        }