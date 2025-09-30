from peewee import *
from datetime import datetime

# ---------------- BASE DE DATOS ---------------- #
db = SqliteDatabase("eventos.db")

class BaseModel(Model):
    class Meta:
        database = db

class Evento(BaseModel):
    tipo = CharField()
    nombre = CharField()
    carnet = CharField()
    direccion_domicilio = CharField()
    monto_garantia = FloatField()
    monto_total = FloatField()
    dia = DateField()
    hora_fin = TimeField()
    decoracion = BooleanField(default=False)

# Crear tablas si no existen
db.connect()
db.create_tables([Evento], safe=True)

# ---------------- FUNCIONES CRUD ---------------- #
def agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion):
    """Agrega un evento a la base de datos"""
    Evento.create(
        tipo=tipo,
        nombre=nombre,
        carnet=carnet,
        direccion_domicilio=direccion,
        monto_garantia=monto_garantia,
        monto_total=monto_total,
        dia=datetime.strptime(dia, "%Y-%m-%d").date(),
        hora_fin=datetime.strptime(hora_fin, "%H:%M").time(),
        decoracion=decoracion
    )

def listar_eventos():
    """Devuelve todos los eventos como iterable (para GUI y TUI)"""
    return Evento.select()

def modificar_evento(evento_id, **kwargs):
    """Modifica un evento según su ID"""
    try:
        evento = Evento.get_by_id(evento_id)
        for campo, valor in kwargs.items():
            setattr(evento, campo, valor)
        evento.save()
        return True
    except Evento.DoesNotExist:
        return False

def eliminar_evento(evento_id):
    """Elimina un evento según su ID"""
    try:
        evento = Evento.get_by_id(evento_id)
        evento.delete_instance()
        return True
    except Evento.DoesNotExist:
        return False
