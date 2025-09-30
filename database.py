from peewee import *
from datetime import datetime, date, time

# ---------------- BASE DE DATOS ---------------- #
db = SqliteDatabase("eventos.db")

class BaseModel(Model):
    class Meta:
        database = db

class Evento(BaseModel):
    tipo = CharField()                        # Tipo de evento (cumpleaños, boda, etc.)
    nombre = CharField()                      # Nombre del cliente
    carnet = CharField()                      # Carnet de identidad
    direccion_domicilio = CharField()         # Dirección del cliente
    monto_garantia = FloatField()             # Monto entregado como garantía
    monto_total = FloatField()                # Monto total del evento
    dia = DateField()                         # Fecha del evento
    hora_fin = TimeField()                    # Hora de finalización del evento
    decoracion = BooleanField(default=False)  # Si se solicitó decoración

# Crear tablas si no existen
db.connect()
db.create_tables([Evento], safe=True)

# ---------------- FUNCIONES ---------------- #
def agregar_evento():
    print("\n➕ Registrar un nuevo evento:")
    tipo = input("🎂 Tipo de evento: ")
    nombre = input("👤 Nombre del cliente: ")
    carnet = input("🪪 Carnet de identidad: ")
    direccion = input("🏠 Dirección de domicilio: ")
    monto_garantia = float(input("💰 Monto de garantía: "))
    monto_total = float(input("💵 Monto total: "))
    dia = input("📅 Fecha (YYYY-MM-DD): ")
    hora_fin = input("⏰ Hora de finalización (HH:MM): ")
    decoracion = input("🎀 ¿Requiere decoración? (s/n): ").lower() == "s"

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
    print("✅ Evento agregado con éxito.")

def listar_eventos():
    print("\n📋 Lista de eventos:")
    for evento in Evento.select():
        print(f"🆔 {evento.id} | 🎂 {evento.tipo} | 👤 {evento.nombre} | 🪪 {evento.carnet} | "
              f"🏠 {evento.direccion_domicilio} | 💰 Garantía: {evento.monto_garantia} | 💵 Total: {evento.monto_total} | "
              f"📅 {evento.dia} | ⏰ {evento.hora_fin} | 🎀 Decoración: {'Sí' if evento.decoracion else 'No'}")
    print()

def modificar_evento():
    listar_eventos()
    try:
        evento_id = int(input("✏️ ID del evento a modificar: "))
        evento = Evento.get_by_id(evento_id)

        print("Deja en blanco si no quieres cambiar un campo.")
        tipo = input(f"🎂 Tipo [{evento.tipo}]: ") or evento.tipo
        nombre = input(f"👤 Nombre [{evento.nombre}]: ") or evento.nombre
        carnet = input(f"🪪 Carnet [{evento.carnet}]: ") or evento.carnet
        direccion = input(f"🏠 Dirección [{evento.direccion_domicilio}]: ") or evento.direccion_domicilio
        monto_garantia = input(f"💰 Garantía [{evento.monto_garantia}]: ")
        monto_total = input(f"💵 Total [{evento.monto_total}]: ")
        dia = input(f"📅 Fecha [{evento.dia}]: ")
        hora_fin = input(f"⏰ Hora fin [{evento.hora_fin}]: ")
        decoracion = input(f"🎀 Decoración (s/n) [{'Sí' if evento.decoracion else 'No'}]: ")

        evento.tipo = tipo
        evento.nombre = nombre
        evento.carnet = carnet
        evento.direccion_domicilio = direccion
        if monto_garantia != "":
            evento.monto_garantia = float(monto_garantia)
        if monto_total != "":
            evento.monto_total = float(monto_total)
        if dia != "":
            evento.dia = datetime.strptime(dia, "%Y-%m-%d").date()
        if hora_fin != "":
            evento.hora_fin = datetime.strptime(hora_fin, "%H:%M").time()
        if decoracion.lower() in ["s", "n"]:
            evento.decoracion = decoracion.lower() == "s"

        evento.save()
        print("✅ Evento modificado con éxito.")

    except Evento.DoesNotExist:
        print("❌ No se encontró el evento.")

def eliminar_evento():
    listar_eventos()
    try:
        evento_id = int(input("🗑️ ID del evento a eliminar: "))
        evento = Evento.get_by_id(evento_id)
        evento.delete_instance()
        print("✅ Evento eliminado con éxito.")
    except Evento.DoesNotExist:
        print("❌ No se encontró el evento.")

# ---------------- MENÚ ---------------- #
def menu():
    while True:
        print("\n🎉 MENÚ PRINCIPAL - GESTIÓN DE EVENTOS 🎉")
        print("1️⃣  Agregar evento")
        print("2️⃣  Modificar evento")
        print("3️⃣  Eliminar evento")
        print("4️⃣  Listar eventos")
        print("5️⃣  Salir")

        opcion = input("👉 Selecciona una opción: ")

        if opcion == "1":
            agregar_evento()
        elif opcion == "2":
            modificar_evento()
        elif opcion == "3":
            eliminar_evento()
        elif opcion == "4":
            listar_eventos()
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("⚠️ Opción inválida, intenta de nuevo.")

# ---------------- EJECUCIÓN ---------------- #
if __name__ == "__main__":
    menu()

