from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Input, Label, DataTable, Checkbox, Select
from textual.containers import Horizontal, Vertical, Container
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime

TIPOS_EVENTO = ["Cumpleaños", "Boda", "Graduación", "Otro"]

class TUIApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #title {
        height: 5;
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
    DataTable {
        height: auto;
        width: 100%;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🎉 BIENVENIDO AL SISTEMA DE EVENTOS 🎉", id="title")

        with Horizontal():
            yield Button("Registrar evento", id="registrar")
            yield Button("Listar eventos", id="listar")
            yield Button("Modificar evento", id="modificar")
            yield Button("Eliminar evento", id="eliminar")
            yield Button("Salir", id="salir")

        yield Footer()

    # ---------------- EVENT HANDLER ---------------- #
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "registrar":
            await self.show_registrar()
        elif button_id == "listar":
            await self.show_listar()
        elif button_id == "modificar":
            await self.show_modificar()
        elif button_id == "eliminar":
            await self.show_eliminar()
        elif button_id == "salir":
            self.exit()

    # ---------------- FUNCIONES ---------------- #
    async def show_registrar(self):
        self.clear_screen_widgets()
        self.registrar_container = Vertical()
        self.mount(self.registrar_container)

        self.registrar_container.mount(Label("Registrar Evento", id="subtitulo"))
        self.tipo_select = Select(TIPOS_EVENTO, prompt="Tipo de evento")
        self.registrar_container.mount(self.tipo_select)
        self.nombre_input = Input(placeholder="Nombre del cliente")
        self.registrar_container.mount(self.nombre_input)
        self.carnet_input = Input(placeholder="Carnet de identidad")
        self.registrar_container.mount(self.carnet_input)
        self.direccion_input = Input(placeholder="Dirección de domicilio")
        self.registrar_container.mount(self.direccion_input)
        self.monto_garantia_input = Input(placeholder="Monto de garantía")
        self.registrar_container.mount(self.monto_garantia_input)
        self.monto_total_input = Input(placeholder="Monto total")
        self.registrar_container.mount(self.monto_total_input)
        self.fecha_input = Input(placeholder="Fecha (YYYY-MM-DD)")
        self.registrar_container.mount(self.fecha_input)
        self.hora_input = Input(placeholder="Hora fin (HH:MM)")
        self.registrar_container.mount(self.hora_input)
        self.decoracion_checkbox = Checkbox(label="¿Requiere decoración?")
        self.registrar_container.mount(self.decoracion_checkbox)

        self.registrar_container.mount(Button("Guardar", id="guardar_registro"))
        self.registrar_container.mount(Button("Volver", id="volver_menu"))

    async def show_listar(self):
        self.clear_screen_widgets()
        eventos = list(listar_eventos())
        if not eventos:
            self.mount(Label("No hay eventos registrados."))
            return

        eventos.sort(key=lambda e: e.dia)

        fechas = {}
        for e in eventos:
            fechas.setdefault(e.dia, []).append(e)

        tabla = DataTable()
        tabla.add_columns("ID", "Tipo", "Nombre", "Carnet", "Fecha", "Hora fin", "Decoración")
        for e in eventos:
            fila_index = tabla.add_row(
                str(e.id), e.tipo, e.nombre, e.carnet,
                str(e.dia), str(e.hora_fin),
                "Sí" if e.decoracion else "No"
            )
            if len(fechas[e.dia]) > 1:
                for col in range(len(tabla.columns)):
                    tabla.set_cell_style(fila_index, col, "bold red")

        self.mount(tabla)
        self.mount(Button("Volver", id="volver_menu"))

    async def show_modificar(self):
        self.clear_screen_widgets()
        self.mount(Label("Modificar evento aún usa consola (tui.py) por simplicidad."))
        import os
        os.system("python tui.py")
        self.mount(Button("Volver", id="volver_menu"))

    async def show_eliminar(self):
        self.clear_screen_widgets()
        self.mount(Label("Eliminar evento aún usa consola (tui.py) por simplicidad."))
        import os
        os.system("python tui.py")
        self.mount(Button("Volver", id="volver_menu"))

    # ---------------- HELPERS ---------------- #
    def clear_screen_widgets(self):
        for child in self.query(Static) + self.query(Vertical) + self.query(DataTable) + self.query(Label) + self.query(Input) + self.query(Checkbox):
            child.remove()

    async def on_button_pressed_guardar_registro(self, event):
        tipo = self.tipo_select.value
        nombre = self.nombre_input.value
        carnet = self.carnet_input.value
        direccion = self.direccion_input.value
        monto_garantia = float(self.monto_garantia_input.value)
        monto_total = float(self.monto_total_input.value)
        dia = self.fecha_input.value
        hora_fin = self.hora_input.value
        decoracion = self.decoracion_checkbox.value

        agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
        self.clear_screen_widgets()
        self.mount(Label("✅ Evento agregado con éxito."))
        self.mount(Button("Volver", id="volver_menu"))

    async def on_button_pressed_volver_menu(self, event):
        self.clear_screen_widgets()

if __name__ == "__main__":
    app = TUIApp()
    app.run()
