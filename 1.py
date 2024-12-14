import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate
import mysql.connector
from mysql.connector import Error

class TallerMecanicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Taller Mecánico")
        self.root.geometry("800x600")

        # Variables
        self.operaciones = []
        self.conn = self.conectar_db()

        # Interfaz gráfica
        self.crear_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def conectar_db(self):
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

    def crear_widgets(self):
        # Entradas y etiquetas
        self.entry_cliente_nombre = self.crear_entrada_con_etiqueta("Nombre del Cliente:", 0)
        self.entry_cliente_telefono = self.crear_entrada_con_etiqueta("Teléfono del Cliente:", 1)
        self.entry_vehiculo_modelo = self.crear_entrada_con_etiqueta("Modelo del Vehículo:", 2)
        self.entry_vehiculo_placa = self.crear_entrada_con_etiqueta("Placa del Vehículo:", 3)
        self.entry_servicio_tipo = self.crear_entrada_con_etiqueta("Tipo de Servicio:", 4)
        self.entry_fecha_ingreso = self.crear_entrada_con_etiqueta("Fecha de Ingreso (YYYY-MM-DD):", 5)
        self.entry_fecha_entrega = self.crear_entrada_con_etiqueta("Fecha de Entrega (YYYY-MM-DD):", 6)
        self.entry_inventario_repuesto = self.crear_entrada_con_etiqueta("Inventario de Repuesto:", 7)
        self.entry_cantidad_repuesto = self.crear_entrada_con_etiqueta("Cantidad de Repuesto:", 8)

        # ComboBox para estado del servicio
        tk.Label(self.root, text="Estado del Servicio:").grid(row=9, column=0, padx=10, pady=5, sticky='e')
        self.combo_estado_servicio = tk.StringVar()
        self.combo_estado_servicio.set("Pendiente")
        estado_options = ["Pendiente", "En Proceso", "Completado"]
        tk.OptionMenu(self.root, self.combo_estado_servicio, *estado_options).grid(row=9, column=1, padx=10, pady=5)

        # Notas
        tk.Label(self.root, text="Notas adicionales:").grid(row=10, column=0, padx=10, pady=5, sticky='e')
        self.entry_notas = tk.Text(self.root, height=4, width=40)
        self.entry_notas.grid(row=10, column=1, padx=10, pady=5)

        # Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.grid(row=11, column=0, columnspan=2, pady=10)

        tk.Button(frame_botones, text="Registrar Vehículo", command=self.registrar_vehiculo).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Programar Servicio", command=self.programar_servicio).grid(row=0, column=1, padx=10)
        tk.Button(frame_botones, text="Controlar Reparaciones", command=self.controlar_reparaciones).grid(row=0, column=2, padx=10)
        tk.Button(frame_botones, text="Gestionar Garantía", command=self.gestionar_garantia).grid(row=0, column=3, padx=10)

        # Área de operaciones
        self.text_operaciones = tk.Text(self.root, height=10, width=80)
        self.text_operaciones.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

    def crear_entrada_con_etiqueta(self, texto_etiqueta, fila):
        tk.Label(self.root, text=texto_etiqueta).grid(row=fila, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(self.root)
        entry.grid(row=fila, column=1, padx=10, pady=5)
        return entry

    def agregar_operacion_a_tabla(self, operacion, placa, estado):
        nueva_fila = [operacion, placa, estado]
        self.operaciones.append(nueva_fila)
        self.text_operaciones.delete(1.0, "end")
        tabla = tabulate(self.operaciones, headers=["Operación", "Placa Vehículo", "Estado"], tablefmt="grid")
        self.text_operaciones.insert(tk.END, tabla)

    def registrar_vehiculo(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.callproc('RegistrarNuevoVehiculo', (
                    self.entry_cliente_nombre.get(),
                    self.entry_cliente_telefono.get(),
                    self.entry_vehiculo_modelo.get(),
                    self.entry_vehiculo_placa.get(),
                    self.entry_servicio_tipo.get(),
                    self.entry_fecha_ingreso.get(),
                    self.entry_fecha_entrega.get(),
                    self.entry_notas.get("1.0", "end-1c")
                ))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
                self.agregar_operacion_a_tabla("Registrar Vehículo", self.entry_vehiculo_placa.get(), "Pendiente")
            except Error as e:
                messagebox.showerror("Error", f"Hubo un error al registrar el vehículo: {e}")

    def programar_servicio(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.callproc('ProgramarServicio', (
                    self.entry_vehiculo_placa.get(),
                    self.entry_servicio_tipo.get(),
                    self.entry_fecha_ingreso.get(),
                    self.entry_fecha_entrega.get()
                ))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Servicio programado correctamente.")
                self.agregar_operacion_a_tabla("Programar Servicio", self.entry_vehiculo_placa.get(), "Pendiente")
            except Error as e:
                messagebox.showerror("Error", f"Hubo un error al programar el servicio: {e}")

    def controlar_reparaciones(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.callproc('ControlReparaciones', (
                    self.entry_vehiculo_placa.get(),
                    self.combo_estado_servicio.get(),
                    self.entry_inventario_repuesto.get(),
                    self.entry_cantidad_repuesto.get()
                ))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Reparación controlada correctamente.")
                self.agregar_operacion_a_tabla("Controlar Reparación", self.entry_vehiculo_placa.get(), self.combo_estado_servicio.get())
            except Error as e:
                messagebox.showerror("Error", f"Hubo un error al controlar las reparaciones: {e}")

    def gestionar_garantia(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.callproc('GestionGarantias', (
                    self.entry_vehiculo_placa.get(),
                    self.entry_notas.get("1.0", "end-1c")
                ))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Garantía gestionada correctamente.")
                self.agregar_operacion_a_tabla("Gestionar Garantía", self.entry_vehiculo_placa.get(), "Garantizado")
            except Error as e:
                messagebox.showerror("Error", f"Hubo un error al gestionar la garantía: {e}")

    def cerrar_ventana(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Conexión a la base de datos cerrada.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TallerMecanicoApp(root)
    root.mainloop()

