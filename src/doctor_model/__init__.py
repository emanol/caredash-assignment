from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# adjust for localhost
USER = 'root'
PASSWORD = 'drowssap!'
HOST = 'localhost:3306'
DATABASE = 'caredash'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dr0wssap!@localhost:3306/caredash'

db = SQLAlchemy(app)

class Doctor(db.Model):
    __tablename__ = 'Doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)
    reviews = db.relationship('Review', backref=db.backref('doctor', lazy=True))

    def __repr__(self):
        doctor = {
            'id': self.id,
            'name': self.name,
            'reviews': self.reviews
        }
        return json.dumps(doctor)

class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctor.id'), nullable=True)

    def __repr__(self):
        review = {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'description': self.description
        }
        return json.dumps(dict)
