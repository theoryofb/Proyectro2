import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento
from datetime import datetime

# ---------------- FUNCIONES ---------------- #
def agregar_evento_gui():
    tipo = simpledialog.askstring("Tipo de evento", "🎂 Tipo de evento:")
    if not tipo: return
    nombre = simpledialog.askstring("Nombre", "👤 Nombre del cliente:")
    if not nombre: return
    carnet = simpledialog.askstring("Carnet", "🪪 Carnet de identidad:")
    if not carnet: return
    direccion = simpledialog.askstring("Dirección", "🏠 Dirección de domicilio:")
    if not direccion: return
    monto_garantia = simpledialog.askfloat("Garantía", "💰 Monto de garantía:")
    monto_total = simpledialog.askfloat("Total", "💵 Monto total del evento:")
    dia = simpledialog.askstring("Fecha", "📅 Fecha (YYYY-MM-DD):")
    hora_fin = simpledialog.askstring("Hora fin", "⏰ Hora de finalización (HH:MM):")
    decoracion = messagebox.askyesno("Decoración", "🎀 ¿Requiere decoración?")

    agregar_evento(tipo, nombre, carnet, direccion, monto_garantia, monto_total, dia, hora_fin, decoracion)
    messagebox.showinfo("✅ Éxito", "Evento agregado correctamente")
    listar_eventos_gui()

def listar_eventos_gui():
    for i in tree.get_children():
        tree.delete(i)
    for e in listar_eventos():
        tree.insert("", "end", values=(
            e.id, e.tipo, e.nombre, e.carnet, e.direccion_domicilio,
            e.monto_garantia, e.monto_total, e.dia, e.hora_fin,
            "Sí" if e.decoracion else "No"
        ))

def eliminar_evento_gui():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("⚠️", "Selecciona un evento")
        return
    evento_id = tree.item(selected)["values"][0]
    if messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar el evento?"):
        eliminar_evento(evento_id)
        listar_eventos_gui()

def modificar_evento_gui():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("⚠️", "Selecciona un evento")
        return
    evento = tree.item(selected)["values"]
    evento_id = evento[0]

    tipo = simpledialog.askstring("Tipo de evento", "🎂 Tipo de evento:", initialvalue=evento[1]) or evento[1]
    nombre = simpledialog.askstring("Nombre", "👤 Nombre del cliente:", initialvalue=evento[2]) or evento[2]
    carnet = simpledialog.askstring("Carnet", "🪪 Carnet de identidad:", initialvalue=evento[3]) or evento[3]
    direccion = simpledialog.askstring("Dirección", "🏠 Dirección de domicilio:", initialvalue=evento[4]) or evento[4]
    monto_garantia = simpledialog.askfloat("Garantía", "💰 Monto de garantía:", initialvalue=evento[5]) or evento[5]
    monto_total = simpledialog.askfloat("Total", "💵 Monto total del evento:", initialvalue=evento[6]) or evento[6]
    dia = simpledialog.askstring("Fecha", "📅 Fecha (YYYY-MM-DD):", initialvalue=str(evento[7])) or evento[7]
    hora_fin = simpledialog.askstring("Hora fin", "⏰ Hora de finalización (HH:MM):", initialvalue=str(evento[8])) or evento[8]
    decoracion = messagebox.askyesno("Decoración", "🎀 ¿Requiere decoración?")

    modificar_evento(evento_id,
                     tipo=tipo, nombre=nombre, carnet=carnet, direccion_domicilio=direccion,
                     monto_garantia=monto_garantia, monto_total=monto_total,
                     dia=datetime.strptime(dia, "%Y-%m-%d").date(),
                     hora_fin=datetime.strptime(hora_fin, "%H:%M").time(),
                     decoracion=decoracion)
    listar_eventos_gui()
    messagebox.showinfo("✅ Éxito", "Evento modificado correctamente")

# ---------------- VENTANA ---------------- #
root = tk.Tk()
root.title("🎉 Gestión de Eventos 🎉")
root.geometry("1100x400")

# Botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="➕ Agregar evento", command=agregar_evento_gui).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="✏️ Modificar evento", command=modificar_evento_gui).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="🗑️ Eliminar evento", command=eliminar_evento_gui).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="📋 Listar eventos", command=listar_eventos_gui).grid(row=0, column=3, padx=5)

# Tabla de eventos
columns = ("ID", "Tipo", "Nombre", "Carnet", "Dirección", "Garantía", "Total", "Fecha", "Hora fin", "Decoración")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill="both", expand=True)

listar_eventos_gui()
root.mainloop()
