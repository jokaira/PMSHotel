from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import customtkinter as ctk
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import customtkinter as ctk
from settings import *
import basedatos
from tkinter import messagebox
from datetime import datetime


class CotizacionEventos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color='transparent')
        self.pack(fill='both', expand=True)

        # Variables de formulario
        self.tipo_var = ctk.StringVar(value='Conferencia')
        self.salon_var = ctk.StringVar(value='Salón A')
        self.fecha_var = ctk.StringVar()
        self.hora_var = ctk.StringVar()
        self.equip_options = ['Proyector', 'Sonido', 'Iluminación', 'Micrófonos']
        # Soporte para selección múltiple vía modal. Se muestra solo la primera selección con "+N"
        self.selected_equip = []
        self.equip_display_var = ctk.StringVar(value='Seleccionar...')
        self.catering_var = ctk.StringVar(value='Buffet')
        self.personas_var = ctk.StringVar()
        self.tarifa_var = ctk.StringVar()
        self.total_var = ctk.StringVar(value='$0.00')
        self.notas_textbox = None
        self.cotizacion_seleccionada = ctk.IntVar(value=0)

        # Construir UI
        self.crear_formulario()
        self.crear_total_y_botones()
        self.crear_tabla()
        self.cargar_cotizaciones()

    def crear_formulario(self):
        frame = ctk.CTkFrame(self, fg_color='transparent', border_color=PRIMARIO, border_width=2, corner_radius=12)
        frame.pack(fill='x', padx=16, pady=(16, 4))

        # Configurar columnas para que se distribuyan bien
        frame.grid_columnconfigure(1, weight=3)
        frame.grid_columnconfigure(3, weight=2)
        frame.grid_columnconfigure(5, weight=1)

        # Fila 0: Tipo, Salón, Fecha
        ctk.CTkLabel(frame, text='Tipo de evento', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=0, padx=(8,2), pady=8, sticky='e')
        ctk.CTkOptionMenu(frame, variable=self.tipo_var, values=['Conferencia', 'Boda', 'Seminario', 'Cena de Gala'], width=260).grid(row=0, column=1, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Salón', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=2, padx=(8,2), pady=8, sticky='e')
        ctk.CTkOptionMenu(frame, variable=self.salon_var, values=['Salón A', 'Salón B', 'Salón C', 'Salón Principal'], width=180).grid(row=0, column=3, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Fecha', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=4, padx=(8,2), pady=8, sticky='e')
        self.date_entry = DateEntry(frame, date_pattern='dd/MM/yyyy', textvariable=self.fecha_var, width=120, background=AZUL, foreground='black', borderwidth=2, locale='es_ES')
        self.date_entry.grid(row=0, column=5, padx=(2,16), pady=8, sticky='we')

        # Fila 1: Hora, Equipamiento, Catering
        ctk.CTkLabel(frame, text='Hora', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=0, padx=(8,2), pady=8, sticky='e')
        ctk.CTkEntry(frame, textvariable=self.hora_var, width=120).grid(row=1, column=1, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Equipamiento', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=2, padx=(8,2), pady=8, sticky='e')
        # Botón que abre un modal con checkboxes para selección múltiple. En el layout se muestra sólo la primera selección +N
        btn_equip = ctk.CTkButton(frame, textvariable=self.equip_display_var, width=180, command=self.abrir_modal_equipamiento)
        btn_equip.grid(row=1, column=3, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Catering', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=4, padx=(8,2), pady=8, sticky='e')
        ctk.CTkOptionMenu(frame, variable=self.catering_var, values=['Buffet', 'Cocktail', 'Servicio a mesa', 'Sin catering'], width=180).grid(row=1, column=5, padx=(2,16), pady=8, sticky='we')

        # Fila 2: Personas y tarifa
        ctk.CTkLabel(frame, text='Nº Personas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=0, padx=(8,2), pady=8, sticky='e')
        ctk.CTkEntry(frame, textvariable=self.personas_var, width=120).grid(row=2, column=1, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Tarifa base', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=2, padx=(8,2), pady=8, sticky='e')
        ctk.CTkEntry(frame, textvariable=self.tarifa_var, width=120).grid(row=2, column=3, padx=(2,16), pady=8, sticky='we')

        # Fila 3: Notas
        ctk.CTkLabel(frame, text='Notas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=3, column=0, padx=8, pady=8, sticky='nw')
        notas_frame = ctk.CTkFrame(frame, fg_color='transparent', border_color=GRIS_CLARO2, border_width=2, corner_radius=8)
        notas_frame.grid(row=3, column=1, columnspan=4, padx=8, pady=8, sticky='nsew')
        self.notas_textbox = ctk.CTkTextbox(notas_frame, height=80, width=600, fg_color=BLANCO)
        self.notas_textbox.pack(fill='both', expand=True, padx=4, pady=4)

        # Actualizar total cuando cambien personas/tarifa
        self.personas_var.trace('w', lambda *args: self.actualizar_total())
        self.tarifa_var.trace('w', lambda *args: self.actualizar_total())

    def crear_total_y_botones(self):
        total_frame = ctk.CTkFrame(self, fg_color='transparent')
        total_frame.pack(fill='x', padx=16, pady=(0, 8))

        subt_frame = ctk.CTkFrame(total_frame, fg_color='transparent')
        subt_frame.pack(side='left', padx=(8, 12))
        self.sub_salon_var = ctk.StringVar(value='$0.00')
        self.sub_catering_var = ctk.StringVar(value='$0.00')
        self.sub_equip_var = ctk.StringVar(value='$0.00')
        ctk.CTkLabel(subt_frame, text='Salón:', font=(FUENTE, 11), text_color=OSCURO).grid(row=0, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_salon_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=0, column=1, sticky='w', padx=(6,16))
        ctk.CTkLabel(subt_frame, text='Catering:', font=(FUENTE, 11), text_color=OSCURO).grid(row=1, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_catering_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=1, column=1, sticky='w', padx=(6,16))
        ctk.CTkLabel(subt_frame, text='Equipamiento:', font=(FUENTE, 11), text_color=OSCURO).grid(row=2, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_equip_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=2, column=1, sticky='w', padx=(6,16))

        ctk.CTkLabel(total_frame, textvariable=self.total_var, font=(FUENTE, 20, 'bold'), text_color=VERDE1).pack(side='left', padx=(12, 32))

        self.btn_guardar = ctk.CTkButton(total_frame, text='💾 Guardar', fg_color=VERDE1, command=self.guardar_cotizacion)
        self.btn_guardar.pack(side='left', padx=8)
        # Button to clear the form for a new quotation
        btn_limpiar = ctk.CTkButton(total_frame, text='🧽 Limpiar', fg_color=MUTE, command=self.limpiar_formulario)
        btn_limpiar.pack(side='left', padx=8)
        btn_pdf = ctk.CTkButton(total_frame, text='🖨️ Generar PDF', fg_color=MORADO, command=self.generar_pdf)
        btn_pdf.pack(side='left', padx=8)

    def actualizar_total(self):
        try:
            personas = int(self.personas_var.get()) if self.personas_var.get() != '' else 0
            tarifa = float(self.tarifa_var.get()) if self.tarifa_var.get() != '' else 0.0

            subtotal_salon = tarifa
            catering_rate = CATERING_RATES.get(self.catering_var.get(), 0.0)
            subtotal_catering = catering_rate * personas

            equip_fees = EQUIP_FEES
            # selected_equip es una lista con las opciones seleccionadas
            selected_equip = getattr(self, 'selected_equip', []) or []
            subtotal_equip = sum(equip_fees.get(item, 0.0) for item in selected_equip)

            total = subtotal_salon + subtotal_catering + subtotal_equip

            self.sub_salon_var.set(f'${subtotal_salon:,.2f}')
            self.sub_catering_var.set(f'${subtotal_catering:,.2f}')
            self.sub_equip_var.set(f'${subtotal_equip:,.2f}')
            self.total_var.set(f'${total:,.2f}')
        except Exception:
            self.total_var.set('$0.00')

    def limpiar_formulario(self):
        # Reset form fields to defaults for a new quotation
        self.tipo_var.set('Conferencia')
        self.salon_var.set('Salón A')
        self.fecha_var.set('')
        self.hora_var.set('')
        self.selected_equip = []
        self.equip_display_var.set('Seleccionar...')
        self.catering_var.set('Buffet')
        self.personas_var.set('')
        self.tarifa_var.set('')
        self.sub_salon_var.set('$0.00')
        self.sub_catering_var.set('$0.00')
        self.sub_equip_var.set('$0.00')
        self.total_var.set('$0.00')
        if self.notas_textbox:
            self.notas_textbox.delete('0.0', 'end')
        self.cotizacion_seleccionada.set(0)
        if self.btn_guardar:
            self.btn_guardar.configure(text='💾 Guardar')

    def crear_tabla(self):
        self.tabla_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.tabla_frame.pack(fill='both', expand=True, padx=16, pady=8)
        self.tabla = None

    def cargar_cotizaciones(self):
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        encabezados = ['Sel.', 'ID', 'Tipo', 'Salón', 'Fecha', 'Personas', 'Total', '']
        for col, texto in enumerate(encabezados):
            # Use transparent background for header labels to avoid visible shading behind row widgets
            ctk.CTkLabel(self.tabla_frame, text=texto, font=(FUENTE, 13, 'bold'), fg_color='transparent', text_color=OSCURO, width=80 if col==0 else 120, anchor='center').grid(row=0, column=col, padx=2, pady=2)

        eventos = basedatos.obtener_cotizaciones_eventos() if hasattr(basedatos, 'obtener_cotizaciones_eventos') else []
        # ensure tabla_frame columns align with headers
        for col in range(8):
            self.tabla_frame.grid_columnconfigure(col, weight=1)

        for i, ev in enumerate(eventos, start=1):
            id_, tipo, salon, fecha, hora, equip, categoria, personas, tarifa, total, fecha_creacion, notas = ev
            selected = (self.cotizacion_seleccionada.get() == id_)
            row_bg = VERDE_CLARO if selected else 'transparent'

            # Place widgets directly on tabla_frame so columns align with headers
            btn_sel = ctk.CTkButton(self.tabla_frame, text='Seleccionar', width=70, fg_color=AZUL, command=lambda id_=id_: self.seleccionar_cotizacion(id_))
            btn_sel.grid(row=i, column=0, padx=4, pady=6, sticky='nsew')

            # center values and remove per-cell shading (transparent background)
            ctk.CTkLabel(self.tabla_frame, text=str(id_), width=40, anchor='center', fg_color='transparent').grid(row=i, column=1, padx=2, pady=6, sticky='nsew')
            ctk.CTkLabel(self.tabla_frame, text=tipo, width=120, anchor='center', fg_color='transparent').grid(row=i, column=2, padx=2, pady=6, sticky='nsew')
            ctk.CTkLabel(self.tabla_frame, text=salon, width=120, anchor='center', fg_color='transparent').grid(row=i, column=3, padx=2, pady=6, sticky='nsew')
            ctk.CTkLabel(self.tabla_frame, text=fecha, width=100, anchor='center', fg_color='transparent').grid(row=i, column=4, padx=2, pady=6, sticky='nsew')
            ctk.CTkLabel(self.tabla_frame, text=str(personas), width=80, anchor='center', fg_color='transparent').grid(row=i, column=5, padx=2, pady=6, sticky='nsew')
            ctk.CTkLabel(self.tabla_frame, text=f'${total:,.2f}', width=100, anchor='center', fg_color='transparent').grid(row=i, column=6, padx=2, pady=6, sticky='nsew')
            btn_eliminar = ctk.CTkButton(self.tabla_frame, text='Eliminar', fg_color=ROJO, width=70, command=lambda id_=id_: self.eliminar_cotizacion(id_))
            btn_eliminar.grid(row=i, column=7, padx=4, pady=6, sticky='nsew')

    def seleccionar_cotizacion(self, id_):
        eventos = basedatos.obtener_cotizaciones_eventos() if hasattr(basedatos, 'obtener_cotizaciones_eventos') else []
        registro = None
        for ev in eventos:
            if ev[0] == id_:
                registro = ev
                break
        if not registro:
            messagebox.showerror('Error', 'No se encontró la cotización seleccionada')
            return

        id_, tipo, salon, fecha, hora, equipamiento, categoria, personas, tarifa, total, fecha_creacion, notas = registro
        self.cotizacion_seleccionada.set(id_)
        self.tipo_var.set(tipo)
        self.salon_var.set(salon)
        self.fecha_var.set(fecha)
        self.hora_var.set(hora)
        # Si en la BD viene un string con varios items, tomamos el primero para el dropdown
        if equipamiento:
            # load CSV into selected_equip list and update display
            parts = [p.strip() for p in str(equipamiento).split(',') if p.strip()]
            self.selected_equip = parts
            if parts:
                if len(parts) > 1:
                    self.equip_display_var.set(f"{parts[0]} +{len(parts)-1}")
                else:
                    self.equip_display_var.set(parts[0])
        else:
            self.selected_equip = []
            self.equip_display_var.set('Seleccionar...')
        self.catering_var.set(categoria if categoria is not None else 'Buffet')
        self.personas_var.set(str(personas))
        self.tarifa_var.set(str(tarifa))
        self.notas_textbox.delete('0.0', 'end')
        if notas:
            self.notas_textbox.insert('0.0', notas)
        self.actualizar_total()
        if self.btn_guardar:
            self.btn_guardar.configure(text='🔄 Actualizar')

    def guardar_cotizacion(self):
        tipo = self.tipo_var.get()
        salon = self.salon_var.get()
        fecha = self.fecha_var.get()
        hora = self.hora_var.get()
        categoria = self.catering_var.get()
        notas = self.notas_textbox.get('0.0', 'end').strip()

        if fecha.strip() == '':
            messagebox.showwarning('Validación', 'La fecha es obligatoria.')
            return
        try:
            datetime.strptime(fecha, '%d/%m/%Y')
        except Exception:
            messagebox.showwarning('Validación', 'Formato de fecha inválido. Use dd/mm/aaaa.')
            return

        try:
            personas = int(self.personas_var.get())
            if personas <= 0:
                messagebox.showwarning('Validación', 'Nº Personas debe ser mayor que 0.')
                return
        except Exception:
            messagebox.showwarning('Validación', 'Nº Personas inválido.')
            return

        try:
            tarifa = float(self.tarifa_var.get())
            if tarifa < 0:
                messagebox.showwarning('Validación', 'Tarifa base inválida.')
                return
        except Exception:
            messagebox.showwarning('Validación', 'Tarifa base inválida.')
            return

        total_str = self.total_var.get().replace('$', '').replace(',', '')
        try:
            total = float(total_str)
        except Exception:
            messagebox.showerror('Error', 'No se pudo calcular el total. Revise los datos.')
            return

        try:
            # Guardar el equipamiento seleccionado como CSV
            equip_str = ','.join(self.selected_equip) if getattr(self, 'selected_equip', None) else ''
            id_sel = self.cotizacion_seleccionada.get()
            if id_sel and id_sel > 0:
                basedatos.actualizar_cotizacion_evento(id_sel, tipo, salon, fecha, hora, equip_str, categoria, personas, tarifa, total, notas)
                messagebox.showinfo('Éxito', 'Cotización actualizada correctamente.')
                self.cotizacion_seleccionada.set(0)
                if self.btn_guardar:
                    self.btn_guardar.configure(text='💾 Guardar')
            else:
                basedatos.insertar_cotizacion_evento(tipo, salon, fecha, hora, equip_str, categoria, personas, tarifa, total, notas)
                messagebox.showinfo('Éxito', 'Cotización de evento guardada correctamente.')
            self.cargar_cotizaciones()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar: {e}')

    def abrir_modal_equipamiento(self):
        # Modal con checkboxes para seleccionar múltiples equipamientos
        modal = ctk.CTkToplevel(self)
        modal.title('Seleccionar equipamiento')
        modal.geometry('360x260')
        # Make it modal and focused so it remains open until user acts
        try:
            modal.transient(self.winfo_toplevel())
        except Exception:
            pass
        try:
            modal.grab_set()
        except Exception:
            pass
        try:
            modal.focus_force()
        except Exception:
            pass
        modal.protocol('WM_DELETE_WINDOW', modal.destroy)
        checks = {}

        def aplicar():
            seleccion = [k for k, var in checks.items() if var.get()]
            self.selected_equip = seleccion
            if seleccion:
                if len(seleccion) > 1:
                    self.equip_display_var.set(f"{seleccion[0]} +{len(seleccion)-1}")
                else:
                    self.equip_display_var.set(seleccion[0])
            else:
                self.equip_display_var.set('Seleccionar...')
            self.actualizar_total()
            modal.destroy()

        for i, opt in enumerate(self.equip_options):
            var = ctk.BooleanVar(value=(opt in getattr(self, 'selected_equip', [])))
            checks[opt] = var
            ctk.CTkCheckBox(modal, text=opt, variable=var).pack(anchor='w', padx=12, pady=6)

        btn_frame = ctk.CTkFrame(modal, fg_color='transparent')
        btn_frame.pack(side='bottom', fill='x', pady=12)
        ctk.CTkButton(btn_frame, text='Cancelar', command=modal.destroy).pack(side='right', padx=12)
        ctk.CTkButton(btn_frame, text='Aplicar', fg_color=VERDE1, command=aplicar).pack(side='right', padx=12)

    def eliminar_cotizacion(self, id_):
        if messagebox.askyesno('Confirmar', '¿Eliminar esta cotización?'):
            basedatos.eliminar_cotizacion_evento(id_)
            self.cargar_cotizaciones()

    def generar_pdf(self):
        try:
            eventos = basedatos.obtener_cotizaciones_eventos() if hasattr(basedatos, 'obtener_cotizaciones_eventos') else []
            id_sel = self.cotizacion_seleccionada.get()
            cot = None
            for ev in eventos:
                if ev[0] == id_sel:
                    cot = ev
                    break
            if not cot:
                messagebox.showwarning('PDF', 'Seleccione una cotización para exportar.')
                return
            pdf_path = os.path.join(os.getcwd(), f'cotizacion_evento_{id_sel}.pdf')
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            c.setFont('Helvetica-Bold', 18)
            c.drawString(50, height - 50, 'Cotización de Evento')
            c.setFont('Helvetica', 10)
            c.drawString(50, height - 70, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}')

            x = 50
            y = height - 110
            line_h = 18
            # cot columns: id(0), tipo(1), salon(2), fecha(3), hora(4), equipamiento(5), categoria(6), personas(7), tarifa_salon(8), total(9), fecha_creacion(10), notas(11)
            rows = [
                ('ID', cot[0]),
                ('Tipo', cot[1]),
                ('Salón', cot[2]),
                ('Fecha', cot[3]),
                ('Hora', cot[4]),
                ('Equipamiento', cot[5] if cot[5] is not None else ''),
                ('Catering', cot[6]),
                ('Personas', cot[7]),
                ('Tarifa salón', f"${cot[8]:,.2f}"),
                ('Total', f"${cot[9]:,.2f}"),
                ('Notas', cot[11] if len(cot) > 11 and cot[11] is not None else '')
            ]
            for label, valor in rows:
                c.setFont('Helvetica-Bold', 10)
                c.drawString(x, y, f'{label}:')
                c.setFont('Helvetica', 10)
                c.drawString(x + 140, y, str(valor))
                y -= line_h

            c.save()
            messagebox.showinfo('PDF generado', f'PDF guardado en:\n{pdf_path}')
        except Exception as e:
            messagebox.showerror('Error PDF', f'No se pudo generar el PDF:\n{e}')
