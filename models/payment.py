from models.db import db

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(25), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, cost, method, date):
        self.cost = cost
        self.method = method
        self.date = date

    def serialize(self):
        return {
            'id': self.id,
            'cost': self.cost,
            'method': self.method,
            'date': self.date
        }