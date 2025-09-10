from peewee import *
from datetime import date

# Crear la base de datos SQLite
db = SqliteDatabase('mi_base_datos.db')

#Tabla TipoEvento

class TipoEvento(Model):
nombre=CharField(unique=True)

class Meta:
database=db

#Tabla Participante
class Participante(Model):
carnet = CharField(unique=True)
nombre=CharField()
dia_evento=DateField()
tipo_evento=ForeignKeyField(TipoEvento,backref='participantes')

class Meta:
database = db

#conectar y crear las tablas
db.connect()
db.create_tables(T
