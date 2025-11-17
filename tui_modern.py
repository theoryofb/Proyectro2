from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static, DataTable, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message
from datetime import datetime
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from rich.panel import Panel
from rich.text import Text

# ------------------ BOTÓN DE MENÚ ------------------ #
class MenuButton(Button):
    def __init__(self, label: str, action: str):
        super().__init__(label)
        self.action_key = action
        self.can_focus = True

# ------------------ APLICACIÓN ------------------ #
class EventoApp(App):

    CSS_PATH = None
    BINDINGS = [("q", "exit", "Salir")]

    class MenuAction(Message):
        def __init__(self, action: str):
            super().__init__()
            self.action = action

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(Panel("[bold cyan]📅 SISTEMA DE EVENTOS\nSelecciona una opción", expand=False))
        
        # Menú principal
        with Vertical():
            botones = [
                ("➕ Registrar evento", "registrar"),
                ("📋 Listar eventos", "listar"),
                ("✏️ Editar evento", "editar"),
                ("❌ Eliminar evento", "eliminar"),
                ("🚪 Salir", "salir"),
            ]
            for texto, accion in botones:
                yield MenuButton(texto, accion)

        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed):
        control = event.button
        if isinstance(control, MenuButton):
            self.post_message(self.MenuAction(control.action_key))

    async def on_menu_action(self, message: "MenuAction"):
        match message.action:
            case "registrar":
                await self.show_agregar_evento()
            case "listar":
                await self.show_listar_eventos()
            case "editar":
                await self.show_modificar_evento()
            case "eliminar":
                await self.show_eliminar_evento()
            case "salir":
                self.exit()

    # ---------------- FUNCIONES DE LA TUI ---------------- #
    async def show_agregar_evento(self):
        self.clear()
        await self.view.dock(Header(show_clock=True), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        container = Vertical()
        self.inputs = {}
        fields = ["Tipo", "Nombre", "Carnet", "Dirección", "Monto garantía", "Monto total", "Fecha (YYYY-MM-DD)", "Hora fin (HH:MM)", "Decoración (s/n)"]
        for f in fields:
            input_widget = Input(placeholder=f)
            container.mount(Label(f))
            container.mount(input_widget)
            self.inputs[f] = input_widget

        btn_guardar = Button("Guardar", id="guardar")
        container.mount(btn_guardar)
        await self.view.dock(container)

    async def show_listar_eventos(self):
        self.clear()
        await self.view.dock(Header(show_clock=True), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        eventos = listar_eventos()
        tabla = DataTable()
        headers = ["ID", "Tipo", "Nombre", "Carnet", "Dirección", "Garantía", "Total", "Fecha", "Hora fin", "Decoración"]
        tabla.add_columns(*headers)

        # Detectar conflictos de fecha
        fechas = [str(e.dia) for e in eventos]
        duplicadas = {f for f in fechas if fechas.count(f) > 1}

        for e in eventos:
            row = [
                e.id, e.tipo, e.nombre, e.carnet, e.direccion_domicilio,
                e.monto_garantia, e.monto_total, e.dia, e.hora_fin,
                "Sí" if e.decoracion else "No"
            ]
            if str(e.dia) in duplicadas:
                row = [Text(str(x), style="bold red") for x in row]
            tabla.add_row(*row)
        await self.view.dock(tabla)

    async def show_modificar_evento(self):
        # Por simplificar, podemos usar la misma forma que agregar y pedir ID primero
        pass

    async def show_eliminar_evento(self):
        # Por simplificar, podemos pedir ID en un Input y ejecutar eliminar_evento
        pass

if __name__ == "__main__":
    EventoApp().run()
