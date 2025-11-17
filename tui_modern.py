
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Header, Footer
from textual.containers import Horizontal
from textual import events
from rich.text import Text

# Tus funciones clásicas
from tui import agregar_evento_tui, listar_eventos_tui, modificar_evento_tui, eliminar_evento_tui

class MenuVisualApp(App):

    CSS = """
    Button {
        width: 20;
        height: 3;
        margin: 1;
        border: round white;
        background: blue;
        color: white;
        content-align: center middle;
    }
    Button:focus {
        background: darkgreen;
        color: white;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        # Usamos Text para el título con formato
        titulo = Text("📅 SISTEMA DE EVENTOS - Selecciona una opción", style="bold cyan")
        yield Static(titulo)
        
        # Contenedor horizontal de botones
        with Horizontal():
            yield Button("➕ Registrar", id="registrar")
            yield Button("📋 Listar", id="listar")
            yield Button("✏️ Modificar", id="modificar")
            yield Button("❌ Eliminar", id="eliminar")
            yield Button("🚪 Salir", id="salir")
        
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        match button_id:
            case "registrar":
                agregar_evento_tui()
            case "listar":
                listar_eventos_tui()
            case "modificar":
                modificar_evento_tui()
            case "eliminar":
                eliminar_evento_tui()
            case "salir":
                self.exit()

    async def on_key(self, event: events.Key) -> None:
        # Salir también con Q o Escape
        if event.key in ("q", "escape"):
            self.exit()

if __name__ == "__main__":
    MenuVisualApp().run()
