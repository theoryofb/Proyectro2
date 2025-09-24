import urwid
from datetime import date
from database import inicializar_db, agregar_evento, listar_eventos, agregar_participante, listar_participantes

# -----------------------------------------------------------
# Funciones de cada opción del menú
# -----------------------------------------------------------
def mostrar_eventos(button):
    listar_eventos()
    main.original_widget = menu_principal()

def crear_evento(button):
    def on_save(edit, text):
        if text.strip():
            agregar_evento(text.strip())
        main.original_widget = menu_principal()

    main.original_widget = urwid.Filler(
        urwid.Pile([
            urwid.Text("📌 Escribe el nombre del evento:"),
            urwid.Edit(caption="> ", edit_text=""),
            urwid.Button("Guardar", on_press=lambda b: on_save(None, edit.get_edit_text())),
        ])
    )
    edit = main.original_widget.base_widget.contents[1][0]  # capturar el Edit


def mostrar_participantes(button):
    listar_participantes()
    main.original_widget = menu_principal()

def crear_participante(button):
    def on_save(edit, text):
        datos = text.split(",")
        if len(datos) == 5:
            carnet, nombre, celular, fecha_txt, id_evento = [d.strip() for d in datos]
            try:
                fecha_evento = date.fromisoformat(fecha_txt)
                agregar_participante(carnet, nombre, celular, fecha_evento, int(id_evento))
            except Exception as e:
                print("⚠️ Error:", e)
        else:
            print("⚠️ Debes ingresar: carnet,nombre,celular,YYYY-MM-DD,id_evento")

        main.original_widget = menu_principal()

    main.original_widget = urwid.Filler(
        urwid.Pile([
            urwid.Text("📌 Ingresa los datos separados por comas:"),
            urwid.Text("Formato: carnet,nombre,celular,YYYY-MM-DD,id_evento"),
            urwid.Edit(caption="> "),
            urwid.Button("Guardar", on_press=lambda b: on_save(None, edit.get_edit_text())),
        ])
    )
    edit = main.original_widget.base_widget.contents[2][0]  # capturar el Edit


# -----------------------------------------------------------
# Menú principal
# -----------------------------------------------------------
def menu_principal():
    opciones = [
        ("Listar eventos", mostrar_eventos),
        ("Agregar evento", crear_evento),
        ("Listar participantes", mostrar_participantes),
        ("Agregar participante", crear_participante),
        ("Salir", exit),
    ]
    body = [urwid.Text("📋 Menú principal"), urwid.Divider()]
    for texto, funcion in opciones:
        button = urwid.Button(texto)
        urwid.connect_signal(button, 'click', funcion)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


# -----------------------------------------------------------
# Inicio de la TUI
# -----------------------------------------------------------
if __name__ == "__main__":
    inicializar_db()
    main = urwid.Padding(menu_principal(), left=2, right=2)
    loop = urwid.MainLoop(main, palette=[('reversed', 'standout', '')])
    loop.run()
