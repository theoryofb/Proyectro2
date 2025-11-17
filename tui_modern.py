from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Horizontal
from textual import events
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime
from tabulate import tabulate
import os

class MenuVisualApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #title {
        height: 3;
        content-align: center middle;
    }
    Button {
        width: 20;
        margin: 1;
        border: round white;
        background: darkgreen;
        color: white;
    }
    Button:focus {
        background: green;
        color: black;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("📅 SISTEMA DE EVENTOS - Selecciona una opción", id="title")
        
        with Horizontal():
            yield Button("Registrar evento", id="registrar")
            yield Button("Listar eventos", id="listar")
            yield Button("Modificar evento", id="modificar")
            yield Button("Eliminar evento", id="eliminar")
            yield Button("Salir", id="salir")
        
        yield Footer()

    # ---------------- EVENT HANDLER ---------------- #
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "registrar":
            self.call_func("agregar")
        elif button_id == "listar":
            self.call_func("listar")
        elif button_id == "modificar":
            self.call_func("modificar")
        elif button_id == "eliminar":
            self.call_func("eliminar")
        elif button_id == "salir":
            self.exit()

    # ---------------- FUNCIONES ---------------- #
    def call_func(self, action):
        if action == "listar":
            self.listar_eventos()
        else:
            # Para agregar/modificar/eliminar todavía usamos consola
            os.system(f"python tui.py")

    def listar_eventos(self):
        eventos = listar_eventos()
        if not eventos:
            print("\nNo hay eventos registrados.\n")
            input("Presiona Enter para continuar...")
            return

        # Ordenar por fecha
        eventos = sorted(eventos, key=lambda e: e.dia)

        # Mostrar tabla
        tabla = [[
            e.id, e.tipo, e.nombre, e.carnet, e.direccion_domicilio,
            e.monto_garantia, e.monto_total, e.dia, e.hora_fin,
            "Sí" if e.decoracion else "No"
        ] for e in eventos]

        print("\n" + tabulate(tabla,
                             headers=["ID", "Tipo", "Nombre", "Carnet", "Dirección",
                                      "Garantía", "Total", "Fecha", "Hora fin", "Decoración"],
                             tablefmt="fancy_grid"))
        input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    app = MenuVisualApp()
    app.run()
