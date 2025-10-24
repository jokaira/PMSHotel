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
import tkinter as tk
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
        # variable para mostrar el nombre seleccionado en el botón del formulario
        self.salon_btn_var = ctk.StringVar(value=self.salon_var.get())
        # variable para mostrar la capacidad al lado del selector
        self.salon_capacity_var = ctk.StringVar(value=f"Capacidad: {SALON_CAPACITIES.get(self.salon_var.get(), 0)}")
        # sincronizar salon_var -> boton
        self.salon_var.trace('w', lambda *args: self.salon_btn_var.set(self.salon_var.get()))
        self.fecha_var = ctk.StringVar()
        self.hora_inicio_var = ctk.StringVar(value='--')
        self.hora_fin_var = ctk.StringVar(value='--')
        self.equip_options = ['Proyector', 'Sonido', 'Iluminación', 'Micrófonos']
        # Soporte para selección múltiple vía modal. Se muestra solo la primera selección con "+N"
        self.selected_equip = []
        self.equip_display_var = ctk.StringVar(value='Seleccionar...')
        self.catering_var = ctk.StringVar(value='Buffet')
        # Mesas: cantidad por capacidad (4,8,12)
        self.tables_selected = {'4': 0, '8': 0, '12': 0}
        self.tables_display_var = ctk.StringVar(value='Seleccionar mesas...')
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
        ctk.CTkLabel(frame, text='Tipo de montaje', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=0, padx=(8,2), pady=8, sticky='e')
        ctk.CTkOptionMenu(frame, variable=self.tipo_var, values=['Conferencia', 'Boda', 'Seminario', 'Cena de Gala', 'Aula', 'Teatro', 'Coctel'], width=260).grid(row=0, column=1, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Salón', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=2, padx=(8,2), pady=8, sticky='e')
        # Reemplazamos el OptionMenu con un botón que abre un modal mostrando cada salón y su capacidad a la derecha
        # usar mismo azul que otros botones para consistencia
        btn_salon = ctk.CTkButton(frame, textvariable=self.salon_btn_var, width=180, command=self.abrir_modal_salones, fg_color=AZUL, hover_color=AZUL2)
        btn_salon.grid(row=0, column=3, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Fecha', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=0, column=4, padx=(8,2), pady=8, sticky='e')
        # aumentar tamaño del DateEntry para emparejar con el resto de la interfaz
        self.date_entry = DateEntry(frame, date_pattern='dd/MM/yyyy', textvariable=self.fecha_var, width=14, background=AZUL, foreground='black', borderwidth=2, locale='es_ES')
        self.date_entry.grid(row=0, column=5, padx=(2,16), pady=8, sticky='we')

        # Fila 1: Hora, Equipamiento, Catering
        ctk.CTkLabel(frame, text='Hora', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=0, padx=(8,2), pady=8, sticky='e')
        # time selectors (start -> end) using spinboxes (hour + minute) with 15-minute increments
        time_container = ctk.CTkFrame(frame, fg_color='transparent')
        time_container.grid(row=1, column=1, padx=(2,16), pady=8, sticky='we')

        # component vars for spinboxes (use tkinter StringVar for Spinbox compatibility)
        self.hora_inicio_h_var = tk.StringVar(value='--')
        self.hora_inicio_m_var = tk.StringVar(value='--')
        self.hora_inicio_ampm_var = ctk.StringVar(value='AM')
        self.hora_fin_h_var = tk.StringVar(value='--')
        self.hora_fin_m_var = tk.StringVar(value='--')
        self.hora_fin_ampm_var = ctk.StringVar(value='AM')

        # helper to compose HH:MM into the existing hora_inicio_var / hora_fin_var
        # now accepts 12-hour inputs plus AM/PM and converts to 24-hour 'HH:MM'
        def _compose_time(kind):
            if kind == 'inicio':
                h = self.hora_inicio_h_var.get()
                m = self.hora_inicio_m_var.get()
                ampm = self.hora_inicio_ampm_var.get() if getattr(self, 'hora_inicio_ampm_var', None) else 'AM'
                target = self.hora_inicio_var
            else:
                h = self.hora_fin_h_var.get()
                m = self.hora_fin_m_var.get()
                ampm = self.hora_fin_ampm_var.get() if getattr(self, 'hora_fin_ampm_var', None) else 'AM'
                target = self.hora_fin_var
            if not h or not m or h == '--' or m == '--':
                target.set('--')
            else:
                # convert 12h + AM/PM to 24h
                try:
                    hh = int(h)
                    mm = int(m)
                    if ampm.upper() == 'PM' and hh < 12:
                        hh = hh + 12
                    if ampm.upper() == 'AM' and hh == 12:
                        hh = 0
                    target.set(f"{hh:02d}:{mm:02d}")
                except Exception:
                    target.set('--')

        # hour values for 12-hour clock: include '--' + 01..12
        hour_values = ['--'] + [f"{h:02d}" for h in range(1,13)]
        # minute values: include '--' + common 15-min increments
        minute_values = ['--', '00', '15', '30', '45']

        # Start time spinboxes
        start_frame = ctk.CTkFrame(time_container, fg_color='transparent')
        start_frame.pack(side='left', padx=(0,6))
        # aumentar tamaño visual y permitir escritura manual (font y ipady para mayor altura)
        tk.Spinbox(start_frame, values=hour_values, textvariable=self.hora_inicio_h_var, width=10, wrap=True, justify='center', font=(FUENTE, 12), command=lambda: _compose_time('inicio')).pack(side='left', ipady=4)
        tk.Spinbox(start_frame, values=minute_values, textvariable=self.hora_inicio_m_var, width=10, wrap=True, justify='center', font=(FUENTE, 12), command=lambda: _compose_time('inicio')).pack(side='left', padx=(6,0), ipady=4)
        # AM/PM selector
        ctk.CTkOptionMenu(start_frame, values=['AM', 'PM'], variable=self.hora_inicio_ampm_var, width=70).pack(side='left', padx=(8,0))

        ctk.CTkLabel(time_container, text='→', text_color=OSCURO).pack(side='left')

        # End time spinboxes
        end_frame = ctk.CTkFrame(time_container, fg_color='transparent')
        end_frame.pack(side='left', padx=(6,0))
        tk.Spinbox(end_frame, values=hour_values, textvariable=self.hora_fin_h_var, width=10, wrap=True, justify='center', font=(FUENTE, 12), command=lambda: _compose_time('fin')).pack(side='left', ipady=4)
        tk.Spinbox(end_frame, values=minute_values, textvariable=self.hora_fin_m_var, width=10, wrap=True, justify='center', font=(FUENTE, 12), command=lambda: _compose_time('fin')).pack(side='left', padx=(6,0), ipady=4)
        # AM/PM selector
        ctk.CTkOptionMenu(end_frame, values=['AM', 'PM'], variable=self.hora_fin_ampm_var, width=70).pack(side='left', padx=(8,0))

        # also update composed vars when underlying StringVars change (covers programmatic sets)
        try:
            self.hora_inicio_h_var.trace('w', lambda *args: _compose_time('inicio'))
            self.hora_inicio_m_var.trace('w', lambda *args: _compose_time('inicio'))
            self.hora_inicio_ampm_var.trace('w', lambda *args: _compose_time('inicio'))
            self.hora_fin_h_var.trace('w', lambda *args: _compose_time('fin'))
            self.hora_fin_m_var.trace('w', lambda *args: _compose_time('fin'))
            self.hora_fin_ampm_var.trace('w', lambda *args: _compose_time('fin'))
        except Exception:
            # ctk.StringVar may not support trace in some versions; fall back to no-op
            pass

        ctk.CTkLabel(frame, text='Equipamiento', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=2, padx=(8,2), pady=8, sticky='e')
        # Botón que abre un modal con checkboxes para selección múltiple. En el layout se muestra sólo la primera selección +N
        btn_equip = ctk.CTkButton(frame, textvariable=self.equip_display_var, width=180, command=self.abrir_modal_equipamiento)
        btn_equip.grid(row=1, column=3, padx=(2,16), pady=8, sticky='we')

        ctk.CTkLabel(frame, text='Catering', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=1, column=4, padx=(8,2), pady=8, sticky='e')
        ctk.CTkOptionMenu(frame, variable=self.catering_var, values=['Buffet', 'Cocktail', 'Coffee break', 'Servicio a mesa', 'Sin catering'], width=180).grid(row=1, column=5, padx=(2,16), pady=8, sticky='we')

        # Fila 2: Personas y tarifa
        ctk.CTkLabel(frame, text='Nº Personas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=0, padx=(8,2), pady=8, sticky='e')
        # container para entry + warning
        personas_container = ctk.CTkFrame(frame, fg_color='transparent')
        personas_container.grid(row=2, column=1, padx=(2,16), pady=8, sticky='we')
        self.entry_personas = ctk.CTkEntry(personas_container, textvariable=self.personas_var, width=120)
        self.entry_personas.pack(side='left', fill='x', expand=True)
        self.personas_warning_var = ctk.StringVar(value='')
        ctk.CTkLabel(personas_container, textvariable=self.personas_warning_var, font=(FUENTE, 10), text_color=ROJO_CLARO).pack(side='left', padx=(8,0))
        # validar y actualizar total cuando cambien personas
        self.personas_var.trace('w', lambda *args: (self.validar_capacidad(), self.actualizar_total()))
        # revalidar si cambia el salon
        self.salon_var.trace('w', lambda *args: (self.actualizar_capacidad_salon(), self.validar_capacidad()))

        ctk.CTkLabel(frame, text='Tarifa base', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=2, padx=(8,2), pady=8, sticky='e')
        ctk.CTkEntry(frame, textvariable=self.tarifa_var, width=120).grid(row=2, column=3, padx=(2,16), pady=8, sticky='we')

        # Fila 2 (columna 4-5): Selector de Mesas (debajo de Catering)
        ctk.CTkLabel(frame, text='Mesas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=2, column=4, padx=(8,2), pady=8, sticky='e')
        btn_mesas = ctk.CTkButton(frame, textvariable=self.tables_display_var, width=180, command=self.abrir_modal_mesas)
        btn_mesas.grid(row=2, column=5, padx=(2,16), pady=8, sticky='we')

        # Fila 3: Notas
        ctk.CTkLabel(frame, text='Notas', font=(FUENTE, 13, 'bold'), text_color=OSCURO).grid(row=3, column=0, padx=8, pady=8, sticky='nw')
        notas_frame = ctk.CTkFrame(frame, fg_color='transparent', border_color=GRIS_CLARO2, border_width=2, corner_radius=8)
        notas_frame.grid(row=3, column=1, columnspan=4, padx=8, pady=8, sticky='nsew')
        self.notas_textbox = ctk.CTkTextbox(notas_frame, height=80, width=600, fg_color=BLANCO)
        self.notas_textbox.pack(fill='both', expand=True, padx=4, pady=4)

        # Actualizar total cuando cambien personas/tarifa/catering
        self.personas_var.trace('w', lambda *args: self.actualizar_total())
        self.tarifa_var.trace('w', lambda *args: self.actualizar_total())
        # actualizar cuando cambie el tipo de catering para reflejar la tarifa por persona
        self.catering_var.trace('w', lambda *args: self.actualizar_total())

    def abrir_modal_salones(self):
        """Muestra un popup con la lista de salones y su capacidad a la derecha.
        Al seleccionar uno, actualiza self.salon_var y cierra el modal."""
        modal = ctk.CTkToplevel(self)
        modal.title('Seleccionar salón')
        modal.geometry('360x260')
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

        # callback para seleccionar y cerrar
        def _select_and_close(nombre):
            self.salon_var.set(nombre)
            self.actualizar_capacidad_salon()
            # after selecting, re-validate personas against new capacity
            try:
                self.validar_capacidad()
            except Exception:
                pass
            try:
                modal.destroy()
            except Exception:
                pass

        # Contenedor con scroll si hay muchos salones (simple: pack labels)
        modal.configure(fg_color=BLANCO)
        for name, cap in SALON_CAPACITIES.items():
            row = ctk.CTkFrame(modal, fg_color=BLANCO)
            row.pack(fill='x', padx=8, pady=6)
            # usar color azul consistente y texto oscuro
            btn = ctk.CTkButton(row, text=name, fg_color=AZUL, hover_color=AZUL2, command=lambda n=name: _select_and_close(n))
            btn.pack(side='left', fill='x', expand=True)
            lbl = ctk.CTkLabel(row, text=f'Capacidad: {cap}', text_color=OSCURO)
            lbl.pack(side='right')

        # ensure capacity label on form is up-to-date
        self.salon_capacity_var.set(f"Capacidad: {SALON_CAPACITIES.get(self.salon_var.get(), 0)}")

    def actualizar_capacidad_salon(self):
        """Actualiza y guarda la capacidad del salón seleccionado.
        Método ligero para evitar AttributeError cuando se invoca desde otros lugares.
        No modifica la UI visual directamente, solo mantiene el valor en memoria
        para que otras funciones puedan consultarlo.
        """
        try:
            cap = SALON_CAPACITIES.get(self.salon_var.get(), 0)
        except Exception:
            cap = 0
        # almacenar en un atributo para uso posterior y actualizar UI
        self._current_salon_capacity = cap
        try:
            self.salon_capacity_var.set(f"Capacidad: {cap}")
        except Exception:
            pass
        return cap

    def validar_capacidad(self):
        """Valida que el número de personas no exceda la capacidad del salón seleccionado.
        Actualiza el borde del entry y el mensaje de advertencia.
        """
        try:
            personas = int(self.personas_var.get()) if self.personas_var.get() != '' else 0
        except Exception:
            personas = 0
        cap = getattr(self, '_current_salon_capacity', SALON_CAPACITIES.get(self.salon_var.get(), 0))
        # Primero comprobar el máximo global si está definido
        try:
            max_global = int(MAX_PERSONAS)
        except Exception:
            max_global = None

        if max_global is not None and personas > max_global:
            try:
                self.entry_personas.configure(border_color=ROJO)
            except Exception:
                pass
            try:
                self.personas_warning_var.set(f'Máx global {max_global}')
            except Exception:
                pass
            return False

        if cap is not None and personas > cap:
            try:
                self.entry_personas.configure(border_color=ROJO)
            except Exception:
                pass
            try:
                self.personas_warning_var.set(f'Máx {cap}')
            except Exception:
                pass
            return False

        try:
            self.entry_personas.configure(border_color=GRIS)
        except Exception:
            pass
        try:
            self.personas_warning_var.set('')
        except Exception:
            pass
        return True

    def _evento_conflicta_en_fecha_hora(self, fecha, salon, hora_inicio, hora_fin, exclude_id=None):
        """Return True if there is an existing event in the same salon and date that
        conflicts with the provided time range. Uses DB rows returned by
        basedatos.obtener_cotizaciones_eventos() and column order from
        basedatos.obtener_columnas_eventos() to locate hora/hora_inicio/hora_fin.

        Behavior (conservative):
        - If either the new event or an existing event lacks explicit times, treat as conflict.
        - Otherwise detect range overlap (inclusive) between [start,end].
        - exclude_id: skip the record with this id (useful when updating).
        """
        try:
            eventos = basedatos.obtener_cotizaciones_eventos() if hasattr(basedatos, 'obtener_cotizaciones_eventos') else []
            cols = basedatos.obtener_columnas_eventos() if hasattr(basedatos, 'obtener_columnas_eventos') else []

            # helper to find index or None
            def idx(name):
                try:
                    return cols.index(name)
                except Exception:
                    return None

            idx_id = idx('id') if idx('id') is not None else 0
            idx_salon = idx('salon') if idx('salon') is not None else 2
            idx_fecha = idx('fecha') if idx('fecha') is not None else 3
            idx_hora = idx('hora') if idx('hora') is not None else 4
            idx_hi = idx('hora_inicio')
            idx_hf = idx('hora_fin')

            def to_minutes(tstr):
                if not tstr or str(tstr).strip() in ('', '--'):
                    return None
                try:
                    parts = str(tstr).strip().split(':')
                    if len(parts) >= 2:
                        h = int(parts[0]); m = int(parts[1])
                        return h*60 + m
                except Exception:
                    return None
                return None

            new_s = to_minutes(hora_inicio)
            new_e = to_minutes(hora_fin)

            for ev in eventos:
                try:
                    ev_id = ev[idx_id] if idx_id is not None and len(ev) > idx_id else ev[0]
                except Exception:
                    ev_id = ev[0] if len(ev) > 0 else None
                if exclude_id and ev_id == exclude_id:
                    continue

                # same salon and same date only
                ev_salon = ev[idx_salon] if idx_salon is not None and len(ev) > idx_salon else (ev[2] if len(ev) > 2 else None)
                ev_fecha = ev[idx_fecha] if idx_fecha is not None and len(ev) > idx_fecha else (ev[3] if len(ev) > 3 else None)
                if ev_salon != salon or ev_fecha != fecha:
                    continue

                # extract existing times
                ev_hi = None
                ev_hf = None
                if idx_hi is not None and len(ev) > idx_hi:
                    ev_hi = ev[idx_hi]
                if idx_hf is not None and len(ev) > idx_hf:
                    ev_hf = ev[idx_hf]
                # fallback to legacy 'hora' field
                if (not ev_hi) and (not ev_hf):
                    if idx_hora is not None and len(ev) > idx_hora:
                        legacy = ev[idx_hora]
                    else:
                        legacy = ev[4] if len(ev) > 4 else None
                    if legacy and isinstance(legacy, str) and '-' in legacy:
                        a, b = [p.strip() for p in legacy.split('-', 1)]
                        ev_hi = a if a else None
                        ev_hf = b if b else None
                    else:
                        ev_hi = legacy if legacy else None
                        ev_hf = None

                ex_s = to_minutes(ev_hi)
                ex_e = to_minutes(ev_hf)

                # if either side has missing times, conservative: consider it a conflict
                if new_s is None or ex_s is None:
                    return True

                # if end missing, treat as instantaneous event (end == start)
                if new_e is None:
                    new_e = new_s
                if ex_e is None:
                    ex_e = ex_s

                # overlap inclusive: [s1,e1] intersects [s2,e2]
                if (new_s <= ex_e) and (ex_s <= new_e):
                    return True

            return False
        except Exception:
            # On unexpected error, be conservative and report conflict to avoid double-booking
            return True

    def _listar_eventos_conflictivos(self, fecha, salon, hora_inicio, hora_fin, exclude_id=None):
        """Return a list of conflicting events (each as dict) for the given salon/date/time.
        If no conflicts, returns an empty list. Uses same matching logic as _evento_conflicta_en_fecha_hora.
        """
        conflicts = []
        try:
            eventos = basedatos.obtener_cotizaciones_eventos() if hasattr(basedatos, 'obtener_cotizaciones_eventos') else []
            cols = basedatos.obtener_columnas_eventos() if hasattr(basedatos, 'obtener_columnas_eventos') else []

            def idx(name):
                try:
                    return cols.index(name)
                except Exception:
                    return None

            idx_id = idx('id') if idx('id') is not None else 0
            idx_salon = idx('salon') if idx('salon') is not None else 2
            idx_fecha = idx('fecha') if idx('fecha') is not None else 3
            idx_hora = idx('hora') if idx('hora') is not None else 4
            idx_hi = idx('hora_inicio')
            idx_hf = idx('hora_fin')

            def to_minutes(tstr):
                if not tstr or str(tstr).strip() in ('', '--'):
                    return None
                try:
                    parts = str(tstr).strip().split(':')
                    if len(parts) >= 2:
                        h = int(parts[0]); m = int(parts[1])
                        return h*60 + m
                except Exception:
                    return None
                return None

            new_s = to_minutes(hora_inicio)
            new_e = to_minutes(hora_fin)

            for ev in eventos:
                try:
                    ev_id = ev[idx_id] if idx_id is not None and len(ev) > idx_id else ev[0]
                except Exception:
                    ev_id = ev[0] if len(ev) > 0 else None
                if exclude_id and ev_id == exclude_id:
                    continue

                ev_salon = ev[idx_salon] if idx_salon is not None and len(ev) > idx_salon else (ev[2] if len(ev) > 2 else None)
                ev_fecha = ev[idx_fecha] if idx_fecha is not None and len(ev) > idx_fecha else (ev[3] if len(ev) > 3 else None)
                if ev_salon != salon or ev_fecha != fecha:
                    continue

                ev_hi = None
                ev_hf = None
                if idx_hi is not None and len(ev) > idx_hi:
                    ev_hi = ev[idx_hi]
                if idx_hf is not None and len(ev) > idx_hf:
                    ev_hf = ev[idx_hf]
                if (not ev_hi) and (not ev_hf):
                    if idx_hora is not None and len(ev) > idx_hora:
                        legacy = ev[idx_hora]
                    else:
                        legacy = ev[4] if len(ev) > 4 else None
                    if legacy and isinstance(legacy, str) and '-' in legacy:
                        a, b = [p.strip() for p in legacy.split('-', 1)]
                        ev_hi = a if a else None
                        ev_hf = b if b else None
                    else:
                        ev_hi = legacy if legacy else None
                        ev_hf = None

                ex_s = to_minutes(ev_hi)
                ex_e = to_minutes(ev_hf)

                # if either side missing times, treat as conflict
                if new_s is None or ex_s is None:
                    conflicts.append({'id': ev_id, 'salon': ev_salon, 'fecha': ev_fecha, 'hora_inicio': ev_hi, 'hora_fin': ev_hf, 'legacy': ev[idx_hora] if idx_hora is not None and len(ev) > idx_hora else (ev[4] if len(ev) > 4 else None)})
                    continue

                if new_e is None:
                    new_e = new_s
                if ex_e is None:
                    ex_e = ex_s

                if (new_s <= ex_e) and (ex_s <= new_e):
                    conflicts.append({'id': ev_id, 'salon': ev_salon, 'fecha': ev_fecha, 'hora_inicio': ev_hi, 'hora_fin': ev_hf, 'legacy': ev[idx_hora] if idx_hora is not None and len(ev) > idx_hora else (ev[4] if len(ev) > 4 else None)})

            return conflicts
        except Exception:
            # on error, return a single conservative conflict marker
            return [{'id': None, 'salon': salon, 'fecha': fecha, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin, 'legacy': None}]

    def _mostrar_dialogo_conflictos(self, conflicts):
        """Show a modal dialog listing conflicts. Each conflict will show id, fecha, salon and times.
        Allows selecting a conflicting event to load it in the form for review.
        """
        modal = ctk.CTkToplevel(self)
        modal.title('Conflictos encontrados')
        modal.geometry('560x320')
        try:
            modal.transient(self.winfo_toplevel())
        except Exception:
            pass
        try:
            modal.grab_set()
        except Exception:
            pass

        lbl = ctk.CTkLabel(modal, text='Se encontraron eventos que confligen con la fecha/hora seleccionada:', anchor='w')
        lbl.pack(fill='x', padx=12, pady=(12,6))

        content = ctk.CTkFrame(modal, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=12, pady=6)

        # list each conflict with a Select button
        for c in conflicts:
            row = ctk.CTkFrame(content, fg_color=BLANCO, corner_radius=6)
            row.pack(fill='x', pady=6)
            txt = f"ID: {c.get('id', '')}  |  Fecha: {c.get('fecha', '')}  |  Salón: {c.get('salon', '')}  |  Hora: {c.get('hora_inicio') or ''}{(' - ' + str(c.get('hora_fin'))) if c.get('hora_fin') else ''}"
            ctk.CTkLabel(row, text=txt, anchor='w').pack(side='left', padx=8, pady=8, fill='x', expand=True)
            def make_sel(mid):
                return lambda: (self.seleccionar_cotizacion(mid), modal.destroy())
            sel_btn = ctk.CTkButton(row, text='Seleccionar', width=100, command=make_sel(c.get('id')))
            sel_btn.pack(side='right', padx=8, pady=6)

        btn_frame = ctk.CTkFrame(modal, fg_color='transparent')
        btn_frame.pack(fill='x', pady=10)
        ctk.CTkButton(btn_frame, text='Cerrar', command=modal.destroy).pack(side='right', padx=12)

    def crear_total_y_botones(self):
        total_frame = ctk.CTkFrame(self, fg_color='transparent')
        total_frame.pack(fill='x', padx=16, pady=(0, 8))

        subt_frame = ctk.CTkFrame(total_frame, fg_color='transparent')
        subt_frame.pack(side='left', padx=(8, 12))
        self.sub_salon_var = ctk.StringVar(value='$0.00')
        self.sub_catering_var = ctk.StringVar(value='$0.00')
        self.sub_equip_var = ctk.StringVar(value='$0.00')
        self.sub_mesas_var = ctk.StringVar(value='$0.00')
        ctk.CTkLabel(subt_frame, text='Salón:', font=(FUENTE, 11), text_color=OSCURO).grid(row=0, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_salon_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=0, column=1, sticky='w', padx=(6,16))
        ctk.CTkLabel(subt_frame, text='Catering:', font=(FUENTE, 11), text_color=OSCURO).grid(row=1, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_catering_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=1, column=1, sticky='w', padx=(6,16))
        ctk.CTkLabel(subt_frame, text='Equipamiento:', font=(FUENTE, 11), text_color=OSCURO).grid(row=2, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_equip_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=2, column=1, sticky='w', padx=(6,16))
        ctk.CTkLabel(subt_frame, text='Mesas:', font=(FUENTE, 11), text_color=OSCURO).grid(row=3, column=0, sticky='w')
        ctk.CTkLabel(subt_frame, textvariable=self.sub_mesas_var, font=(FUENTE, 11), text_color=OSCURO).grid(row=3, column=1, sticky='w', padx=(6,16))

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

            # calcular asientos totales y costo de mesas
            tables = getattr(self, 'tables_selected', {'4':0,'8':0,'12':0})
            seats_total = 0
            costo_mesas = 0.0
            try:
                from settings import TABLE_FEES
            except Exception:
                TABLE_FEES = {'4':5.0,'8':8.0,'12':12.0}
            for size, count in tables.items():
                try:
                    size_int = int(size)
                except Exception:
                    size_int = 0
                try:
                    cnt = int(count)
                except Exception:
                    cnt = 0
                seats_total += size_int * cnt
                costo_mesas += TABLE_FEES.get(size, 0.0) * cnt

            total = subtotal_salon + subtotal_catering + subtotal_equip + costo_mesas

            self.sub_salon_var.set(f'${subtotal_salon:,.2f}')
            # Mostrar solo el subtotal numérico del catering en la prefactura
            try:
                self.sub_catering_var.set(f'${subtotal_catering:,.2f}')
            except Exception:
                self.sub_catering_var.set(f'${subtotal_catering:,.2f}')
            self.sub_equip_var.set(f'${subtotal_equip:,.2f}')
            self.sub_mesas_var.set(f'${costo_mesas:,.2f}')
            self.total_var.set(f'${total:,.2f}')

            # Advertencia si los asientos proporcionados son menores al número de personas
            try:
                if seats_total > 0 and personas > seats_total:
                    self.personas_warning_var.set(f'Asientos insuficientes ({seats_total})')
                    try:
                        self.entry_personas.configure(border_color=ROJO)
                    except Exception:
                        pass
                else:
                    # revalidar capacidad normal
                    self.validar_capacidad()
            except Exception:
                pass
        except Exception:
            self.total_var.set('$0.00')

    def limpiar_formulario(self):
        # Reset form fields to defaults for a new quotation
        self.tipo_var.set('Conferencia')
        self.salon_var.set('Salón A')
        self.fecha_var.set('')
        self.hora_inicio_var.set('--')
        self.hora_fin_var.set('--')
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
            # safe unpacking to tolerate additional columns (mesas, asientos, costo)
            id_ = ev[0] if len(ev) > 0 else ''
            tipo = ev[1] if len(ev) > 1 else ''
            salon = ev[2] if len(ev) > 2 else ''
            fecha = ev[3] if len(ev) > 3 else ''
            hora = ev[4] if len(ev) > 4 else ''
            equip = ev[5] if len(ev) > 5 else ''
            categoria = ev[6] if len(ev) > 6 else ''
            personas = ev[7] if len(ev) > 7 else 0
            tarifa = ev[8] if len(ev) > 8 else 0.0
            total = ev[9] if len(ev) > 9 else 0.0
            fecha_creacion = ev[10] if len(ev) > 10 else ''
            notas = ev[11] if len(ev) > 11 else ''
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

        # DB schema may include mesas_csv, asientos_totales, costo_mesas at the end
        id_ = registro[0]
        tipo = registro[1] if len(registro) > 1 else ''
        salon = registro[2] if len(registro) > 2 else ''
        fecha = registro[3] if len(registro) > 3 else ''
        hora = registro[4] if len(registro) > 4 else ''
        hora_inicio_reg = registro[15] if len(registro) > 15 else None
        hora_fin_reg = registro[16] if len(registro) > 16 else None
        equipamiento = registro[5] if len(registro) > 5 else ''
        categoria = registro[6] if len(registro) > 6 else ''
        personas = registro[7] if len(registro) > 7 else 0
        tarifa = registro[8] if len(registro) > 8 else 0.0
        total = registro[9] if len(registro) > 9 else 0.0
        fecha_creacion = registro[10] if len(registro) > 10 else ''
        notas = registro[11] if len(registro) > 11 else ''
        mesas_csv = registro[12] if len(registro) > 12 else ''
        asientos_totales = registro[13] if len(registro) > 13 else 0
        costo_mesas = registro[14] if len(registro) > 14 else 0.0

        self.cotizacion_seleccionada.set(id_)
        self.tipo_var.set(tipo)
        self.salon_var.set(salon)
        self.fecha_var.set(fecha)
        # prefer explicit hora_inicio/hora_fin if available in DB
        if hora_inicio_reg is not None or hora_fin_reg is not None:
            self.hora_inicio_var.set(hora_inicio_reg if hora_inicio_reg else '--')
            self.hora_fin_var.set(hora_fin_reg if hora_fin_reg else '--')
        else:
            # fallback: parse legacy single 'hora' field which may contain a range like '08:00 - 10:00'
            try:
                if hora and isinstance(hora, str) and '-' in hora:
                    a, b = [p.strip() for p in hora.split('-', 1)]
                    self.hora_inicio_var.set(a if a else '--')
                    self.hora_fin_var.set(b if b else '--')
                else:
                    self.hora_inicio_var.set(hora if hora else '--')
                    self.hora_fin_var.set('--')
            except Exception:
                self.hora_inicio_var.set('--')
                self.hora_fin_var.set('--')
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
        # load mesas from CSV if present
        try:
            self.tables_selected = {'4':0,'8':0,'12':0}
            if mesas_csv:
                parts = [p.strip() for p in str(mesas_csv).split(',') if p.strip()]
                for p in parts:
                    if ':' in p:
                        k, v = p.split(':', 1)
                        try:
                            self.tables_selected[k] = int(v)
                        except Exception:
                            self.tables_selected[k] = 0
            # update display: show simple legend when any selection exists
            any_selected = any(int(self.tables_selected.get(k, 0)) > 0 for k in ('4', '8', '12'))
            if any_selected:
                self.tables_display_var.set('Cambiar seleccion')
            else:
                self.tables_display_var.set('Seleccionar mesas...')
        except Exception:
            pass
        self.actualizar_total()
        if self.btn_guardar:
            self.btn_guardar.configure(text='🔄 Actualizar')

    def guardar_cotizacion(self):
        tipo = self.tipo_var.get()
        salon = self.salon_var.get()
        fecha = self.fecha_var.get()
        hora_inicio = self.hora_inicio_var.get() if getattr(self, 'hora_inicio_var', None) else None
        hora_fin = self.hora_fin_var.get() if getattr(self, 'hora_fin_var', None) else None
        # build legacy 'hora' string for compatibility
        if hora_inicio and hora_inicio != '--' and hora_fin and hora_fin != '--':
            hora = f"{hora_inicio} - {hora_fin}"
        elif hora_inicio and hora_inicio != '--':
            hora = hora_inicio
        else:
            hora = ''
        # validate time range if both provided
        if hora_inicio and hora_inicio != '--' and hora_fin and hora_fin != '--':
            try:
                h1, m1 = [int(x) for x in hora_inicio.split(':')]
                h2, m2 = [int(x) for x in hora_fin.split(':')]
                if (h1 * 60 + m1) >= (h2 * 60 + m2):
                    messagebox.showwarning('Validación', 'La hora de inicio debe ser anterior a la hora de fin.')
                    return
            except Exception:
                # if parsing fails, let other validations catch it
                pass
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

        # Comprobar límite global antes de guardar (MAX_PERSONAS en settings)
        try:
            max_global = int(MAX_PERSONAS)
        except Exception:
            max_global = None
        if max_global is not None and personas > max_global:
            messagebox.showwarning('Capacidad excedida', f'El número de personas excede el máximo global de {max_global}. Ajusta el número antes de guardar.')
            return

        # Comprobar aforo antes de guardar (capacidad del salón)
        capacidad = getattr(self, '_current_salon_capacity', None)
        if capacidad is None:
            capacidad = SALON_CAPACITIES.get(salon, None)
        if capacidad is not None and personas > capacidad:
            messagebox.showwarning('Capacidad excedida', f'El salón seleccionado tiene capacidad máxima de {capacidad} personas. Ajusta el número de personas o cambia el salón antes de guardar.')
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
            # serializar mesas como CSV tipo: '4:2,8:1,12:0'
            mesas_csv = ','.join([f"{k}:{v}" for k, v in self.tables_selected.items() if int(v) > 0]) if getattr(self, 'tables_selected', None) else ''
            # calcular asientos totales y costo_mesas para persistencia
            seats_total = 0
            costo_mesas = 0.0
            try:
                from settings import TABLE_FEES
            except Exception:
                TABLE_FEES = {'4':5.0,'8':8.0,'12':12.0}
            for k, v in (self.tables_selected or {}).items():
                try:
                    cnt = int(v)
                except Exception:
                    cnt = 0
                try:
                    size = int(k)
                except Exception:
                    size = 0
                seats_total += size * cnt
                costo_mesas += TABLE_FEES.get(k, 0.0) * cnt

            # Check for conflicting event (same salon + same date + overlapping time)
            # exclude current id when updating
            try:
                conflicts = self._listar_eventos_conflictivos(fecha, salon, hora_inicio, hora_fin, exclude_id=(id_sel if id_sel and id_sel > 0 else None))
                if conflicts:
                    self._mostrar_dialogo_conflictos(conflicts)
                    return
            except Exception:
                # On any error while checking conflicts, be conservative and block the save
                messagebox.showwarning('Conflicto', 'No se pudo verificar conflictos. Ajuste la fecha/hora o inténtelo de nuevo.')
                return

            if id_sel and id_sel > 0:
                basedatos.actualizar_cotizacion_evento(id_sel, tipo, salon, fecha, hora, equip_str, categoria, personas, tarifa, total, notas, hora_inicio=hora_inicio, hora_fin=hora_fin, mesas_csv=mesas_csv, asientos_totales=seats_total, costo_mesas=costo_mesas)
                messagebox.showinfo('Éxito', 'Cotización actualizada correctamente.')
                self.cotizacion_seleccionada.set(0)
                if self.btn_guardar:
                    self.btn_guardar.configure(text='💾 Guardar')
            else:
                basedatos.insertar_cotizacion_evento(tipo, salon, fecha, hora, equip_str, categoria, personas, tarifa, total, notas, hora_inicio=hora_inicio, hora_fin=hora_fin, mesas_csv=mesas_csv, asientos_totales=seats_total, costo_mesas=costo_mesas)
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

    def abrir_modal_mesas(self):
        """Modal para seleccionar cantidades de mesas: 4, 8 y 12 personas."""
        modal = ctk.CTkToplevel(self)
        modal.title('Seleccionar Mesas')
        modal.geometry('360x240')
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

        # spinboxes para cada tipo de mesa
        frame = ctk.CTkFrame(modal, fg_color=BLANCO)
        frame.pack(fill='both', expand=True, padx=12, pady=12)

        # Helper to create a small control with - [entry] +
        def make_counter(row, label_text, initial):
            ctk.CTkLabel(frame, text=label_text, text_color=OSCURO).grid(row=row, column=0, sticky='w', pady=6)
            ent = ctk.CTkEntry(frame, width=60, justify='center')
            ent.grid(row=row, column=1, sticky='e', pady=6)
            ent.insert(0, str(initial))
            def dec():
                try:
                    v = int(ent.get())
                except Exception:
                    v = 0
                if v > 0:
                    ent.delete(0, 'end'); ent.insert(0, str(v-1))
            def inc():
                try:
                    v = int(ent.get())
                except Exception:
                    v = 0
                ent.delete(0, 'end'); ent.insert(0, str(v+1))
            btns = ctk.CTkFrame(frame, fg_color='transparent')
            btns.grid(row=row, column=2, sticky='w', padx=(8,0))
            ctk.CTkButton(btns, text='-', width=24, command=dec).pack(side='left', padx=2)
            ctk.CTkButton(btns, text='+', width=24, command=inc).pack(side='left', padx=2)
            return ent

        e4 = make_counter(0, 'Mesas para 4 personas:', self.tables_selected.get('4', 0))
        e8 = make_counter(1, 'Mesas para 8 personas:', self.tables_selected.get('8', 0))
        e12 = make_counter(2, 'Mesas para 12 personas:', self.tables_selected.get('12', 0))

        def aplicar_mesas():
            try:
                self.tables_selected['4'] = int(e4.get())
                self.tables_selected['8'] = int(e8.get())
                self.tables_selected['12'] = int(e12.get())
            except Exception:
                pass
            # actualizar display compacto: si hay alguna selección mostrar "Cambiar seleccion"
            any_selected = any(int(self.tables_selected.get(k, 0)) > 0 for k in ('4', '8', '12'))
            if any_selected:
                self.tables_display_var.set('Cambiar seleccion')
            else:
                self.tables_display_var.set('Seleccionar mesas...')
            # actualizar totales y validación
            try:
                self.actualizar_total()
            except Exception:
                pass
            modal.destroy()

        btn_frame = ctk.CTkFrame(modal, fg_color='transparent')
        btn_frame.pack(side='bottom', fill='x', pady=12)
        ctk.CTkButton(btn_frame, text='Cancelar', command=modal.destroy).pack(side='right', padx=8)
        ctk.CTkButton(btn_frame, text='Aplicar', fg_color=VERDE1, command=aplicar_mesas).pack(side='right', padx=8)

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
            # calcular subtotal de catering usando la categoría y el número de personas
            try:
                catering_cat = cot[6] if len(cot) > 6 else None
                personas_pdf = int(cot[7]) if len(cot) > 7 and cot[7] is not None else 0
            except Exception:
                catering_cat = cot[6] if len(cot) > 6 else None
                personas_pdf = 0
            try:
                catering_rate_pdf = CATERING_RATES.get(catering_cat, 0.0)
            except Exception:
                catering_rate_pdf = 0.0
            subtotal_catering_pdf = catering_rate_pdf * personas_pdf
            # parse mesas info if present (indices may vary depending on DB schema)
            mesas_csv = cot[12] if len(cot) > 12 else ''
            asientos_totales_pdf = cot[13] if len(cot) > 13 else 0
            costo_mesas_pdf = cot[14] if len(cot) > 14 else 0.0

            # build mesas breakdown lines
            mesas_lines = []
            try:
                from settings import TABLE_FEES
            except Exception:
                TABLE_FEES = {'4':5.0,'8':8.0,'12':12.0}
            if mesas_csv:
                parts = [p.strip() for p in str(mesas_csv).split(',') if p.strip()]
                for p in parts:
                    if ':' in p:
                        k, v = p.split(':', 1)
                        try:
                            cnt = int(v)
                        except Exception:
                            cnt = 0
                        fee = TABLE_FEES.get(k, 0.0)
                        line_total = fee * cnt
                        mesas_lines.append((f'Mesas {k}p', f'{cnt} x ${fee:,.2f} = ${line_total:,.2f}'))

            rows = [
                ('ID', cot[0]),
                ('Tipo', cot[1]),
                ('Salón', cot[2]),
                ('Fecha', cot[3]),
                ('Hora', cot[4]),
                ('Equipamiento', cot[5] if cot[5] is not None else ''),
                # Mostrar Personas, luego tarifa por persona, luego el subtotal de catering
                ('Personas', cot[7]),
                ('Tarifa por persona', f"${catering_rate_pdf:,.2f}/p"),
                # Mostrar sólo el subtotal numérico del catering en el PDF
                ('Catering', f"${subtotal_catering_pdf:,.2f}"),
            ]

            # append mesas breakdown (each table type) then a costo mesas and asiento total
            for label, valor in mesas_lines:
                rows.append((label, valor))
            if costo_mesas_pdf and costo_mesas_pdf != 0.0:
                rows.append(('Costo mesas', f'${costo_mesas_pdf:,.2f}'))
            if asientos_totales_pdf and asientos_totales_pdf != 0:
                rows.append(('Asientos totales', str(asientos_totales_pdf)))

            # continue with remaining rows
            rows.extend([
                ('Tarifa salón', f"${cot[8]:,.2f}"),
                ('Total', f"${cot[9]:,.2f}"),
                ('Notas', cot[11] if len(cot) > 11 and cot[11] is not None else '')
            ])
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
