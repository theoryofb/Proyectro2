from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from database import eliminar_evento

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
                # Mensaje simple de error
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
