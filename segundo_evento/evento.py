from datetime import datetime

from flask import request

from segundo_evento.base import Evento, db, q, api, app

auxEvento = Evento(
    datetime.strptime('2024-02-16', '%Y-%m-%d'),
    datetime.strptime('2024-02-23', '%Y-%m-%d'),
    "Error2",
    "Error2"
)

def getSegundoIntentoEvento(evento):
    eventos = (db.session.query(Evento).filter(Evento.fecha_inicio < request.json['fecha'])
               .filter(Evento.fecha_fin > evento['fecha'])
               .filter(Evento.lugar == evento['lugar']).all())
    if eventos:
        q.enqueue(process_order, eventos[0])
        return {"message": "Eventos encolados correctamente."}, 200
    else:
        q.enqueue(process_order, auxEvento)

def process_order(data):
    pass

