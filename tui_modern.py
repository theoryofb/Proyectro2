from textual.app import App
from textual.widgets import Static
from textual import events

from tui import agregar_evento_tui, listar_eventos_tui  # tus funciones clásicas

class MenuVisualApp(App):

    botones = ["➕ Registrar evento", "📋 Listar eventos", "✏️ Editar evento", "❌ Eliminar evento", "🚪 Salir"]
    acciones = ["registrar", "listar", "editar", "eliminar", "salir"]

    def compose(self):
        texto = "\n".join(f"[cyan]{b}[/cyan]" for b in self.botones)
        yield Static(texto, expand=True)

    async def on_key(self, event: events.Key):
        if event.key == "1":
            agregar_evento_tui()   # Función clásica
        elif event.key == "2":
            listar_eventos_tui()
        elif event.key == "3":
            from tui import modificar_evento_tui
            modificar_evento_tui()
        elif event.key == "4":
            from tui import eliminar_evento_tui
            eliminar_evento_tui()
        elif event.key in ("5", "q", "escape"):
            self.exit()

if __name__ == "__main__":
    MenuVisualApp().run()
