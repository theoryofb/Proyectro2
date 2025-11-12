# consola/main.py
# Versión de consola simple (no TUI)
# Usa la misma base de datos eventos.db
# y las funciones definidas en database.py

from database import agregar_evento, listar_eventos, eliminar_evento
from datetime import datetime

def menu():
    while True:
        print("\n=== GESTOR DE EVENTOS (Consola) ===")
        print("1. Agregar evento")
        print("2. Listar eventos")
        print("3. Eliminar evento")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar()
        elif opcion == "2":
            listar()
        elif opcion == "3":
            eliminar()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def agregar():
    print("\n--- Agregar evento ---")
    nombre = input("Nombre del evento: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    lugar = input("Lugar: ")

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        agregar_evento(nombre, fecha, lugar)
        print("✅ Evento agregado con éxito.")
    except ValueError:
        print("❌ Formato de fecha inválido.")

def listar():
    print("\n--- Lista de eventos ---")
    eventos = listar_eventos()

    if not eventos:
        print("No hay eventos registrados.")
        return

    for e in eventos:
        print(f"[{e.id}] {e.nombre} - {e.fecha} - {e.lugar}")

def eliminar():
    print("\n--- Eliminar evento ---")
    listar()
    try:
        id_evento = int(input("ID del evento a eliminar: "))
        eliminar_evento(id_evento)
        print("🗑️ Evento eliminado.")
    except ValueError:
        print("❌ ID inválido.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    menu()
