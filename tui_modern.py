from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Center
from textual.message import Message
from rich.panel import Panel

# ------------------ TUI MODERNA ------------------ #
class MenuButton(Button):
    def __init__(self, label, action):
        super().__init__(label)
        self.action_key = action

class EventoApp(App):

    CSS_PATH = None  # No necesitamos CSS externo

    # Clase para manejar acciones de menú
    class MenuAction(Message):
        def __init__(self, action: str):
            super().__init__()
            self.action = action

    def compose(self) -> ComposeResult:
        # Header y mensaje de bienvenida
        yield Header(show_clock=True)
        yield Center(
            Static(Panel("[bold cyan]📅 SISTEMA DE EVENTOS\nSelecciona una opción", expand=False)),
        )

        # Botones del menú
        botones = [
            ("➕ Registrar evento", "registrar"),
            ("📋 Listar eventos", "listar"),
            ("✏️  Editar evento", "editar"),
            ("❌ Eliminar evento", "eliminar"),
            ("🚪 Salir", "salir"),
        ]

        for texto, accion in botones:
            yield Center(MenuButton(texto, accion))

        yield Footer()

    # Evento al presionar un botón
    def on_button_pressed(self, event: Button.Pressed):
        control = event.button
        if isinstance(control, MenuButton):
            # Lanza un mensaje con la acción del botón
            self.post_message(self.MenuAction(control.action_key))

    # Evento para manejar la acción seleccionada
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
                print("\n👋 Saliendo…")
                self.exit()

# ------------------ EJECUCIÓN ------------------ #
if __name__ == "__main__":
    EventoApp().run()
