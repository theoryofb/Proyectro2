from database import agregar_evento, listar_eventos, eliminar_evento
from datetime import datetime

def menu_consola():
    while True:
        print("\n=== CONSOLA DE EVENTOS ===")
        print("1. Agregar evento")
        print("2. Listar eventos")
        print("3. Eliminar evento")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            tipo = input("Tipo de evento: ")
            nombre = input("Nombre del cliente: ")
            carnet = input("Carnet: ")
            direccion = input("Dirección: ")
            monto_garantia = float(input("Monto de garantía: "))
            monto_total = float(input("Monto total: "))
            dia = input("Fecha (YYYY-MM-DD): ")
            hora_fin = input("Hora fin (HH:MM): ")
            decoracion = input("Decoración (s/n): ").lower() == "s"

            agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
            print("✅ Evento agregado.")

        elif opcion == "2":
            eventos = listar_eventos()
            for e in eventos:
                print(f"[{e.id}] {e.tipo} - {e.nombre} - {e.dia} - {e.hora_fin}")

        elif opcion == "3":
            evento_id = int(input("ID del evento a eliminar: "))
            if eliminar_evento(evento_id):
                print("🗑️ Evento eliminado.")
            else:
                print("❌ No se encontró ese ID.")

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_consola()
