from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, Input, DataTable, Checkbox, Select
from textual.containers import Horizontal, Vertical
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime

TIPOS_EVENTO = [
    ("cumpleanos", "Cumpleaños"),
    ("boda", "Boda"),
    ("graduacion", "Graduación"),
    ("otro", "Otro")
]

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

        self.tipo_select = Select(TIPOS_EVENTO, prompt="Tipo de evento")
        self.nombre_input = Input(placeholder="Nombre del cliente")
        self.carnet_input = Input(placeholder="Carnet de identidad")
        self.direccion_input = Input(placeholder="Dirección de domicilio")
        self.garantia_input = Input(placeholder="Monto de garantía")
        self.total_input = Input(placeholder="Monto total")
        self.fecha_input = Input(placeholder="Fecha (YYYY-MM-DD)")
        self.hora_input = Input(placeholder="Hora fin (HH:MM)")
        self.decoracion_checkbox = Checkbox(label="Requiere decoración")

        # Botón para guardar
        self.guardar_btn = Button("Guardar", id="guardar_registro")

        for widget in [
            self.tipo_select, self.nombre_input, self.carnet_input,
            self.direccion_input, self.garantia_input, self.total_input,
            self.fecha_input, self.hora_input, self.decoracion_checkbox,
            self.guardar_btn
        ]:
            self.registrar_container.mount(widget)

        self.guardar_btn.on_click(self.on_guardar_registro)

    async def on_guardar_registro(self, event):
        tipo = self.tipo_select.value
        nombre = self.nombre_input.value
        carnet = self.carnet_input.value
        direccion = self.direccion_input.value
        monto_garantia = float(self.garantia_input.value)
        monto_total = float(self.total_input.value)
        dia = self.fecha_input.value
        hora_fin = self.hora_input.value
        decoracion = self.decoracion_checkbox.value

        agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
        await self.message_box("Evento agregado con éxito.")

    async def show_listar(self):
        self.clear_screen_widgets()
        eventos = list(listar_eventos())
        if not eventos:
            await self.message_box("No hay eventos registrados.")
            return

        eventos.sort(key=lambda e: e.dia)
        fechas = {}
        for e in eventos:
            fechas.setdefault(e.dia, []).append(e)

        self.tabla = DataTable()
        self.tabla.add_columns("ID", "Tipo", "Nombre", "Carnet", "Fecha", "Hora", "Decoración")
        for e in eventos:
            row_index = self.tabla.add_row(
                str(e.id), e.tipo, e.nombre, e.carnet,
                str(e.dia), str(e.hora_fin),
                "Sí" if e.decoracion else "No"
            )
            if len(fechas[e.dia]) > 1:
                for col in range(len(self.tabla.columns)):
                    self.tabla.set_cell_style(row_index, col, "bold red")

        self.mount(self.tabla)
        await self.message_box("Presiona Enter para volver al menú.")

    async def show_modificar(self):
        await self.message_box("Modificar evento aún usa consola (tui.py) por simplicidad.")

    async def show_eliminar(self):
        await self.message_box("Eliminar evento aún usa consola (tui.py) por simplicidad.")

    # ---------------- HELPERS ---------------- #
    def clear_screen_widgets(self):
        for child in self.query(Static) + self.query(Vertical) + self.query(DataTable) + self.query(Checkbox) + self.query(Input) + self.query(Select) + self.query(Button):
            child.remove()

    async def message_box(self, mensaje):
        print("\n" + mensaje)
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    app = TUIApp()
    app.run()

