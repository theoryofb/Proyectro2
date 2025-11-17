import os
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style
from collections import Counter

# Inicializar colorama
init(autoreset=True)

# ---------------- FUNCIONES AUXILIARES ---------------- #
def clear_screen():
    print("\033c", end="")

def pause():
    print(Fore.MAGENTA + "\nPresiona Enter para continuar..." + Style.RESET_ALL)
    input()

# ---------------- MENÚ PRINCIPAL ---------------- #
def menu():
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        print("GESTIÓN DE EVENTOS".center(80))
        print("=" * 80 + Style.RESET_ALL)

        print(Fore.YELLOW + "1 - Agregar evento")
        print("2 - Modificar evento")
        print("3 - Eliminar evento")
        print("4 - Listar eventos")
        print("5 - Salir" + Style.RESET_ALL)

        print(Fore.BLUE + "\n(Atajos: Q o ESC para salir)" + Style.RESET_ALL)
        opcion = input(Fore.GREEN + "\nSelecciona una opción: " + Style.RESET_ALL).strip().lower()

        # 🔹 Bindings de salida
        if opcion in ["5", "q", "esc"]:
            print(Fore.MAGENTA + "Saliendo del sistema...")
            break

        if opcion == "1":
            agregar_evento_tui()
        elif opcion == "2":
            modificar_evento_tui()
        elif opcion == "3":
            eliminar_evento_tui()
        elif opcion == "4":
            listar_eventos_tui()
        else:
            print(Fore.RED + "Opción inválida, intenta de nuevo.")
            pause()

# ---------------- FUNCIONES TUI ---------------- #
def agregar_evento_tui():
    clear_screen()
    print(Fore.BLUE + Style.BRIGHT + "REGISTRAR NUEVO EVENTO".center(80) + Style.RESET_ALL)

    tipo = input("Tipo de evento: ")
    nombre = input("Nombre del cliente: ")
    carnet = input("Carnet de identidad: ")
    direccion = input("Dirección de domicilio: ")
    monto_garantia = float(input("Monto de garantía: "))
    monto_total = float(input("Monto total: "))
    dia = input("Fecha (YYYY-MM-DD): ")
    hora_fin = input("Hora de finalización (HH:MM): ")
    decoracion = input("¿Requiere decoración? (s/n): ").lower() == "s"

    agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
    print(Fore.GREEN + "\nEvento agregado con éxito.")
    pause()

def marcar_conflictos(eventos):
    fechas = [e.dia for e in eventos]
    conflictos = {f for f, c in Counter(fechas).items() if c > 1}
    for e in eventos:
        setattr(e, "conflicto", e.dia in conflictos)

def listar_eventos_tui():
    clear_screen()
    eventos = list(listar_eventos())

    # Orden por fecha
    eventos.sort(key=lambda x: x.dia)

    # Detectar conflictos
    marcar_conflictos(eventos)

    print(Fore.CYAN + Style.BRIGHT + "LISTA DE EVENTOS".center(80) + Style.RESET_ALL)

    if not eventos:
        print(Fore.YELLOW + "\nNo hay eventos registrados.\n")
        pause()
        return

    tabla = []
    for e in eventos:
        fila = [
            e.id,
            e.tipo,
            e.nombre,
            e.carnet,
            e.direccion_domicilio,
            e.monto_garantia,
            e.monto_total,
            e.dia,
            e.hora_fin,
            "Sí" if e.decoracion else "No"
        ]
        if e.conflicto:
            fila = [Fore.RED + str(x) + Style.RESET_ALL for x in fila]

        tabla.append(fila)

    print(tabulate(
        tabla,
        headers=["ID", "Tipo", "Nombre", "Carnet", "Dirección", "Garantía", "Total",
                 "Fecha", "Hora fin", "Decoración"],
        tablefmt="fancy_grid",
        stralign="center",
        numalign="center",
    ))
    print(Fore.RED + "\n⚠️  En rojo: eventos con conflicto de fecha.\n" + Style.RESET_ALL)
    pause()

def modificar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input(Fore.GREEN + "\nID del evento a modificar: " + Style.RESET_ALL))
        print("Deja en blanco si no quieres cambiar un campo.")
        tipo = input("Nuevo tipo: ")
        nombre = input("Nuevo nombre: ")
        carnet = input("Nuevo carnet: ")
        direccion = input("Nueva dirección: ")
        monto_garantia = input("Nueva garantía: ")
        monto_total = input("Nuevo total: ")
        dia = input("Nueva fecha (YYYY-MM-DD): ")
        hora_fin = input("Nueva hora fin (HH:MM): ")
        decoracion = input("Nueva decoración (s/n): ")

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
            print(Fore.GREEN + "\nEvento modificado con éxito.")
        else:
            print(Fore.RED + "\nNo se encontró el evento.")
    except ValueError:
        print(Fore.RED + "\nID inválido.")
    pause()

def eliminar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input(Fore.GREEN + "\nID del evento a eliminar: " + Style.RESET_ALL))
        if eliminar_evento(evento_id):
            print(Fore.GREEN + "\nEvento eliminado con éxito.")
        else:
            print(Fore.RED + "\nNo se encontró el evento.")
    except ValueError:
        print(Fore.RED + "\nID inválido.")
    pause()

# ---------------- EJECUCIÓN ---------------- #
if __name__ == "__main__":
    menu()

