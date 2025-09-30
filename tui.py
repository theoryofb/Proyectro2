from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime

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
            agregar_evento_tui()
        elif opcion == "2":
            modificar_evento_tui()
        elif opcion == "3":
            eliminar_evento_tui()
        elif opcion == "4":
            listar_eventos_tui()
        elif opcion == "5":
            print("👋 ¡Hasta luego! Saliendo del sistema...")
            break
        else:
            print("⚠️ Opción inválida, intenta de nuevo.")

# ---------------- FUNCIONES TUI ---------------- #
def agregar_evento_tui():
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

    agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
    print("✅ Evento agregado con éxito.")

def listar_eventos_tui():
    print("\n📋 Lista de eventos:")
    for e in listar_eventos():
        print(f"🆔 {e.id} | 🎂 {e.tipo} | 👤 {e.nombre} | 🪪 {e.carnet} | "
              f"🏠 {e.direccion_domicilio} | 💰 Garantía: {e.monto_garantia} | 💵 Total: {e.monto_total} | "
              f"📅 {e.dia} | ⏰ {e.hora_fin} | 🎀 Decoración: {'Sí' if e.decoracion else 'No'}")
    print()

def modificar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input("✏️ ID del evento a modificar: "))
        print("Deja en blanco si no quieres cambiar un campo.")
        tipo = input("🎂 Nuevo tipo: ")
        nombre = input("👤 Nuevo nombre: ")
        carnet = input("🪪 Nuevo carnet: ")
        direccion = input("🏠 Nueva dirección: ")
        monto_garantia = input("💰 Nueva garantía: ")
        monto_total = input("💵 Nuevo total: ")
        dia = input("📅 Nueva fecha (YYYY-MM-DD): ")
        hora_fin = input("⏰ Nueva hora fin (HH:MM): ")
        decoracion = input("🎀 Nueva decoración (s/n): ")

        kwargs = {}
        if tipo: kwargs["tipo"] = tipo
        if nombre: kwargs["nombre"] = nombre
        if carnet: kwargs["carnet"] = carnet
        if direccion: kwargs["direccion_domicilio"] = direccion
        if monto_garantia: kwargs["monto_garantia"] = float(monto_garantia)
        if monto_total: kwargs["monto_total"] = float(monto_total)
        if dia: kwargs["dia"] = datetime.strptime(dia, "%Y-%m-%d").date()
        if hora_fin: kwargs["hora_fin"] = datetime.strptime(hora_fin, "%H:%M").time()
        if decoracion.lower() in ["s", "n"]: kwargs["decoracion"] = decoracion.lower() == "s"

        if modificar_evento(evento_id, **kwargs):
            print("✅ Evento modificado con éxito.")
        else:
            print("❌ No se encontró el evento.")
    except ValueError:
        print("⚠️ ID inválido.")

def eliminar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input("🗑️ ID del evento a eliminar: "))
        if eliminar_evento(evento_id):
            print("✅ Evento eliminado con éxito.")
        else:
            print("❌ No se encontró el evento.")
    except ValueError:
        print("⚠️ ID inválido.")

# ---------------- EJECUCIÓN ---------------- #
if __name__ == "__main__":
    menu()
