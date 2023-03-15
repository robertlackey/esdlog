from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ESDForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    method = db.Column(db.String(20))
    contact_info = db.Column(db.String(100))
    date = db.Column(db.Date)
    notes = db.Column(db.String(1000))

    def __init__(self, type, company, position, method, contact_info, date, notes):
        self.type = type
        self.company = company
        self.position = position
        self.method = method
        self.contact_info = contact_info
        self.date = date
        self.notes = notes