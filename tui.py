from database import inicializar_db, agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import date, time

def menu():
    inicializar_db()

    while True:
        print("\n===== MENÚ DE EVENTOS =====")
        print("1. Agregar evento")
        print("2. Modificar evento")
        print("3. Eliminar evento")
        print("4. Listar eventos")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            tipo = input("Tipo de evento: ")
            nombre = input("Nombre del cliente: ")
            garantia = float(input("Monto de garantía: "))
            total = float(input("Monto total: "))
            dia = date.fromisoformat(input("Fecha (YYYY-MM-DD): "))
            hora = time.fromisoformat(input("Hora fin (HH:MM): "))
            decoracion = input("¿Decoración? (s/n): ").lower() == "s"
            agregar_evento(tipo, nombre, garantia, total, dia, hora, decoracion)

        elif opcion == "2":
            id_ev = int(input("ID del evento a modificar: "))
            nuevo_total = float(input("Nuevo monto total: "))
            modificar_evento(id_ev, monto_total=nuevo_total)

        elif opcion == "3":
            id_ev = int(input("ID del evento a eliminar: "))
            eliminar_evento(id_ev)

        elif opcion == "4":
            listar_eventos()

        elif opcion == "0":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == "__main__":
    menu()
