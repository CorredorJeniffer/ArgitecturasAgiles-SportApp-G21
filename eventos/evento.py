from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////eventos.db'
db = SQLAlchemy(app)
api = Api(app)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lugar = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)