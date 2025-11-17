from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Horizontal
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        match button_id:
            case "registrar":
                os.system("python tui.py")
            case "listar":
                os.system("python tui.py")
            case "modificar":
                os.system("python tui.py")
            case "eliminar":
                os.system("python tui.py")
            case "salir":
                self.exit()

if __name__ == "__main__":
    app = MenuVisualApp()
    app.run()
