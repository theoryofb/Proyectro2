from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, DataTable, Checkbox, Select, Input
from textual.containers import Horizontal, Vertical
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
            await self.registrar_evento()
        elif button_id == "listar":
            await self.listar_eventos()
        elif button_id == "modificar":
            await self.modificar_evento()
        elif button_id == "eliminar":
            await self.eliminar_evento()
        elif button_id == "salir":
            self.exit()

    # ---------------- FUNCIONES ---------------- #
    async def registrar_evento(self):
        self.clear()
        # Selección de tipo de evento
        tipo = await self.input_dialog("Tipo de evento", TIPOS_EVENTO)
        nombre = await self.simple_input("Nombre del cliente")
        carnet = await self.simple_input("Carnet de identidad")
        direccion = await self.simple_input("Dirección de domicilio")
        monto_garantia = float(await self.simple_input("Monto de garantía"))
        monto_total = float(await self.simple_input("Monto total"))
        dia = await self.simple_input("Fecha (YYYY-MM-DD)")
        hora_fin = await self.simple_input("Hora de finalización (HH:MM)")
        decoracion = await self.checkbox_input("¿Requiere decoración?")

        agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
        await self.message_box("✅ Evento agregado con éxito.")

    async def listar_eventos(self):
        self.clear()
        eventos = list(listar_eventos())
        if not eventos:
            await self.message_box("No hay eventos registrados.")
            return

        # Ordenar por fecha
        eventos.sort(key=lambda e: e.dia)

        # Detectar conflictos
        fechas = {}
        for e in eventos:
            fechas.setdefault(e.dia, []).append(e)

        # Crear tabla
        tabla = DataTable()
        tabla.add_columns("ID", "Tipo", "Nombre", "Carnet", "Fecha", "Hora fin", "Decoración")

        for e in eventos:
            fila_index = tabla.add_row(
                str(e.id), e.tipo, e.nombre, e.carnet,
                str(e.dia), str(e.hora_fin),
                "Sí" if e.decoracion else "No"
            )
            # Resaltar conflictos
            if len(fechas[e.dia]) > 1:
                for col in range(len(tabla.columns)):
                    tabla.set_cell_style(fila_index, col, "bold red")

        await self.mount(tabla)
        await self.message_box("⚠️ Eventos en rojo tienen conflicto de fecha. Presiona Enter para volver al menú.")

    async def modificar_evento(self):
        await self.message_box("Modificar evento actualmente usa consola (tui.py).")
        import os
        os.system("python tui.py")

    async def eliminar_evento(self):
        await self.message_box("Eliminar evento actualmente usa consola (tui.py).")
        import os
        os.system("python tui.py")

    # ---------------- HELPERS ---------------- #
    async def input_dialog(self, prompt, opciones):
        print(f"{prompt}:")
        for i, val in enumerate(opciones, 1):
            print(f"{i}. {val}")
        choice = int(input("Selecciona opción: "))
        return opciones[choice - 1]

    async def simple_input(self, prompt):
        return input(f"{prompt}: ")

    async def checkbox_input(self, prompt):
        val = input(f"{prompt} (s/n): ").lower()
        return val == "s"

    async def message_box(self, mensaje):
        print("\n" + mensaje)
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    app = TUIApp()
    app.run()
