from importlib.resources import Resource
from flask import request
from flask_jwt_extended import jwt_required

from base import AuxEvento, socketio
from primer_evento.base import Evento, db, q, api, app


class VistaEvento(Resource):
    eventos = []
    @jwt_required()
    def get(self):
        q.enqueue(getPrimerIntentoEvento, request.json['evento'])
        q.enqueue(getSegundoIntentoEvento, request.json['evento'])
        q.enqueue(getTercerIntentoEvento, request.json['evento'])
        return {"message": "Eventos encolados correctamente."}, 200


def getPrimerIntentoEvento(evento):
    pass

def getSegundoIntentoEvento(evento):
    pass

def getTercerIntentoEvento(evento):
    pass

def process_order(evento):
    db.session.add(evento)
    db.session.commit()
    eventos = (db.session.query(AuxEvento).filter(evento.peticion == AuxEvento.peticion).filter(evento.lugar == AuxEvento.lugar).scalar())
    if eventos > 1:
        sendValue((db.session.query(AuxEvento).filter(evento.peticion == AuxEvento.peticion).filter(evento.lugar == AuxEvento.lugar).all()))

def sendValue(eventos):
    socketio.emit('response', {'evento': eventos[0]})


api.add_resource(VistaEvento, '/api-commands/events')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')