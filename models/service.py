from models.db import db

class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    in_date = db.Column(db.Date, nullable=False)
    out_date = db.Column(db.Date, nullable=False)

    def __init__(self, description, in_date, out_date):
        self.description = description
        self.in_date = in_date
        self.out_date = out_date

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'in_date': self.in_date,
            'out_date': self.out_date
        }