from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, TextLog
from textual.containers import Vertical, Horizontal
from datetime import datetime
from database import listar_eventos
from tabulate import tabulate


class MenuVisualApp(App):

    ### 🔹 ESTILOS MODERNOS
    CSS = """
    Screen {
        align: center middle;
    }

    #banner {
        text-align: center;
        height: 4;
        background: yellow;
        color: black;
        content-align: center middle;
        margin-bottom: 2;
        border: double black;
    }

    Button {
        width: 22;
        margin: 1;
        border: round white;
        background: darkgreen;
        color: white;
    }
    Button:focus {
        background: green;
        color: black;
    }

    #log {
        height: 20;
        width: 100%;
        border: round cyan;
        margin-top: 2;
    }
    """

    ### 🔹 ATAJOS DE TECLADO
    BINDINGS = [
        ("l", "listar", "Listar eventos"),
        ("q", "quit", "Salir"),
    ]

    ### ---------------- UI ---------------- ###
    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        yield Static("🌟 BIENVENIDO AL SISTEMA DE EVENTOS 🌟", id="banner")

        with Horizontal():
            yield Button("Registrar evento", id="registrar")
            yield Button("Listar eventos", id="listar")
            yield Button("Modificar evento", id="modificar")
            yield Button("Eliminar evento", id="eliminar")
            yield Button("🚪 Salir", id="salir")

        yield TextLog(id="log", highlight=True)

        yield Footer()

    ### ---------------- EVENTOS ---------------- ###

    def on_button_pressed(self, event: Button.Pressed) -> None:
        botones = {
            "listar": self.action_listar,
            "salir": self.action_quit
        }

        if event.button.id in botones:
            botones[event.button.id]()
        else:
            self.show_in_console(event.button.id)

    ### 🔹 Acción LISTAR dentro de la TUI
    def action_listar(self):
        eventos = listar_eventos()

        log = self.query_one("#log", TextLog)
        log.clear()

        if not eventos:
            log.write("⚠ No hay eventos registrados.")
            return

        eventos = sorted(eventos, key=lambda e: e.dia)

        tabla = [
            [e.id, e.tipo, e.nombre, e.carnet, e.direccion_domicilio,
             e.monto_garantia, e.monto_total, e.dia, e.hora_fin,
             "Sí" if e.decoracion else "No"]
            for e in eventos
        ]

        text = tabulate(
            tabla,
            headers=["ID", "Tipo", "Nombre", "Carnet", "Dirección",
                     "Garantía", "Total", "Fecha", "Fin", "Deco"],
            tablefmt="fancy_grid"
        )

        for line in text.split("\n"):
            log.write(line)

        log.write("\n💡 Usa Q para salir")

    ### 🔹 Abrir otras funciones en consola mientras las migramos
    def show_in_console(self, action):
        log = self.query_one("#log", TextLog)
        log.write(f"⚠ Esta función aún no está en la TUI ({action})")
        log.write("➡ Se abrirá en modo consola...")
        import os
        os.system("python tui.py")

    ### 🔹 Acción SALIR
    def action_quit(self):
        self.exit()


if __name__ == "__main__":
    MenuVisualApp().run()
