from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import customtkinter as ctk
from settings import *
import basedatos
from tkinter import messagebox
from datetime import datetime

class CotizacionBuffet(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master=master, fg_color='transparent')
		self.pack(fill='both', expand=True)

		self.fecha_var = ctk.StringVar()
		self.personas_var = ctk.StringVar()
		self.menu_var = ctk.StringVar(value='Clásico')
		self.precio_var = ctk.StringVar()
		self.total_var = ctk.StringVar(value='$0.00')
		self.notas_textbox = None
		self.cotizacion_seleccionada = ctk.IntVar(value=0)

		self.crear_formulario()
		self.crear_total_y_botones()
		self.crear_tabla()
		self.cargar_cotizaciones()

	def crear_formulario(self):
		frame = ctk.CTkFrame(self, fg_color='transparent', border_color=PRIMARIO, border_width=2, corner_radius=12)
		frame.pack(fill='x', padx=16, pady=(16, 4))
		frame.grid_columnconfigure(1, weight=2)
		frame.grid_columnconfigure(3, weight=1)
		frame.grid_columnconfigure(5, weight=2)
		frame.grid_columnconfigure(7, weight=1)

		# Fecha
		ctk.CTkLabel(frame, text='Fecha', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=0, padx=(8,2), pady=8, sticky='e')
		self.date_entry = DateEntry(frame, date_pattern='dd/MM/yyyy', textvariable=self.fecha_var, width=80, background=AZUL, foreground='black', borderwidth=2, locale='es_ES')
		self.date_entry.grid(row=0, column=1, padx=(2,16), pady=8, sticky='we')

		#numero de personas
		ctk.CTkLabel(frame, text='Nº Personas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=2, padx=(8,2), pady=8, sticky='e')
		ctk.CTkEntry(frame, textvariable=self.personas_var, width=120).grid(row=0, column=3, padx=(2,16), pady=8, sticky='we')
		#menu a elegir
		ctk.CTkLabel(frame, text='Menú', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=0, padx=(8,2), pady=8, sticky='e')
		ctk.CTkOptionMenu(frame, variable=self.menu_var, values=['Clásico', 'Premium', 'Vegetariano', 'Infantil'], width=180).grid(row=1, column=1, padx=(2,16), pady=8, sticky='we')
		#precio por persona
		ctk.CTkLabel(frame, text='Precio/persona', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=2, padx=(8,2), pady=8, sticky='e')
		ctk.CTkEntry(frame, textvariable=self.precio_var, width=120).grid(row=1, column=3, padx=(2,16), pady=8, sticky='we')

		# Notas
		ctk.CTkLabel(frame, text='Notas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=0, padx=8, pady=8, sticky='nw')
		notas_frame = ctk.CTkFrame(frame, fg_color='transparent', border_color=GRIS_CLARO2, border_width=2, corner_radius=8)
		notas_frame.grid(row=2, column=1, columnspan=7, padx=8, pady=8, sticky='nsew')
		self.notas_textbox = ctk.CTkTextbox(notas_frame, height=60, width=900, fg_color=BLANCO)
		self.notas_textbox.pack(fill='both', expand=True, padx=4, pady=4)

		# Actualizar total automáticamente
		self.personas_var.trace('w', lambda *args: self.actualizar_total())
		self.precio_var.trace('w', lambda *args: self.actualizar_total())

	def crear_total_y_botones(self):
		# Total y botones fuera del formulario, como en la imagen
		total_frame = ctk.CTkFrame(self, fg_color='transparent')
		total_frame.pack(fill='x', padx=16, pady=(0, 8))

		ctk.CTkLabel(total_frame, text='Total', font=(FUENTE, 15, 'bold'), text_color=OSCURO).pack(side='left', padx=(8, 0))
		ctk.CTkLabel(total_frame, textvariable=self.total_var, font=(FUENTE, 28, 'bold'), text_color=VERDE1).pack(side='left', padx=(8, 32))

		# Guardar / Actualizar
		self.btn_guardar = ctk.CTkButton(total_frame, text='💾 Guardar', fg_color=VERDE1, command=self.guardar_cotizacion)
		self.btn_guardar.pack(side='left', padx=8)
		# Botón para cancelar edición: crear pero NO mostrar hasta que haya selección
		self.btn_cancelar = ctk.CTkButton(total_frame, text='✖ Cancelar edición', fg_color=ROJO, command=self.cancelar_edicion)
		btn_pdf = ctk.CTkButton(total_frame, text='🖨️ Generar PDF', fg_color=MORADO, command=self.generar_pdf)
		btn_pdf.pack(side='left', padx=8)

	def actualizar_total(self):
		try:
			personas = int(self.personas_var.get())
			precio = float(self.precio_var.get())
			total = personas * precio
			self.total_var.set(f'${total:,.2f}')
		except Exception:
			self.total_var.set('$0.00')

	def crear_tabla(self):
		# Contenedor principal para la tabla
		tabla_container = ctk.CTkFrame(self, fg_color='transparent')
		tabla_container.pack(fill='both', expand=True, padx=16, pady=8)
		
		# Contenedor con scroll vertical para navegar cotizaciones largas (scrollbar en lateral derecho)
		self.tabla_frame = ctk.CTkScrollableFrame(tabla_container, fg_color='transparent', scrollbar_button_color=AZUL, scrollbar_button_hover_color=AZUL2)
		self.tabla_frame.pack(fill='both', expand=True)
		self.tabla = None

	def cargar_cotizaciones(self):
		# Limpiar tabla previa
		for widget in self.tabla_frame.winfo_children():
			widget.destroy()

		encabezados = ['Sel.', 'ID', 'Fecha', 'Personas', 'Menú', 'Total', '']
		for col, texto in enumerate(encabezados):
			ctk.CTkLabel(self.tabla_frame, text=texto, font=(FUENTE, 13, 'bold'), fg_color=GRIS_CLARO3, width=70 if col==0 else 100, anchor='center').grid(row=0, column=col, padx=2, pady=2)

		cotizaciones = basedatos.obtener_cotizaciones_buffet() if hasattr(basedatos, 'obtener_cotizaciones_buffet') else []
		for i, cot in enumerate(cotizaciones, start=1):
			id_, fecha, personas, menu, precio, total, notas, _ = cot
			btn_sel = ctk.CTkButton(self.tabla_frame, text='Seleccionar', width=60, fg_color=AZUL, command=lambda id_=id_: self.seleccionar_cotizacion(id_))
			btn_sel.grid(row=i, column=0, padx=2)
			# Resaltar fila si está seleccionada
			bg = VERDE_CLARO if self.cotizacion_seleccionada.get() == id_ else 'transparent'
			ctk.CTkLabel(self.tabla_frame, text=str(id_), width=40, anchor='center', fg_color=bg).grid(row=i, column=1)
			ctk.CTkLabel(self.tabla_frame, text=fecha, width=100, anchor='center', fg_color=bg).grid(row=i, column=2)
			ctk.CTkLabel(self.tabla_frame, text=str(personas), width=60, anchor='center', fg_color=bg).grid(row=i, column=3)
			ctk.CTkLabel(self.tabla_frame, text=menu, width=100, anchor='center', fg_color=bg).grid(row=i, column=4)
			ctk.CTkLabel(self.tabla_frame, text=f'${total:,.2f}', width=80, anchor='center', fg_color=bg).grid(row=i, column=5)
			btn_eliminar = ctk.CTkButton(self.tabla_frame, text='Eliminar', fg_color=ROJO, width=70, command=lambda id_=id_: self.eliminar_cotizacion(id_))
			btn_eliminar.grid(row=i, column=6, padx=4)

	def seleccionar_cotizacion(self, id_):
		# Marcar selección y cargar datos de la cotización en el formulario para edición
		self.cotizacion_seleccionada.set(id_)
		# Buscar la cotización por ID
		cotizaciones = basedatos.obtener_cotizaciones_buffet() if hasattr(basedatos, 'obtener_cotizaciones_buffet') else []
		cot = None
		for c in cotizaciones:
			if c[0] == id_:
				cot = c
				break
		if not cot:
			messagebox.showerror('Error', 'No se encontró la cotización seleccionada.')
			return
		# Rellenar formulario con los valores existentes
		_, fecha, personas, menu, precio, total, notas, _ = cot if len(cot) >= 8 else cot
		self.fecha_var.set(fecha)
		self.personas_var.set(str(personas))
		self.menu_var.set(menu)
		self.precio_var.set(str(precio))
		self.notas_textbox.delete('0.0', 'end')
		self.notas_textbox.insert('0.0', notas if notas else '')
		self.total_var.set(f'${total:,.2f}')
		# Cambiar estado de botones para edición
		self.btn_guardar.configure(text='✏️ Actualizar')
		# Mostrar botón cancelar si aún no está visible
		try:
			if not self.btn_cancelar.winfo_ismapped():
				self.btn_cancelar.pack(side='left', padx=8)
		except Exception:
			# si por alguna razón el widget no está mapeable, ignorar
			pass
		self.cargar_cotizaciones()

	def guardar_cotizacion(self):
		try:
			fecha = self.fecha_var.get()
			personas = int(self.personas_var.get())
			menu = self.menu_var.get()
			precio = float(self.precio_var.get())
			notas = self.notas_textbox.get('0.0', 'end').strip()
			total = personas * precio
			# Validar fecha
			datetime.strptime(fecha, '%d/%m/%Y')
			if self.cotizacion_seleccionada.get() and self.cotizacion_seleccionada.get() != 0:
				# Actualizar cotización existente
				id_ = self.cotizacion_seleccionada.get()
				basedatos.actualizar_cotizacion_buffet(id_, fecha, personas, menu, precio, total, notas)
				messagebox.showinfo('Éxito', 'Cotización actualizada correctamente.')
			else:
				# Insertar nueva cotización
				basedatos.insertar_cotizacion_buffet(fecha, personas, menu, precio, total, notas)
				messagebox.showinfo('Éxito', 'Cotización guardada correctamente.')
			self.cargar_cotizaciones()
			# Reset estado de edición y ocultar botón cancelar si está visible
			self.cotizacion_seleccionada.set(0)
			self.btn_guardar.configure(text='💾 Guardar')
			try:
				if self.btn_cancelar.winfo_ismapped():
					self.btn_cancelar.pack_forget()
			except Exception:
				pass
		except Exception as e:
			messagebox.showerror('Error', f'Error al guardar: {e}')

	def cancelar_edicion(self):
		# Limpiar selección y formulario
		self.cotizacion_seleccionada.set(0)
		self.fecha_var.set('')
		self.personas_var.set('')
		self.menu_var.set('Clásico')
		self.precio_var.set('')
		self.notas_textbox.delete('0.0', 'end')
		self.total_var.set('$0.00')
		self.btn_guardar.configure(text='💾 Guardar')
		# Ocultar botón cancelar si está visible
		try:
			if self.btn_cancelar.winfo_ismapped():
				self.btn_cancelar.pack_forget()
		except Exception:
			pass
		self.cargar_cotizaciones()

	def eliminar_cotizacion(self, id_):
		if messagebox.askyesno('Confirmar', '¿Eliminar esta cotización?'):
			basedatos.eliminar_cotizacion_buffet(id_)
			self.cargar_cotizaciones()

	def generar_pdf(self):
		try:
			cotizaciones = basedatos.obtener_cotizaciones_buffet() if hasattr(basedatos, 'obtener_cotizaciones_buffet') else []
			id_sel = self.cotizacion_seleccionada.get()
			cotizacion = None
			for cot in cotizaciones:
				if cot[0] == id_sel:
					cotizacion = cot
					break
			if not cotizacion:
				messagebox.showwarning('PDF', 'Seleccione una cotización para exportar.')
				return
			pdf_path = os.path.join(os.getcwd(), f'cotizacion_buffet_{id_sel}.pdf')
			c = canvas.Canvas(pdf_path, pagesize=letter)
			width, height = letter
			c.setFont('Helvetica-Bold', 16)
			c.drawString(50, height - 50, 'Cotización de Buffet')
			c.setFont('Helvetica', 12)
			labels = ['ID', 'Fecha', 'Personas', 'Menú', 'Precio/persona', 'Total', 'Notas']
			y = height - 100
			for i, label in enumerate(labels):
				c.drawString(50, y, f'{label}:')
				valor = cotizacion[i] if i < 7 else ''
				if label == 'Precio/persona':
					valor = f"${cotizacion[4]:,.2f}"
				elif label == 'Total':
					valor = f"${cotizacion[5]:,.2f}"
				c.drawString(180, y, str(valor))
				y -= 30
			c.save()
			messagebox.showinfo('PDF generado', f'PDF guardado en:\n{pdf_path}')
		except Exception as e:
			messagebox.showerror('Error PDF', f'No se pudo generar el PDF:\n{e}')

# Métodos de acceso a la base de datos para buffet
def obtener_cotizaciones_buffet():
	conn = basedatos.conectar_bd()
	if conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM buffet ORDER BY fecha DESC')
		return cursor.fetchall()
	return []

def insertar_cotizacion_buffet(fecha, personas, menu, precio, total, notas):
	conn = basedatos.conectar_bd()
	if conn:
		cursor = conn.cursor()
		cursor.execute('INSERT INTO buffet (fecha, personas, menu, precio_por_persona, total, notas) VALUES (?, ?, ?, ?, ?, ?)',
					   (fecha, personas, menu, precio, total, notas))
		conn.commit()
		conn.close()

def eliminar_cotizacion_buffet(id_):
	conn = basedatos.conectar_bd()
	if conn:
		cursor = conn.cursor()
		cursor.execute('DELETE FROM buffet WHERE id = ?', (id_,))
		conn.commit()
		conn.close()
 
