import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# --- CONFIGURACIÓN ---
DB_PATH = r"C:\Users\Jokaira\Documents\GITHUB\PMSHotel\base_datos.db"

# ==========================
# FUNCIONES DE UTILIDAD
# ==========================

def validar_fecha(fecha_str):
    """Convierte y valida una cadena de fecha a objeto date, formato YYYY-MM-DD."""
    try:
        return datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# ==========================
# FUNCIONES BASE DE DATOS
# ==========================
def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def obtener_tipos_habitacion():
    """Obtiene todos los nombres de tipos de habitación para el Combobox."""
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM tipos_habitacion")
    tipos = [row[0] for row in cur.fetchall()]
    conn.close()
    return tipos

# --- CHECK-IN / CHECK-OUT ---
def buscar_reserva(query):
    conn = conectar_db()
    cur = conn.cursor()
    # Usamos LIKE para búsqueda parcial por nombre o número de habitación
    cur.execute("SELECT * FROM reservas WHERE id=? OR cliente_nombre LIKE ? OR numero_hab LIKE ?",
                (query, f"%{query}%", f"%{query}%"))
    result = cur.fetchall()
    conn.close()
    return result

def buscar_habitaciones_disponibles(fecha_entrada, fecha_salida, tipo):
    """
    Busca habitaciones disponibles que:
    1. Estén en estado 'Disponible'.
    2. Coincidan con el 'tipo' solicitado.
    3. NO estén reservadas para un periodo que se solape con la estancia solicitada.
    """
    conn = conectar_db()
    cur = conn.cursor()
    
    # Lógica de solapamiento mejorada:
    # Una reserva se solapa si (reserva_salida > nueva_entrada) Y (reserva_entrada < nueva_salida)
    cur.execute("""
        SELECT h.numero, t.nombre as tipo_nombre, t.precio_base
        FROM habitaciones h
        JOIN tipos_habitacion t ON h.tipo_id=t.id
        WHERE h.estado='Disponible' AND t.nombre=?
        AND h.numero NOT IN (
            SELECT numero_hab FROM reservas
            WHERE (fecha_salida > ?) AND (fecha_entrada < ?)
        )
    """, (tipo, fecha_entrada, fecha_salida))
    
    result = cur.fetchall()
    conn.close()
    return result

def registrar_checkin(reserva_id):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE reservas SET checked_in=1, estado='checked-in' WHERE id=?", (reserva_id,))
        cur.execute("UPDATE habitaciones SET estado='Ocupada' WHERE numero=(SELECT numero_hab FROM reservas WHERE id=?)", (reserva_id,))
        cur.execute("INSERT INTO checkins_checkouts(reserva_id, tipo, fecha_hora) VALUES (?, 'checkin', ?)",
                    (reserva_id, datetime.now()))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e # Re-lanza el error para que la GUI pueda mostrarlo
    finally:
        conn.close()

def registrar_walkin(nombre, email, fecha_entrada, fecha_salida, personas, monto_pago, numero_hab):
    """Registra un walk-in (check-in sin reserva previa) como una transacción atómica."""
    conn = conectar_db()
    cur = conn.cursor()

    try:
        # 1️ Registrar ingreso
        cur.execute(
            "INSERT INTO ingresos(tipo_ingreso, concepto, monto, metodo_pago) VALUES (?, ?, ?, ?)",
            ("walk_in", f"Walk-in {nombre}", monto_pago, "efectivo")
        )
        id_pago = cur.lastrowid

        # 2 Registrar walk-in (esto asume que tienes una tabla walk_ins, o podrías usar la tabla 'reservas' con un campo 'es_walkin')
        # Si no tienes la tabla 'walk_ins', lo trataremos como una reserva
        cur.execute("""
            INSERT INTO reservas (
                numero_hab, cliente_nombre, cliente_email, fecha_entrada, fecha_salida, 
                total_personas, monto_pago, estado, checked_in, checked_out
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'checked-in', 1, 0)
        """, (numero_hab, nombre, email, fecha_entrada, fecha_salida, personas, monto_pago))
        
        # 3️ Marcar habitación como ocupada
        cur.execute("UPDATE habitaciones SET estado='Ocupada' WHERE numero=?", (numero_hab,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def registrar_checkout(reserva_id):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE reservas SET estado='checked-out', checked_out=1 WHERE id=?", (reserva_id,))
        cur.execute("UPDATE habitaciones SET estado='Disponible' WHERE numero=(SELECT numero_hab FROM reservas WHERE id=?)", (reserva_id,))
        cur.execute("INSERT INTO checkins_checkouts(reserva_id, tipo, fecha_hora) VALUES (?, 'checkout', ?)",
                    (reserva_id, datetime.now()))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def agregar_cargo_checkout(reserva_id, concepto, descripcion, monto):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        # 1. Registrar el cargo como ingreso adicional
        cur.execute("INSERT INTO ingresos(tipo_ingreso, concepto, monto, metodo_pago) VALUES (?, ?, ?, ?)",
                    ("costo_adicional_checkout", f"{concepto}: {descripcion}", monto, "efectivo"))
        # 2. Actualizar el monto total de la reserva (esto asume que el cargo se paga al checkout)
        cur.execute("UPDATE reservas SET monto_pago = monto_pago + ? WHERE id=?", (monto, reserva_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def extender_estadia(reserva_id, nueva_salida):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE reservas SET fecha_salida=? WHERE id=?", (nueva_salida, reserva_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def obtener_dashboard():
    conn = conectar_db()
    cur = conn.cursor()
    hoy = date.today().isoformat()
    # Check-ins pendientes para hoy
    cur.execute("SELECT COUNT(*) FROM reservas WHERE fecha_entrada=? AND estado='Pendiente'", (hoy,))
    checkins = cur.fetchone()[0]
    # Check-outs pendientes para hoy (reservas en estado checked-in cuya fecha de salida es hoy)
    cur.execute("SELECT COUNT(*) FROM reservas WHERE fecha_salida=? AND estado='checked-in'", (hoy,))
    checkouts = cur.fetchone()[0]
    # Habitaciones ocupadas (incluye check-ins de hoy que ya se completaron)
    cur.execute("SELECT COUNT(*) FROM habitaciones WHERE estado='Ocupada'")
    ocupadas = cur.fetchone()[0]
    # Ingresos del día
    cur.execute("SELECT SUM(monto) FROM ingresos WHERE date(fecha_pago)=?", (hoy,))
    ingresos = cur.fetchone()[0] or 0
    conn.close()
    return checkins, checkouts, ocupadas, ingresos

# ==========================
# INTERFAZ GRÁFICA
# ==========================
class FrontDeskApp:
    def __init__(self, master):
        self.master = master
        # master.title("Front Desk - PMS Hotel")
        # master.geometry("1300x750")

        # Dashboard
        self.dashboard_frame = tk.Frame(master)
        self.dashboard_frame.pack(pady=10, fill="x")
        self.kpi_checkins = tk.Label(self.dashboard_frame, text="Check-ins Hoy: 0", font=("Arial",14))
        self.kpi_checkins.pack(side="left", padx=10)
        self.kpi_checkouts = tk.Label(self.dashboard_frame, text="Check-outs Hoy: 0", font=("Arial",14))
        self.kpi_checkouts.pack(side="left", padx=10)
        self.kpi_ocupadas = tk.Label(self.dashboard_frame, text="Habitaciones Ocupadas: 0", font=("Arial",14))
        self.kpi_ocupadas.pack(side="left", padx=10)
        self.kpi_ingresos = tk.Label(self.dashboard_frame, text="Ingresos Hoy: $0", font=("Arial",14))
        self.kpi_ingresos.pack(side="left", padx=10)

        # Tabs
        self.tab_control = ttk.Notebook(master)
        self.tab_checkin = ttk.Frame(self.tab_control)
        self.tab_walkin = ttk.Frame(self.tab_control)
        self.tab_checkout = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_checkin, text="Check-in")
        self.tab_control.add(self.tab_walkin, text="Walk-in")
        self.tab_control.add(self.tab_checkout, text="Check-out")
        self.tab_control.pack(expand=1, fill='both')

        self.crear_checkin()
        self.crear_walkin()
        self.crear_checkout()
        self.actualizar_dashboard()

    # ------------------
    # DASHBOARD
    # ------------------
    def actualizar_dashboard(self):
        checkins, checkouts, ocupadas, ingresos = obtener_dashboard()
        self.kpi_checkins.config(text=f"Check-ins Hoy: {checkins}")
        self.kpi_checkouts.config(text=f"Check-outs Hoy: {checkouts}")
        self.kpi_ocupadas.config(text=f"Habitaciones Ocupadas: {ocupadas}")
        self.kpi_ingresos.config(text=f"Ingresos Hoy: ${ingresos:,.2f}") # Formato de moneda

    # ------------------
    # CHECK-IN
    # ------------------
    def crear_checkin(self):
        frame = tk.Frame(self.tab_checkin)
        frame.pack(pady=10, fill="x")
        tk.Label(frame, text="Buscar Reserva (ID, Nombre o Habitación):").pack(anchor="w")
        self.ci_query = tk.Entry(frame)
        self.ci_query.pack(fill="x")
        tk.Button(frame, text="Buscar", command=self.buscar_reserva_gui).pack(pady=5)

        self.ci_resultados = ttk.Treeview(frame, columns=("ID","Cliente","Habitación","Entrada","Salida","Total","Estado"), show="headings")
        for col in self.ci_resultados["columns"]:
            self.ci_resultados.heading(col, text=col)
        self.ci_resultados.pack(pady=10, fill="x")

        tk.Button(frame, text="Confirmar Check-in", command=self.confirmar_checkin_gui, bg="#4CAF50", fg="white").pack(pady=5)

    def buscar_reserva_gui(self):
        query = self.ci_query.get()
        resultados = buscar_reserva(query)
        for i in self.ci_resultados.get_children():
            self.ci_resultados.delete(i)
        for row in resultados:
            monto_formateado = f"${row['monto_pago']:,.2f}" if row['monto_pago'] is not None else "$0.00"
            self.ci_resultados.insert("", "end", values=(row["id"], row["cliente_nombre"], row["numero_hab"],
                                                         row["fecha_entrada"], row["fecha_salida"],
                                                         monto_formateado, row["estado"]))

    def confirmar_checkin_gui(self):
        selected = self.ci_resultados.selection()
        if not selected:
            messagebox.showwarning("Aviso","Seleccione una reserva")
            return
        
        estado = self.ci_resultados.item(selected[0])["values"][6]
        if estado != "Pendiente":
             messagebox.showwarning("Aviso",f"La reserva ya está en estado: {estado}")
             return

        reserva_id = self.ci_resultados.item(selected[0])["values"][0]
        try:
            registrar_checkin(reserva_id)
            messagebox.showinfo("Éxito","Check-in registrado con éxito.")
            self.buscar_reserva_gui() # Actualiza la lista
            self.actualizar_dashboard()
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el Check-in. Error: {e}")

    # ------------------
    # WALK-IN
    # ------------------
    def crear_walkin(self):
        frame = tk.Frame(self.tab_walkin)
        frame.pack(pady=10, fill="both", expand=True)

        # Configuración de grilla para Walk-in
        frame.columnconfigure(1, weight=1) # Permite que los campos de entrada se expandan

        # --- Datos del cliente ---
        tk.Label(frame, text="Nombre:").grid(row=0,column=0, padx=5, pady=5, sticky="e")
        self.w_name = tk.Entry(frame)
        self.w_name.grid(row=0,column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Email:").grid(row=1,column=0, padx=5, pady=5, sticky="e")
        self.w_email = tk.Entry(frame)
        self.w_email.grid(row=1,column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="Fecha Entrada (YYYY-MM-DD):").grid(row=2,column=0, padx=5, pady=5, sticky="e")
        self.w_fecha_entrada = tk.Entry(frame)
        self.w_fecha_entrada.grid(row=2,column=1, padx=5, pady=5, sticky="ew")
        self.w_fecha_entrada.insert(0, date.today().isoformat()) # Fecha por defecto

        tk.Label(frame, text="Fecha Salida (YYYY-MM-DD):").grid(row=3,column=0, padx=5, pady=5, sticky="e")
        self.w_fecha_salida = tk.Entry(frame)
        self.w_fecha_salida.grid(row=3,column=1, padx=5, pady=5, sticky="ew")
        
        # --- Combobox para Tipo de Habitación ---
        tk.Label(frame, text="Tipo Habitación:").grid(row=4,column=0, padx=5, pady=5, sticky="e")
        tipos = obtener_tipos_habitacion()
        self.w_tipo = ttk.Combobox(frame, values=tipos, state="readonly")
        self.w_tipo.grid(row=4,column=1, padx=5, pady=5, sticky="ew")

        tk.Label(frame, text="No. Personas:").grid(row=5,column=0, padx=5, pady=5, sticky="e")
        self.w_personas = tk.Entry(frame)
        self.w_personas.grid(row=5,column=1, padx=5, pady=5, sticky="ew")

        # --- Botón para buscar habitaciones disponibles ---
        tk.Button(frame, text="Buscar Habitaciones Disponibles", command=self.buscar_habitaciones_gui).grid(row=6,column=0,columnspan=2,pady=10)

        # --- Treeview para mostrar habitaciones disponibles ---
        self.w_habitaciones = ttk.Treeview(frame, columns=("Número","Tipo","Precio","Base"), show="headings")
        self.w_habitaciones.column("Base", width=0, stretch=tk.NO) # Columna oculta para el precio base
        self.w_habitaciones.heading("Número", text="Número")
        self.w_habitaciones.heading("Tipo", text="Tipo")
        self.w_habitaciones.heading("Precio", text="Precio por Noche")
        self.w_habitaciones.grid(row=7,column=0,columnspan=2,pady=10, sticky="nsew")

        # Campo para mostrar el monto calculado
        self.w_monto_label = tk.Label(frame, text="Monto Total Estimado: $0.00", font=("Arial", 12, "bold"), fg="blue")
        self.w_monto_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # --- Botón Confirmar Walk-in ---
        tk.Button(frame, text="Confirmar Walk-in", command=self.confirmar_walkin_gui, bg="#4CAF50", fg="white").grid(row=9,column=0,columnspan=2,pady=10)


    # ------------------
    # FUNCIONES WALK-IN
    # ------------------
    def buscar_habitaciones_gui(self):
        f_entrada_str = self.w_fecha_entrada.get()
        f_salida_str = self.w_fecha_salida.get()
        tipo = self.w_tipo.get()
        
        # 1. Validación de fechas
        f_entrada = validar_fecha(f_entrada_str)
        f_salida = validar_fecha(f_salida_str)

        if not f_entrada or not f_salida:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
            return
        
        if f_entrada >= f_salida:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada.")
            return

        if not tipo:
            messagebox.showwarning("Aviso", "Seleccione un tipo de habitación")
            return

        # Limpiar y buscar
        for i in self.w_habitaciones.get_children():
            self.w_habitaciones.delete(i)
        self.w_monto_label.config(text="Monto Total Estimado: $0.00")

        habitaciones = buscar_habitaciones_disponibles(f_entrada_str, f_salida_str, tipo)
        
        if not habitaciones:
             messagebox.showinfo("Aviso", "No se encontraron habitaciones disponibles para ese período/tipo.")

        for h in habitaciones:
            # Insertamos el precio base en la columna oculta 'Base' (índice 3)
            self.w_habitaciones.insert("", "end", values=(h["numero"], h["tipo_nombre"], f"${h['precio_base']:,.2f}", h["precio_base"]))
            
        # Bind para calcular el precio al seleccionar
        self.w_habitaciones.bind('<<TreeviewSelect>>', self.calcular_monto_walkin)

    def calcular_monto_walkin(self, event=None):
        selected = self.w_habitaciones.selection()
        if not selected:
            self.w_monto_label.config(text="Monto Total Estimado: $0.00")
            return

        f_entrada = validar_fecha(self.w_fecha_entrada.get())
        f_salida = validar_fecha(self.w_fecha_salida.get())

        if not f_entrada or not f_salida or f_entrada >= f_salida:
            self.w_monto_label.config(text="Monto Total Estimado: $0.00 (Revise las fechas)", fg="red")
            return
        
        dias_estancia = (f_salida - f_entrada).days
        
        # Obtenemos el precio base de la columna oculta (índice 3)
        try:
            precio_base = self.w_habitaciones.item(selected[0])["values"][3]
            monto_total = precio_base * dias_estancia
            self.w_monto_label.config(text=f"Monto Total Estimado ({dias_estancia} noches): ${monto_total:,.2f}", fg="blue")
        except:
             self.w_monto_label.config(text="Error al calcular monto", fg="red")


    def confirmar_walkin_gui(self):
        selected = self.w_habitaciones.selection()
        
        # 1. Validaciones
        nombre = self.w_name.get()
        f_entrada_str = self.w_fecha_entrada.get()
        f_salida_str = self.w_fecha_salida.get()
        email = self.w_email.get()
        personas_str = self.w_personas.get()
        
        if not all([nombre, f_entrada_str, f_salida_str, personas_str, selected]):
            messagebox.showwarning("Aviso", "Complete todos los datos y seleccione una habitación.")
            return

        f_entrada = validar_fecha(f_entrada_str)
        f_salida = validar_fecha(f_salida_str)

        if not f_entrada or not f_salida or f_entrada >= f_salida:
            messagebox.showerror("Error de Fecha", "Fechas inválidas. Revise el formato y la lógica.")
            return
            
        try:
            personas = int(personas_str)
        except ValueError:
            messagebox.showerror("Error","Número de personas inválido.")
            return

        # 2. Obtener datos de la habitación
        values = self.w_habitaciones.item(selected[0])["values"]
        numero_hab = values[0]
        precio_base = values[3] 
        dias_estancia = (f_salida - f_entrada).days
        monto_pago = precio_base * dias_estancia
        
        # 3. Confirmación final
        if not messagebox.askyesno("Confirmar Cobro y Registro", 
                               f"Cliente: {nombre}\nHabitación: {numero_hab}\nTotal ({dias_estancia} noches): ${monto_pago:,.2f}\n\n¿Desea CONFIRMAR el Walk-in y marcar la habitación como ocupada?"):
            return

        # 4. Registro
        try:
            registrar_walkin(nombre, email, f_entrada_str, f_salida_str, personas, monto_pago, numero_hab)
            messagebox.showinfo("Éxito","Walk-in registrado con éxito.")
            self.actualizar_dashboard()
            # Limpiar campos después de un registro exitoso (UX)
            self.w_name.delete(0, tk.END)
            self.w_email.delete(0, tk.END)
            self.w_personas.delete(0, tk.END)
            for i in self.w_habitaciones.get_children():
                self.w_habitaciones.delete(i)
            self.w_monto_label.config(text="Monto Total Estimado: $0.00", fg="blue")
            self.w_tipo.set('')

        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo registrar el Walk-in. Error: {e}")


    # ------------------
    # CHECK-OUT
    # ------------------
    def crear_checkout(self):
        frame = tk.Frame(self.tab_checkout)
        frame.pack(pady=10, fill="x")

        tk.Label(frame, text="Check-out de reservas").pack()
        self.co_resultados = ttk.Treeview(frame, columns=("ID","Cliente","Habitación","Entrada","Salida","Total","Estado"), show="headings")
        for col in self.co_resultados["columns"]:
            self.co_resultados.heading(col, text=col)
        self.co_resultados.pack(pady=10, fill="x")

        tk.Button(frame, text="Cargar Check-outs de Hoy", command=self.cargar_checkouts).pack(pady=5)

        # Contenedor de Opciones Adicionales
        opciones_frame = tk.Frame(frame)
        opciones_frame.pack(pady=10, fill="x")
        
        # --- Cargos adicionales ---
        cargo_frame = tk.LabelFrame(opciones_frame, text="Cargos Adicionales", padx=10, pady=10)
        cargo_frame.pack(side="left", padx=10, fill="x", expand=True)
        cargo_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(cargo_frame, text="Concepto:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.co_concepto = ttk.Combobox(cargo_frame, values=["Minibar","Room Service","Lavandería","Estacionamiento","WiFi Premium","Otro"])
        self.co_concepto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(cargo_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.co_descr = tk.Entry(cargo_frame)
        self.co_descr.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(cargo_frame, text="Monto:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.co_monto = tk.Entry(cargo_frame)
        self.co_monto.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Button(cargo_frame, text="Agregar Cargo", command=self.agregar_cargo, bg="#FFC107").grid(row=3, column=0, columnspan=2, pady=5)
        
        # Treeview para mostrar cargos provisionales
        self.co_cargos_tree = ttk.Treeview(cargo_frame, columns=("Concepto","Monto"), show="headings", height=5)
        self.co_cargos_tree.heading("Concepto", text="Concepto")
        self.co_cargos_tree.heading("Monto", text="Monto")
        self.co_cargos_tree.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # --- Extensión de estadía ---
        ext_frame = tk.LabelFrame(opciones_frame, text="Extensión de Estadía", padx=10, pady=10)
        ext_frame.pack(side="right", padx=10, fill="x")
        ext_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(ext_frame, text="Nueva fecha de salida (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.co_nueva_salida = tk.Entry(ext_frame)
        self.co_nueva_salida.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Button(ext_frame, text="Extender Estadía", command=self.extender_estadia_gui, bg="#007BFF", fg="white").grid(row=1,column=0,columnspan=2,pady=5)

        tk.Button(frame, text="Confirmar Check-out", command=self.confirmar_checkout_gui, bg="#4CAF50", fg="white").pack(pady=10)

    def cargar_checkouts(self):
        conn = conectar_db()
        hoy = date.today().isoformat()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reservas WHERE estado='checked-in' AND fecha_salida <= ?", (hoy,)) # También incluye atrasados
        resultados = cur.fetchall()
        conn.close()
        for i in self.co_resultados.get_children():
            self.co_resultados.delete(i)
            
        # Limpiar cargos provisionales
        for i in self.co_cargos_tree.get_children():
            self.co_cargos_tree.delete(i)

        for row in resultados:
            monto_formateado = f"${row['monto_pago']:,.2f}" if row['monto_pago'] is not None else "$0.00"
            self.co_resultados.insert("", "end", values=(row["id"], row["cliente_nombre"], row["numero_hab"],
                                                         row["fecha_entrada"], row["fecha_salida"],
                                                         monto_formateado, row["estado"]))

    def agregar_cargo(self):
        selected = self.co_resultados.selection()
        if not selected:
            messagebox.showwarning("Aviso","Seleccione una reserva en Check-in.")
            return
        
        reserva_id = self.co_resultados.item(selected[0])["values"][0]
        concepto = self.co_concepto.get()
        descripcion = self.co_descr.get()
        
        if not concepto or not descripcion:
            messagebox.showwarning("Aviso","Seleccione un concepto y escriba una descripción.")
            return

        try:
            monto = float(self.co_monto.get())
            if monto <= 0:
                 raise ValueError
        except ValueError:
            messagebox.showerror("Error","Monto inválido. Debe ser un número positivo.")
            return
            
        try:
            agregar_cargo_checkout(reserva_id, concepto, descripcion, monto)
            messagebox.showinfo("Éxito","Cargo agregado al total de la reserva.")
            self.cargar_checkouts() # Para refrescar el monto total en el Treeview
            self.actualizar_dashboard()
            self.co_cargos_tree.insert("", "end", values=(f"{concepto}: {descripcion}", f"${monto:,.2f}"))
            self.co_monto.delete(0, tk.END)
            self.co_descr.delete(0, tk.END)
            self.co_concepto.set('')
        except Exception as e:
             messagebox.showerror("Error de DB", f"No se pudo agregar el cargo. Error: {e}")

     # En la función extender_estadia_gui

    def extender_estadia_gui(self):
        selected = self.co_resultados.selection()
        if not selected:
            messagebox.showwarning("Aviso","Seleccione una reserva.")
            return
    
        reserva_id = self.co_resultados.item(selected[0])["values"][0]
        nueva_salida_str = self.co_nueva_salida.get()
        fecha_actual_salida_str = self.co_resultados.item(selected[0])["values"][4]
    
    # 1. Validación de fechas (Usando la función de utilidad)
        nueva_salida = validar_fecha(nueva_salida_str)
        fecha_actual_salida = validar_fecha(fecha_actual_salida_str)

        if not nueva_salida:
            messagebox.showerror("Error de Fecha", "Formato de fecha de salida inválido (YYYY-MM-DD).")
            return
    
        if not fecha_actual_salida:
        # Esto solo debería ocurrir si el dato en la DB es erróneo
            messagebox.showerror("Error de Datos", "No se pudo leer la fecha de salida actual.")
            return
        
    # 2. Lógica de extensión: debe ser estrictamente posterior
    # Si la nueva fecha es menor o igual, mostramos el error de extensión.
        if nueva_salida <= fecha_actual_salida:
            messagebox.showerror("Error de Extensión", "La nueva fecha de salida debe ser estrictamente posterior a la fecha actual.")
            return

    # Si todo es correcto, se procede a la extensión
        try:
            extender_estadia(reserva_id, nueva_salida_str)
            messagebox.showinfo("Éxito","Estadía extendida con éxito.")
            self.cargar_checkouts()
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo extender la estadía. Error: {e}")

    def confirmar_checkout_gui(self):
        selected = self.co_resultados.selection()
        if not selected:
            messagebox.showwarning("Aviso","Seleccione una reserva.")
            return
        
        reserva_id = self.co_resultados.item(selected[0])["values"][0]
        
        # Confirmación de salida (UX)
        if not messagebox.askyesno("Confirmar Check-out", 
                               f"¿Confirma la salida de la reserva ID {reserva_id}?\nSe marcará la habitación como DISPONIBLE."):
            return
            
        try:
            registrar_checkout(reserva_id)
            messagebox.showinfo("Éxito","Check-out confirmado. Habitación liberada.")
            self.cargar_checkouts()
            self.actualizar_dashboard()
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo completar el Check-out. Error: {e}")


# ==========================
# EJECUTAR APP
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = FrontDeskApp(root)
    root.mainloop()