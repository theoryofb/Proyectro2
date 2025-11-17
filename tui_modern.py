from textual.app import App
from textual.widgets import Static
from textual import events
from rich.text import Text
from rich.console import Console

# Importar tus funciones clásicas
from tui import agregar_evento_tui, listar_eventos_tui, modificar_evento_tui, eliminar_evento_tui

console = Console()

class MenuVisualApp(App):
    def compose(self):
        # Crear botones visuales en fila con colores
        botones = [
            ("➕ Registrar", "registrar"),
            ("📋 Listar", "listar"),
            ("✏️ Modificar", "modificar"),
            ("❌ Eliminar", "eliminar"),
            ("🚪 Salir", "salir")
        ]

        texto_botones = Text()
        for b, _ in botones:
            texto_botones.append(f" {b} ", style="bold white on blue")
            texto_botones.append("  ")  # Espacio entre botones

        yield Static(texto_botones, expand=True)

    async def on_key(self, event: events.Key):
        # Asignamos teclas para “presionar” botones
        if event.key == "1":
            agregar_evento_tui()
        elif event.key == "2":
            listar_eventos_tui()
        elif event.key == "3":
            modificar_evento_tui()
        elif event.key == "4":
            eliminar_evento_tui()
        elif event.key in ("5", "q", "escape"):
            self.exit()

if __name__ == "__main__":
    MenuVisualApp().run()
