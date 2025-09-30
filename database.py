from peewee import *
from datetime import date, time

# Conexión a SQLite
db = SqliteDatabase("mi_base_datos.db")

class Evento(Model):
    """
    Representa un evento registrado.
    """
    tipo = CharField()  # cumpleaños, boda, etc.
    nombre_cliente = CharField()
    monto_garantia = FloatField()
    monto_total = FloatField()
    dia = DateField()
    hora_fin = TimeField()
    decoracion = BooleanField(default=False)
    num_invitados = IntegerField(null=True)  # opcional
    estado_pago = CharField(default="Pendiente")  # Pendiente, Parcial, Completo
    observaciones = TextField(null=True)

    class Meta:
        database = db


def inicializar_db():
    db.connect()
    db.create_tables([Evento], safe=True)
    print("📌 Base de datos inicializada.")


# ---------------- FUNCIONES ---------------- #
def agregar_evento(tipo, nombre_cliente, monto_garantia, monto_total, dia, hora_fin, decoracion,
                   num_invitados=None, estado_pago="Pendiente", observaciones=None):
    evento = Evento.create(
        tipo=tipo,
        nombre_cliente=nombre_cliente,
        monto_garantia=monto_garantia,
        monto_total=monto_total,
        dia=dia,
        hora_fin=hora_fin,
        decoracion=decoracion,
        num_invitados=num_invitados,
        estado_pago=estado_pago,
        observaciones=observaciones
    )
    print(f"✅ Evento '{tipo}' para {nombre_cliente} agregado.")
    return evento


def listar_eventos():
    print("\n📌 Lista de eventos:")
    for e in Evento.select():
        deco = "Sí" if e.decoracion else "No"
        print(f"- ID {e.id}: {e.tipo} | Cliente: {e.nombre_cliente} | "
              f"Garantía: {e.monto_garantia} | Total: {e.monto_total} | "
              f"Día: {e.dia} | Hora fin: {e.hora_fin} | Decoración: {deco}")
    print()


def modificar_evento(id_evento, **kwargs):
    try:
        evento = Evento.get_by_id(id_evento)
        for campo, valor in kwargs.items():
            setattr(evento, campo, valor)
        evento.save()
        print(f"✏️ Evento {id_evento} modificado.")
    except Evento.DoesNotExist:
        print("⚠️ El evento no existe.")


def eliminar_evento(id_evento):
    try:
        evento = Evento.get_by_id(id_evento)
        evento.delete_instance()
        print(f"❌ Evento {id_evento} eliminado.")
    except Evento.DoesNotExist:
        print("⚠️ El evento no existe.")
