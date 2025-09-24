from peewee import *
from datetime import date

# -----------------------------------------------------------
# Configuración de la base de datos SQLite
# -----------------------------------------------------------
db = SqliteDatabase('mi_base_datos.db')

# -----------------------------------------------------------
# Definición de modelos (tablas)
# -----------------------------------------------------------
class TipoEvento(Model):
    """
    Tabla de tipos de eventos (ej: Conferencia, Taller, Seminario).
    """
    nombre = CharField(unique=True)  # No se repite el nombre del evento

    class Meta:
        database = db


class Participante(Model):
    """
    Tabla de participantes asociados a un tipo de evento.
    """
    carnet = CharField(unique=True)  # Identificación única
    nombre = CharField()
    celular = CharField()
    diadeevento = DateField()
    tipo_evento = ForeignKeyField(TipoEvento, backref='participantes')

    class Meta:
        database = db


# -----------------------------------------------------------
# Funciones para trabajar con la base de datos
# -----------------------------------------------------------
def inicializar_db():
    """
    Crea las tablas si no existen.
    """
    db.connect()
    db.create_tables([TipoEvento, Participante], safe=True)
    print("📌 Base de datos inicializada.")


def agregar_evento(nombre_evento: str):
    """
    Agrega un nuevo tipo de evento.
    """
    try:
        evento, creado = TipoEvento.get_or_create(nombre=nombre_evento)
        if creado:
            print(f"✅ Evento '{nombre_evento}' creado.")
        else:
            print(f"ℹ️ El evento '{nombre_evento}' ya existe.")
        return evento
    except IntegrityError:
        print(f"⚠️ Error: no se pudo crear el evento '{nombre_evento}'.")


def listar_eventos():
    """
    Muestra todos los tipos de eventos.
    """
    print("\n📌 Lista de eventos:")
    for evento in TipoEvento.select():
        print(f"- {evento.id}: {evento.nombre}")
        print("\n")

def agregar_participante(carnet: str, nombre: str, celular: str, fecha_evento: date, id_evento: int):
    """
    Agrega un participante asociado a un evento.
    """
    try:
        evento = TipoEvento.get_by_id(id_evento)
        participante = Participante.create(
            carnet=carnet,
            nombre=nombre,
            celular=celular,
            diadeevento=fecha_evento,
            tipo_evento=evento
        )
        print(f"✅ Participante '{nombre}' agregado al evento '{evento.nombre}'.")
        return participante
    except TipoEvento.DoesNotExist:
        print("⚠️ Error: El evento con ese ID no existe.")


def listar_participantes():
    """
    Muestra todos los participantes con sus datos y evento.
    """
    print("\n📌 Lista de participantes:")
    for p in Participante.select():
        print(f"- {p.carnet} | {p.nombre} | {p.celular} | {p.diadeevento} | Evento: {p.tipo_evento.nombre}")
        print("\n")

# -----------------------------------------------------------
# Ejemplo de uso (solo se ejecuta si corres este archivo)
# -----------------------------------------------------------
if __name__ == "__main__":
    inicializar_db()

    # Crear algunos eventos
    agregar_evento("Conferencia")
    agregar_evento("Taller")

    # Listar eventos
    listar_eventos()

    # Agregar participantes
    agregar_participante("123456", "Gian Villca", "777888999", date(2025, 9, 10), 1)
    agregar_participante("654321", "Ana Pérez", "700123456", date(2025, 9, 11), 2)

    # Listar participantes
    listar_participantes()

    # Cerrar conexión
    db.close()
