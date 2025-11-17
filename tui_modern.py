from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Button, Static, Input, Checkbox, Select, DataTable
)
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from datetime import datetime
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento

# -------------------------------------------------------
# 🔷 FORMULARIO DE REGISTRO / MODIFICACIÓN (OPCIONAL)
# -------------------------------------------------------
# Puedes mantenerlo si quieres agregar eventos desde la app
class FormScreen(Screen):

    def __init__(self, editar=False, evento=None):
        super().__init__()
        self.editar = editar
        self.evento = evento

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            "✍ REGISTRAR EVENTO" if not self.editar else "✏ MODIFICAR EVENTO",
            id="title"
        )

        yield Input(placeholder="Nombre del cliente", id="nombre")
        yield Input(placeholder="Carnet", id="carnet")

        yield Select(
            options=[
                ("cumpleanos", "Cumpleaños"),
                ("boda", "Boda"),
                ("graduacion", "Graduación"),
                ("infantil", "Fiesta infantil"),
                ("baby", "Baby Shower"),
                ("corporativo", "Corporativo"),
                ("otro", "Otro")
            ],
            id="tipo"
        )

        yield Input(placeholder="Monto garantía", id="garantia")
        yield Input(placeholder="Monto total", id="total")
        yield Input(placeholder="Fecha YYYY-MM-DD", id="dia")
        yield Input(placeholder="Hora fin HH:MM", id="hora")
        yield Checkbox("¿Requiere decoración?", id="decoracion")

        yield Horizontal(
            Button("💾 Guardar", id="guardar", variant="success"),
            Button("⬅ Volver", id="volver", variant="error"),
            id="botones"
        )

        yield Footer()

    def on_mount(self):
        if self.editar and self.evento:
            self.query_one("#nombre").value = self.evento.nombre
            self.query_one("#carnet").value = self.evento.carnet
            self.query_one("#tipo").value = self.evento.tipo
            self.query_one("#garantia").value = str(self.evento.monto_garantia)
            self.query_one("#total").value = str(self.evento.monto_total)
            self.query_one("#dia").value = str(self.evento.dia)
            self.query_one("#hora").value = str(self.evento.hora_fin)
            self.query_one("#decoracion").value = self.evento.decoracion

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "volver":
            self.app.pop_screen()
            return

        datos = {
            "nombre": self.query_one("#nombre").value,
            "carnet": self.query_one("#carnet").value,
            "tipo": self.query_one("#tipo").value,
            "monto_garantia": float(self.query_one("#garantia").value),
            "monto_total": float(self.query_one("#total").value),
            "dia": datetime.strptime(self.query_one("#dia").value, "%Y-%m-%d").date(),
            "hora_fin": datetime.strptime(self.query_one("#hora").value, "%H:%M").time(),
            "decoracion": self.query_one("#decoracion").value
        }

        if self.editar:
            modificar_evento(self.evento.id, **datos)
        else:
            agregar_evento(**datos)

        self.app.pop_screen()


# -------------------------------------------------------
# 🔷 FORMULARIO PARA ELIMINAR EVENTO POR ID
# -------------------------------------------------------
class EliminarEventoScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("❌ ELIMINAR EVENTO", id="title")

        yield Input(placeholder="Ingrese ID del evento a eliminar", id="event_id")

        yield Horizontal(
            Button("🗑 Eliminar", id="eliminar", variant="error"),
            Button("⬅ Volver", id="volver", variant="primary"),
            id="botones"
        )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "volver":
            self.app.pop_screen()
            return
        if event.button.id == "eliminar":
            event_id_str = self.query_one("#event_id").value
            if event_id_str.isdigit():
                event_id = int(event_id_str)
                eliminar_evento(event_id)
                self.app.pop_screen()
            else:
                self.query_one("#event_id").placeholder = "ID inválido, ingrese un número"


# -------------------------------------------------------
# 🔷 MENÚ PRINCIPAL
# -------------------------------------------------------
class ModernApp(App):

    CSS = """
    #title {
        padding: 1;
        text-align: center;
        color: yellow;
    }
    """

    BINDINGS = [("q", "quit", "Salir")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🌟 SISTEMA DE EVENTOS 🌟", id="title")

        yield Vertical(
            Button("❌ Eliminar evento", id="del", variant="error"),
            Button("🚪 Salir", id="quitbtn", variant="error"),
            id="menu"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "del":
            self.push_screen(EliminarEventoScreen())
        elif event.button.id == "quitbtn":
            self.exit()


# -------------------------------------------------------
# 🚀 EJECUCIÓN
# -------------------------------------------------------
if __name__ == "__main__":
    ModernApp().run()

