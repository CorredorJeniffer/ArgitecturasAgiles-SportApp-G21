import datetime
import random

from flask import request

from tercer_evento.base import Evento, db, q, api, app

contador = 0
auxEvento = Evento(
    datetime.strptime('2024-02-16', '%Y-%m-%d'),
    datetime.strptime('2024-02-23', '%Y-%m-%d'),
    "Error",
    "Error"
)

def getTercerIntentoEvento(evento):
    eventos = (db.session.query(Evento).filter(Evento.fecha_inicio < request.json['fecha'])
               .filter(Evento.fecha_fin > evento['fecha'])
               .filter(Evento.lugar == evento['lugar']).all())
    if eventos is not None and has_to_continue_ok():
        # add to queue to process order
        q.enqueue(process_order, eventos[0])
        return {"message": "Eventos encolados correctamente."}, 200
    else:
        q.enqueue(process_order, auxEvento)
        return {"error": "There aren't events"}, 400


def has_to_continue_ok():
    number = random.randint(1, 10)
    if number % 3 == 0:
        return True
    else:
        return False


def process_order(data):
    pass
