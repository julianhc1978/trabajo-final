import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate
import mysql.connector
from mysql.connector import Error


def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TallerMecanico"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
        return None


def registrar_vehiculo():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc('RegistrarNuevoVehiculo', (
                entry_cliente_nombre.get(),
                entry_cliente_telefono.get(),
                entry_vehiculo_modelo.get(),
                entry_vehiculo_placa.get(),
                entry_servicio_tipo.get(),
                entry_fecha_ingreso.get(),
                entry_fecha_entrega.get(),
                entry_notas.get("1.0", "end-1c")
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            agregar_operacion_a_tabla("Registrar Vehículo", entry_vehiculo_placa.get(), "Pendiente")
        except Error as e:
            messagebox.showerror("Error", f"Hubo un error al registrar el vehículo: {e}")
        finally:
            conn.close()


def programar_servicio():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc('ProgramarServicio', (
                entry_vehiculo_placa.get(),
                entry_servicio_tipo.get(),
                entry_fecha_ingreso.get(),
                entry_fecha_entrega.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio programado correctamente.")
            agregar_operacion_a_tabla("Programar Servicio", entry_vehiculo_placa.get(), "Pendiente")
        except Error as e:
            messagebox.showerror("Error", f"Hubo un error al programar el servicio: {e}")
        finally:
            conn.close()


def controlar_reparaciones():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc('ControlReparaciones', (
                entry_vehiculo_placa.get(),
                combo_estado_servicio.get(),
                entry_inventario_repuesto.get(),
                entry_cantidad_repuesto.get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Reparación controlada correctamente.")
            agregar_operacion_a_tabla("Controlar Reparación", entry_vehiculo_placa.get(), combo_estado_servicio.get())
        except Error as e:
            messagebox.showerror("Error", f"Hubo un error al controlar las reparaciones: {e}")
        finally:
            conn.close()


def gestionar_garantia():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc('GestionGarantias', (
                entry_vehiculo_placa.get(),
                entry_notas.get("1.0", "end-1c")
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Garantía gestionada correctamente.")
            agregar_operacion_a_tabla("Gestionar Garantía", entry_vehiculo_placa.get(), "Garantizado")
        except Error as e:
            messagebox.showerror("Error", f"Hubo un error al gestionar la garantía: {e}")
        finally:
            conn.close()


def agregar_operacion_a_tabla(operacion, placa, estado):
    nueva_fila = [operacion, placa, estado]
    operaciones.append(nueva_fila)
    text_operaciones.delete(1.0, "end")
    tabla = tabulate(operaciones, headers=["Operación", "Placa Vehículo", "Estado"], tablefmt="grid")
    text_operaciones.insert(tk.END, tabla)


def cerrar_ventana():
    if conn.is_connected():
        conn.close()
        print("Conexión a la base de datos cerrada.")
    root.destroy()


root = tk.Tk()
root.title("Gestión Taller Mecánico")
root.geometry("800x600")


conn = conectar_db()


root.protocol("WM_DELETE_WINDOW", cerrar_ventana)


operaciones = []


tk.Label(root, text="Nombre del Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_cliente_nombre = tk.Entry(root)
entry_cliente_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Teléfono del Cliente:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_cliente_telefono = tk.Entry(root)
entry_cliente_telefono.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Modelo del Vehículo:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_vehiculo_modelo = tk.Entry(root)
entry_vehiculo_modelo.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Placa del Vehículo:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_vehiculo_placa = tk.Entry(root)
entry_vehiculo_placa.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Tipo de Servicio:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
entry_servicio_tipo = tk.Entry(root)
entry_servicio_tipo.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha de Ingreso (YYYY-MM-DD):").grid(row=5, column=0, padx=10, pady=5, sticky='e')
entry_fecha_ingreso = tk.Entry(root)
entry_fecha_ingreso.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha de Entrega (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky='e')
entry_fecha_entrega = tk.Entry(root)
entry_fecha_entrega.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Inventario de Repuesto:").grid(row=7, column=0, padx=10, pady=5, sticky='e')
entry_inventario_repuesto = tk.Entry(root)
entry_inventario_repuesto.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Cantidad de Repuesto:").grid(row=8, column=0, padx=10, pady=5, sticky='e')
entry_cantidad_repuesto = tk.Entry(root)
entry_cantidad_repuesto.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Estado del Servicio:").grid(row=9, column=0, padx=10, pady=5, sticky='e')
combo_estado_servicio = tk.StringVar()
combo_estado_servicio.set("Pendiente")
estado_options = ["Pendiente", "En Proceso", "Completado"]
tk.OptionMenu(root, combo_estado_servicio, *estado_options).grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Notas adicionales:").grid(row=10, column=0, padx=10, pady=5, sticky='e')
entry_notas = tk.Text(root, height=4, width=40)
entry_notas.grid(row=10, column=1, padx=10, pady=5)


frame_botones = tk.Frame(root)
frame_botones.grid(row=11, column=0, columnspan=2, pady=10)

tk.Button(frame_botones, text="Registrar Vehículo", command=registrar_vehiculo).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Programar Servicio", command=programar_servicio).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Controlar Reparaciones", command=controlar_reparaciones).grid(row=0, column=2, padx=10)
tk.Button(frame_botones, text="Gestionar Garantía", command=gestionar_garantia).grid(row=0, column=3, padx=10)


text_operaciones = tk.Text(root, height=10, width=80)
text_operaciones.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
