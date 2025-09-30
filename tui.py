import os
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# ---------------- FUNCIONES AUXILIARES ---------------- #
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(Fore.MAGENTA + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

# ---------------- MENÚ PRINCIPAL ---------------- #
def menu():
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "═" * 100)
        print("🎉  GESTIÓN DE EVENTOS  🎉".center(100))
        print("═" * 100 + Style.RESET_ALL)

        print(Fore.YELLOW + "1️⃣  Agregar evento")
        print("2️⃣  Modificar evento")
        print("3️⃣  Eliminar evento")
        print("4️⃣  Listar eventos")
        print("5️⃣  Salir" + Style.RESET_ALL)

        opcion = input(Fore.GREEN + "\n👉 Selecciona una opción: " + Style.RESET_ALL)

        if opcion == "1":
            agregar_evento_tui()
        elif opcion == "2":
            modificar_evento_tui()
        elif opcion == "3":
            eliminar_evento_tui()
        elif opcion == "4":
            listar_eventos_tui()
        elif opcion == "5":
            print(Fore.MAGENTA + "👋 Saliendo del sistema...")
            break
        else:
            print(Fore.RED + "⚠️ Opción inválida, intenta de nuevo.")
            pause()

# ---------------- FUNCIONES TUI ---------------- #
def agregar_evento_tui():
    clear_screen()
    print(Fore.BLUE + Style.BRIGHT + "➕  REGISTRAR NUEVO EVENTO".center(100) + Style.RESET_ALL)
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
    print(Fore.GREEN + "\n✅ Evento agregado con éxito.")
    pause()

def listar_eventos_tui():
    clear_screen()
    eventos = listar_eventos()
    print(Fore.CYAN + Style.BRIGHT + "📋  LISTA DE EVENTOS".center(100) + Style.RESET_ALL)
    if not eventos:
        print(Fore.YELLOW + "\nNo hay eventos registrados.\n")
        pause()
        return

    tabla = [[e.id, e.tipo, e.nombre, e.carnet, e.direccion_domicilio,
              e.monto_garantia, e.monto_total, e.dia, e.hora_fin,
              "Sí" if e.decoracion else "No"] for e in eventos]

    print(tabulate(tabla, headers=["ID","Tipo","Nombre","Carnet","Dirección","Garantía","Total","Fecha","Hora fin","Decoración"], 
                   tablefmt="fancy_grid", stralign="center", numalign="center"))
    pause()

def modificar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input(Fore.GREEN + "\n✏️ ID del evento a modificar: " + Style.RESET_ALL))
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
            print(Fore.GREEN + "\n✅ Evento modificado con éxito.")
        else:
            print(Fore.RED + "\n❌ No se encontró el evento.")
    except ValueError:
        print(Fore.RED + "\n⚠️ ID inválido.")
    pause()

def eliminar_evento_tui():
    listar_eventos_tui()
    try:
        evento_id = int(input(Fore.GREEN + "\n🗑️ ID del evento a eliminar: " + Style.RESET_ALL))
        if eliminar_evento(evento_id):
            print(Fore.GREEN + "\n✅ Evento eliminado con éxito.")
        else:
            print(Fore.RED + "\n❌ No se encontró el evento.")
    except ValueError:
        print(Fore.RED + "\n⚠️ ID inválido.")
    pause()

# ---------------- EJECUCIÓN ---------------- #
if __name__ == "__main__":
    menu()
