import requests
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from redis.asyncio import Redis
from rq import Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_BINDS'] = {
    'db_one': 'sqlite:///shared.db',
    'db_two': 'sqlite:///db_two.sqlite3'
}
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

jwt = JWTManager(app)
api = Api(app)

token = requests.get(f"https://jwt-queries:5000/api-queries/jwt", verify=False)
token = token.json()
headers = {'Authorization': f"Bearer {token['access_token']}"}
queue_name = None
try:
    queue_name = requests.get(f"https://acl-queries:5000/api-queries/eventos/q", verify=False, headers=headers)
    queue_name = queue_name.json()
    queue_name = queue_name['primer_evento']
except:
    print("Queue q not in ACL")
    exit(1)

q = Queue(connection=Redis(host='redis', port=6379, db=queue_name))
queue_name = None


class Evento(db.Model):
    __bind_key__ = 'db_one'
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Integer)
    fecha_fin = db.Column(db.Integer)
    lugar = db.Column(db.Integer)
    peticion = db.Column(db.String(100))

class AuxEvento(db.Model):
    __bind_key__ = 'db_two'
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Integer)
    fecha_fin = db.Column(db.Integer)
    lugar = db.Column(db.Integer)
    peticion = db.Column(db.String(100))
