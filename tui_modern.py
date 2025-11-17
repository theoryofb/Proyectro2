from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical
from textual.message import Message
from textual import events
from rich.panel import Panel

class MenuButton(Button):
    def __init__(self, label, action):
        super().__init__(label)
        self.action_key = action
        self.can_focus = True  # Asegura que pueda recibir foco

class EventoApp(App):

    CSS_PATH = None

    class MenuAction(Message):
        def __init__(self, action: str):
            super().__init__()
            self.action = action

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(Panel("[bold cyan]📅 SISTEMA DE EVENTOS\nSelecciona una opción", expand=False))

        # Botones verticales
        with Vertical():
            botones = [
                ("➕ Registrar evento", "registrar"),
                ("📋 Listar eventos", "listar"),
                ("✏️  Editar evento", "editar"),
                ("❌ Eliminar evento", "eliminar"),
                ("🚪 Salir", "salir"),
            ]
            for texto, accion in botones:
                yield MenuButton(texto, accion)

        yield Footer()

    # Capturar Enter explícitamente
    async def on_key(self, event: events.Key):
        if event.key == "enter":
            focused = self.focused
            if isinstance(focused, MenuButton):
                self.post_message(self.MenuAction(focused.action_key))
        elif event.key in ("q", "escape"):
            self.exit()

    def on_menu_action(self, message: "MenuAction"):
        match message.action:
            case "registrar":
                from tui import agregar_evento_tui
                agregar_evento_tui()
            case "listar":
                from tui import listar_eventos_tui
                listar_eventos_tui()
            case "editar":
                from tui import modificar_evento_tui
                modificar_evento_tui()
            case "eliminar":
                from tui import eliminar_evento_tui
                eliminar_evento_tui()
            case "salir":
                self.exit()

if __name__ == "__main__":
    EventoApp().run()
