from peewee import *
from datetime import date

# Crear la base de datos SQLite
db = SqliteDatabase('mi_base_datos.db')

#Tabla TipoEvento

class TipoEvento(Model):
nombre=CharField(unique=True)

class Meta:
database=db
