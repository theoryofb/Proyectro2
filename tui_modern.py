from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Button, Static, Input, Checkbox, Select, DataTable
)
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from datetime import datetime
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento

# -------------------------------------------------------
# 🔷 FORMULARIO DE REGISTRO / MODIFICACIÓN
# -------------------------------------------------------
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
        yield Input(placeholder="Dirección", id="direccion")

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
            self.query_one("#direccion").value = self.evento.direccion_domicilio
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
            "direccion_domicilio": self.query_one("#direccion").value,
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
# 🔷 LISTA DE EVENTOS
# -------------------------------------------------------
class ListaEventos(Screen):

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("📋 LISTA DE EVENTOS", id="title")
        self.tabla = DataTable(id="tabla")
        yield self.tabla
        yield Footer()

    def on_mount(self):
        self.tabla.add_columns(
            "ID", "Tipo", "Nombre", "Carnet", "Fecha", "Hora", "Decoración"
        )

        eventos = list(listar_eventos())
        eventos.sort(key=lambda e: e.dia)

        fechas = {}
        for e in eventos:
            fechas.setdefault(e.dia, []).append(e)

        for e in eventos:
            conflicto = len(fechas[e.dia]) > 1
            # En versiones modernas de textual, DataTable no acepta style en add_row
            self.tabla.add_row(
                str(e.id), e.tipo, e.nombre, e.carnet,
                str(e.dia), str(e.hora_fin),
                "Sí" if e.decoracion else "No"
            )
            if conflicto:
                fila_index = len(self.tabla.rows) - 1
                for col_index in range(len(self.tabla.columns)):
                    self.tabla.get_row(fila_index).cells[col_index].style = "bold red"

    def key_e(self):
        fila = self.tabla.cursor_row
        if fila is None:
            return
        event_id = int(self.tabla.rows[fila].cells[0].value)
        evento = next(e for e in listar_eventos() if e.id == event_id)
        self.app.push_screen(FormScreen(editar=True, evento=evento))

    def key_d(self):
        fila = self.tabla.cursor_row
        if fila is None:
            return
        event_id = int(self.tabla.rows[fila].cells[0].value)
        eliminar_evento(event_id)
        self.app.push_screen(ListaEventos())


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

    BINDINGS = [
        ("q", "quit", "Salir"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🌟 BIENVENIDO AL SISTEMA DE EVENTOS 🌟", id="title")

        yield Vertical(
            Button("➕ Registrar evento", id="add", variant="success"),
            Button("📋 Ver eventos", id="list", variant="primary"),
            Button("❌ Salir", id="quitbtn", variant="error"),
            id="menu"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add":
            self.push_screen(FormScreen())
        elif event.button.id == "list":
            self.push_screen(ListaEventos())
        elif event.button.id == "quitbtn":
            self.exit()


# -------------------------------------------------------
# 🚀 EJECUCIÓN
# -------------------------------------------------------
if __name__ == "__main__":
    ModernApp().run()

