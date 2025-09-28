import customtkinter as ctk
from settings import *
from func_clases import *
from tkinter import messagebox

class GestorLogistica(ctk.CTkFrame):
    #TODO: hacer pestaña aparte para los turnos
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #variables
        self.selec = []
        self.hab_sucia = ctk.StringVar()
        self.personal_housekeeping = ctk.StringVar()
        self.busqueda_var = ctk.StringVar()

        #pestañas
        self.contenedor_pestanas = ctk.CTkFrame(master=self, fg_color='transparent')
        self.contenedor_pestanas.pack(anchor = 'n',fill = 'x', pady = (0,8))
        self.boton_pestanas(master=self.contenedor_pestanas)

        self.logistica = ctk.CTkFrame(master=self, fg_color='transparent', border_color=GRIS_CLARO3, corner_radius=10, border_width=0)
        self.logistica.pack(anchor = 'n', fill = 'x')

        self.housekeeping()

    def boton_pestanas(self, master):
            self.btn_housekeeping = ctk.CTkButton(master=master, 
                          text= 'Housekeeping',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.housekeeping,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_housekeeping.pack(side ='left')

            self.btn_mantenimiento = ctk.CTkButton(master=master, 
                          text= 'Mantenimiento',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_mantenimiento.pack(side ='left', padx = (10,5))

            self.btn_inventario = ctk.CTkButton(master=master, 
                          text= 'Inventario',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.inventario,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_inventario.pack(side ='left', padx = 5)

            self.btn_personal = ctk.CTkButton(master=master, 
                          text= 'Personal',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_personal.pack(side ='left', padx = 5)

            self.btn_turnos = ctk.CTkButton(master=master, 
                          text= 'Turnos',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= "",
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_turnos.pack(side ='left', padx = 5)

    def housekeeping(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_housekeeping.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_turnos.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)
        
        #kpi de housekeeping
        self.kpis = ctk.CTkFrame(master=self.logistica, fg_color='transparent', corner_radius=0)
        self.kpis.pack(anchor = 'n',fill = 'x')

        self.kpis.rowconfigure(index=0, weight=0, minsize=109)
        self.kpis.rowconfigure(index=1, weight=0)
        self.kpis.columnconfigure(index=(0,1,2,3), weight=1, uniform='c')
        crear_tarjetas_kpi(master=self.kpis, dict=KPI_HOUSEKEEPING())

        frame_asignar = ctk.CTkFrame(master=self.logistica, 
                                     fg_color='transparent',
                                     border_color=GRIS_CLARO3,
                                     border_width=1,
                                     corner_radius=12
                                     )
        frame_asignar.pack(fill = 'x', anchor = 'n')
        
        ctk.CTkLabel(master=frame_asignar, text="📋 Asignar Limpieza", font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'), text_color=OSCURO).pack(anchor = 'w', padx = 15, pady = (12,10))
        
        frame_entrys = ctk.CTkFrame(master=frame_asignar, fg_color='transparent')
        frame_entrys.pack(fill = 'x', anchor = 'n', padx = 15, pady = (0,9))

        #habitacion
        ctk.CTkLabel(master=frame_entrys, text="Habitación:", font=(FUENTE, TAMANO_TEXTO_DEFAULT), text_color=OSCURO).pack(side = 'left', anchor = 'w', padx = (0,15))
        hab_sucias = basedatos.obtener_hab_sucias() if basedatos.obtener_hab_sucias() else ['No hay habitaciones sucias']
        self.hab_sucia.set(hab_sucias[0])

        ctk.CTkComboBox(master=frame_entrys,
                        values = hab_sucias,
                        variable= self.hab_sucia,
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35, width = 300).pack(side = 'left', anchor = 'w', padx = (0,15))
        
        #personal
        ctk.CTkLabel(master=frame_entrys, text="Asignar a:", font=(FUENTE, TAMANO_TEXTO_DEFAULT), text_color=OSCURO).pack(side = 'left', anchor = 'w', padx = (0,15))
        emp_hk = basedatos.obtener_personal_housekeeping() if basedatos.obtener_personal_housekeeping() else ['No hay empleados de housekeeping']
        self.personal_housekeeping.set(emp_hk[0])
        ctk.CTkComboBox(master=frame_entrys,
                        values = emp_hk,
                        variable=self.personal_housekeeping,
                        corner_radius=8,
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color= GRIS_CLARO2,
                        border_width=1, height=35, width = 200).pack(side = 'left', anchor = 'w', padx = (0,15))
        
        #boton
        btn_asignar = Boton(master=frame_entrys,texto='🔄 Asignar Limpieza', metodo=self.asignar_limpieza)

        frame_plan = ctk.CTkFrame(master=self.logistica, 
                                     fg_color='transparent',
                                     border_color=GRIS_CLARO3,
                                     border_width=1,
                                     corner_radius=12
                                     )
        frame_plan.pack(fill = 'both', anchor = 'n', pady = 8)

        ctk.CTkLabel(master=frame_plan, text="📊 Plan de Limpieza del Día", font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'), text_color=OSCURO).pack(anchor = 'w', padx = 15, pady = (15,5))

        #contenedor de tabla del plan de housekeeping
        self.contenedor_tabla = ctk.CTkFrame(frame_plan, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='x', expand=True, padx = 12, pady = (0,12))

        #plan de housekeeping
        self.crear_tabla(data=[ENCABEZADOS_HOUSEKEEPING] + [p for p in PLAN_HOUSEKEEPING()])

        btn_frame = ctk.CTkFrame(frame_plan, fg_color="transparent")
        btn_frame.pack(fill = 'x', anchor = 'n', padx = 12, pady = 12)

        btn_completar = Boton(master=btn_frame,
                           texto='Marcar como Completado',
                           color=VERDE1,
                           hover=VERDE2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo=self.completar_limpieza
                           )
    
    def crear_tabla(self, data): 
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', padx = 12, pady = 12)

        #resaltado segun estado
        colores = {
                    'Completado': VERDE1, 
                    'En proceso': AZUL
                  }

        self.celdas = []
        for f, fila in enumerate(data):
            fila_widgets = []
            for c, texto in enumerate(fila):
                  #coloreado de las lineas
                  if f == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                  elif f % 2 == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, 12)
                  else:
                    bg = GRIS_CLARO4
                    fg = OSCURO
                    font = (FUENTE, 12)

                  if c == 5 and f != 0:
                    try:
                          texto = datetime.strftime(datetime.strptime(texto, '%Y-%m-%d'),'%d-%m-%Y')
                    except ValueError:
                        pass
                
                  if c == 4 and f != 0:
                    try:
                          texto = datetime.strftime(datetime.strptime(texto, '%Y-%m-%d'),'%d-%m-%Y')
                    except ValueError:
                        pass

                  #resaltado de estado con "pilas"
                  if texto in colores:
                      cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                      cont_pila.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                      pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height = 28)
                      pila.pack(fill = 'y')

                      lbl = ctk.CTkLabel(master=pila, text=texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                      lbl.pack(expand = True, padx = 8, pady = 2)

                      if f > 0:
                        lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion(fila))
                    widget_celda = (lbl, False)
                  
                  frame.grid_columnconfigure(c, weight=1)

                  #borde encabezado
                  if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column = c, sticky = 'ew')
                    borde.grid_propagate(False)
                    borde.configure(height = 2)

                  #bind capturando fila
                  
                  fila_widgets.append(widget_celda)
            self.celdas.append(fila_widgets) 

    def seleccion(self, fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w, _ in self.celdas[fila]]
        self.selec = valores
        print(self.selec)

        #resaltado
        for f, fila_widgets in enumerate(self.celdas):
            for w, es_badge in fila_widgets:
                if es_badge:
                    continue
    
                if f == fila:
                    w.configure(fg_color = AZUL_CLARO)
                else:
                    if f == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    elif f % 2 == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    else:
                        default_bg = GRIS_CLARO4
                        default_text = OSCURO

                    w.configure(fg_color=default_bg, text_color=default_text)       

    def asignar_limpieza(self):
        if self.hab_sucia.get().strip() == 'No hay habitaciones sucias':
            messagebox.showerror('Error','No hay habitaciones pendientes de asignar')
            return
        
        if self.personal_housekeeping.get().strip() == 'No hay empleados de housekeeping':
            messagebox.showerror('Error','No hay empleados de housekeeping activos')
            return
        
        nro_hab = self.hab_sucia.get().strip()[:3]
        cod_emp = self.personal_housekeeping.get().strip()[:6]

        data = [
            nro_hab,
            basedatos.id_empleado(cod_emp)
        ]
        
        limpieza_asignada, mensaje_limpieza = basedatos.asignar_limpieza(datos=data)
        if not limpieza_asignada:
            messagebox.showerror('Error', mensaje_limpieza)

        messagebox.showinfo("Limpieza asignada", "La limpieza fue asignada exitosamente")

        #actualizar tabla
        from settings import PLAN_HOUSEKEEPING
        self.crear_tabla(data=[ENCABEZADOS_HOUSEKEEPING] + [p for p in PLAN_HOUSEKEEPING()])

    def completar_limpieza(self):
        if self.selec is None:
            messagebox.showerror('Error','Debe seleccionar una habitacion en proceso de limpieza')
            return
        
        data = [
            self.selec[0],
            self.selec[1][:3]
        ]

        limpieza_completada, mensaje_limpieza = basedatos.completar_limpieza(datos=data)
        if not limpieza_completada:
            messagebox.showerror('Error', mensaje_limpieza)

        messagebox.showinfo("Limpieza completada", "La limpieza fue marcada como completada exitosamente")

        #actualizar tabla
        from settings import PLAN_HOUSEKEEPING, KPI_HOUSEKEEPING
        for w in self.kpis.winfo_children():
             w.destroy()

        crear_tarjetas_kpi(master=self.kpis, dict=KPI_HOUSEKEEPING())
        self.crear_tabla(data=[ENCABEZADOS_HOUSEKEEPING] + [p for p in PLAN_HOUSEKEEPING()])

    def inventario(self): #TODO: crear modales de agregar item y hacer transacción
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_inventario.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_housekeeping.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_turnos.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)

        inventario_actual = ctk.CTkFrame(master=self.logistica, 
                                              fg_color='transparent',
                                              border_color=GRIS_CLARO3,
                                              border_width=1,
                                              corner_radius=10)
        inventario_actual.pack(fill = 'x', anchor = 'n', pady = 8)

        ctk.CTkLabel(master=inventario_actual, text='Suministros actuales', text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')).pack(anchor = 'w', padx = 15, pady = (12,8))

        frame_busqueda = ctk.CTkFrame(master=inventario_actual, fg_color='transparent')
        frame_busqueda.pack(fill = 'x', anchor = 'n', padx = 15, pady = (0,8))

        ctk.CTkLabel(master=frame_busqueda, text='Artículo', text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT)).pack(side = 'left',anchor = 'w', padx = (0,15))
        ctk.CTkEntry(master=frame_busqueda, placeholder_text='ID o Descripción',
                     placeholder_text_color=GRIS_CLARO2,
                     textvariable=self.busqueda_var,
                     corner_radius=8,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35).pack(side = 'left',anchor = 'w', padx = (0,15), fill = 'x', expand = True)
        
        btn_buscar = Boton (master=frame_busqueda,
                           texto = 'Buscar', 
                           fill=None, 
                           padx=(12,6),
                           metodo=self.buscar_articulo
                           )

        btn_limpiar = Boton(master=frame_busqueda,
                            texto='Limpiar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None,
                            metodo=self.limpiar_busqueda_art
                            )
        
        btn_nuevo_item = Boton(master=frame_busqueda,
                            texto='Agregar artículo',
                            color=VERDE1,
                            hover=VERDE2,
                            padx=6,
                            fill=None,
                            metodo= lambda: self.modal_inventario('agregar')
                            )
        
        btn_nueva_trans = Boton(master=frame_busqueda,
                            texto='Hacer transacción',
                            color=MAMEY,
                            hover=MAMEY2,
                            padx=6,
                            fill=None
                            )

        self.contenedor_tabla = ctk.CTkFrame(inventario_actual, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = (0,8))

        #inventario actual
        self.tabla_inventario([ENCABEZADOS_INVENTARIO] + [a for a in INVENTARIO()])

        btn_editar = Boton(master=inventario_actual,
                            texto='Editar artículo',
                            padx=6,
                            fill=None,
                            altura=25,
                            pady=(0,5),
                            metodo=lambda: self.modal_inventario(tipo='editar')
                            )

        #últimas transacciones
        historial_transacciones = ctk.CTkFrame(master=self.logistica, 
                                              fg_color='transparent',
                                              border_color=GRIS_CLARO3,
                                              border_width=1,
                                              corner_radius=10)
        historial_transacciones.pack(fill = 'x', anchor = 'n', pady = (0,8))

        historial_transacciones.rowconfigure(0, weight=0)
        historial_transacciones.rowconfigure(1, weight=1)
        historial_transacciones.rowconfigure(0, weight=0)
        historial_transacciones.columnconfigure(0, weight=1)

        ctk.CTkLabel(master=historial_transacciones, text='Últimas Transacciones', text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')).grid(row = 0, column = 0, sticky = 'w', padx = 15, pady = (10,8))

        self.contenedor_tabla2 = ctk.CTkFrame(historial_transacciones, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla2.grid(row = 1, column = 0, sticky = 'nsew', padx = 12, pady = (0,8))

        #historial de transacciones
        self.tabla_trans([ENCABEZADO_TRANS_INVENT] + [t for t in TRANS_INVENTARIO()])

        frame_btn = ctk.CTkFrame(historial_transacciones, fg_color='transparent')
        frame_btn.grid(row = 2, column = 0, sticky = 'ew', padx=12, pady=(0,8))

        btn_detalle = Boton (master=frame_btn,
                           texto = 'Ver detalle', 
                           fill=None, 
                           padx=(12,6),
                           metodo= lambda: self.modal_inventario(tipo='detalle_trans')
                           )
        btn_detalle.pack_configure(side = 'right')

    def seleccion_inv(self, fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w, _ in self.celdas_inv[fila]]
        self.selec = valores
        print(self.selec)

        if hasattr(self, "celdas_trans"):
          for f, fila_widgets in enumerate(self.celdas_trans):
              for w, es_badge in fila_widgets:
                  default_bg = 'transparent' if f % 2 == 0 else GRIS_CLARO4
                  w.configure(fg_color=default_bg, text_color=OSCURO)

        #resaltado
        for f, fila_widgets in enumerate(self.celdas_inv):
            for w, es_badge in fila_widgets:
                if es_badge:
                    continue
    
                if f == fila:
                    w.configure(fg_color = AZUL_CLARO)
                else:
                    if f == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    elif f % 2 == 0:
                        default_bg = 'transparent'
                        default_text = OSCURO
                    else:
                        default_bg = GRIS_CLARO4
                        default_text = OSCURO

                    w.configure(fg_color=default_bg, text_color=default_text)

    def tabla_inventario(self, data): 
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

        #resaltado segun estado
        colores = {
                    'OK': VERDE1, 
                    'Bajo': MAMEY,
                    'Agotado': ROJO,
                  }

        self.celdas_inv = []
        for f, fila in enumerate(data):
            fila_widgets = []
            for c, texto in enumerate(fila):
                  #coloreado de las lineas
                  if f == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                  elif f % 2 == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, 12)
                  else:
                    bg = GRIS_CLARO4
                    fg = OSCURO
                    font = (FUENTE, 12)

                  #resaltado de estado con "pilas"
                  if texto in colores:
                      cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                      cont_pila.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                      pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height = 28)
                      pila.pack(fill = 'y')

                      lbl = ctk.CTkLabel(master=pila, text=texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                      lbl.pack(expand = True, padx = 8, pady = 2)

                      if f > 0:
                        lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_inv(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_inv(fila))
                    widget_celda = (lbl, False)
                  
                  frame.grid_columnconfigure(c, weight=1)

                  #borde encabezado
                  if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column = c, sticky = 'ew')
                    borde.grid_propagate(False)
                    borde.configure(height = 2)

                  #bind capturando fila
                  fila_widgets.append(widget_celda)
            self.celdas_inv.append(fila_widgets) 

    def seleccion_trans(self,fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w, _ in self.celdas_trans[fila]]
        self.selec = valores
        print(self.selec)

        if hasattr(self, "celdas_inv"):
          for f, fila_widgets in enumerate(self.celdas_inv):
              for w, es_badge in fila_widgets:
                  if es_badge:
                      continue
                  default_bg = 'transparent' if f % 2 == 0 else GRIS_CLARO4
                  w.configure(fg_color=default_bg, text_color=OSCURO)

        #resaltado
        for f, fila_widgets in enumerate(self.celdas_trans):
             for w, es_badge in fila_widgets:
              if f == fila:
                  w.configure(fg_color=AZUL_CLARO)
              else:
                  default_bg = 'transparent' if f % 2 == 0 else GRIS_CLARO4
                  w.configure(fg_color=default_bg, text_color=OSCURO)

    def tabla_trans(self, data): 
        for w in self.contenedor_tabla2.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla2, fg_color='transparent')
        frame.pack(fill = 'both', expand = True,padx = 12, pady = 12)
        frame.configure(height = 200)
        frame.pack_propagate(False)

        self.celdas_trans = []
        for f, fila in enumerate(data):
            fila_widgets = []
            for c, texto in enumerate(fila):
                  #coloreado de las lineas
                  if f == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                  elif f % 2 == 0:
                    bg = 'transparent'
                    fg = OSCURO
                    font = (FUENTE, 12)
                  else:
                    bg = GRIS_CLARO4
                    fg = OSCURO
                    font = (FUENTE, 12)
                
                  lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                  lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)
                  
                  frame.grid_columnconfigure(c, weight=1)

                  #borde encabezado
                  if f == 0:
                    borde = ctk.CTkFrame(master=frame, fg_color=GRIS)
                    borde.grid(row=f*2+1, column = c, sticky = 'ew')
                    borde.grid_propagate(False)
                    borde.configure(height = 2)

                  #bind capturando fila
                  if f > 0:
                    lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_trans(fila))
                  fila_widgets.append((lbl, False))
            self.celdas_trans.append(fila_widgets)

    def buscar_articulo(self):
        busqueda = self.busqueda_var.get().strip()
        if not busqueda:
          self.tabla_inventario([ENCABEZADOS_INVENTARIO] + [a for a in INVENTARIO()])

        resultado = basedatos.buscar_articulo(texto=busqueda)
        data = [ENCABEZADOS_INVENTARIO] + resultado
        self.tabla_inventario(data=data)

    def limpiar_busqueda_art(self):
        self.busqueda_var.set('')
        self.tabla_inventario([ENCABEZADOS_INVENTARIO] + [a for a in INVENTARIO()])

    def modal_inventario(self, tipo):
            if tipo == 'editar' and len(self.selec) != 7:
                messagebox.showwarning("Advertencia", "Por favor seleccione un artículo para editar")
                return
            
            if tipo == 'detalle_trans' and len(self.selec) != 6:
                messagebox.showerror("Error", "Debe seleccionar una transacción")
                return

            titulo_ventana = ""
            titulo_modal = ""
            match tipo:
                case "agregar":
                    titulo_ventana = "Agregar Nuevo Artículo"
                    titulo_modal = titulo_ventana
                case 'editar':
                    titulo_ventana = "Editar Artículo"
                    titulo_modal = titulo_ventana
                case 'detalle_trans':
                    titulo_ventana = "Ver detalles de Transacción"
                    titulo_modal = "Detalles de la transacción"

            dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
            dialogo.title(titulo_ventana)
            dialogo.geometry("720x380")
            dialogo.resizable(False,False)
            dialogo.transient(self)
            dialogo.grab_set()
            
            #titulo
            ctk.CTkLabel(dialogo, 
                        text= titulo_modal, 
                        text_color=OSCURO, 
                        font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                        ).pack(anchor = 'w', pady = (16,0), padx = 16)
            
            ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

            match tipo:
                case "agregar":
                    self.formulario_articulo(master = dialogo, tipo='agregar')
                case "editar":
                    self.formulario_articulo(master=dialogo, tipo='editar')
                case 'detalle_trans':
                    self.ver_detalle_transaccion(master = dialogo)
    
    def formulario_articulo(self, master, tipo):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        descripcion = ctk.StringVar()
        stock_actual = ctk.IntVar(value=0)
        stock_minimo = ctk.IntVar()
        unidad = ctk.StringVar()
        precio_unitario = ctk.DoubleVar(value=0.00)
        notas = ctk.StringVar()
        id = None

        if tipo == 'editar':
            descripcion.set(self.selec[1])
            stock_actual.set(self.selec[2])
            stock_minimo.set(basedatos.stock_minimo(self.selec[0]))
            unidad.set(self.selec[3])
            precio_unitario.set(self.selec[4])
            notas.set(self.selec[6])
            id = self.selec[0]


        # letrero de campos obligatorios
        obligatorio = ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios")
        obligatorio.place(relx = 0.95, rely = 0.95, anchor = 'se')

        #descripcion
        ctk.CTkLabel(master=frame_formulario,
                     text='Descripción*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=descripcion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS,
                     state='disabled' if tipo == 'editar' else 'normal'
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)
        
        #stock actual
        ctk.CTkLabel(master=frame_formulario,
                     text='Stock Actual*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=stock_actual,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 3, sticky = 'nsew', pady = 12)
        
        #stock minimo
        ctk.CTkLabel(master=frame_formulario,
                     text='Stock Mínimo*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=stock_minimo,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 1, sticky = 'nsew', pady = 12)
        
        #unidad
        ctk.CTkLabel(master=frame_formulario,
                     text='Unidad de medida*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=unidad,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 3, sticky = 'nsew', pady = 12)
        
        #precio
        ctk.CTkLabel(master=frame_formulario,
                     text='Precio Unitario*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=precio_unitario,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 2, column = 1, sticky = 'nsew', pady = 12)
        
        #notas
        ctk.CTkLabel(master=frame_formulario,
                     text='Notas',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 2, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=notas,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 2, column = 3, sticky = 'nsew', pady = 12)
        
        def guardar():
            datos = [
                descripcion.get().strip(),
                stock_actual.get(),
                stock_minimo.get(),
                unidad.get().strip(),
                precio_unitario.get(),
                notas.get().strip(),
            ]

            if not datos[0] or not datos[1] or not datos[2] or not datos[3] or not datos[4]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje = basedatos.guardar_articulo(data=datos, tipo=tipo, id = id)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return
            
            messagebox.showinfo("Éxito", mensaje)
            master.destroy()
            self.tabla_inventario([ENCABEZADOS_INVENTARIO] + [a for a in INVENTARIO()])

        #boton cancelar
        ctk.CTkButton(master = frame_formulario,
                      text='Cancelar',
                      fg_color=PRIMARIO,
                      hover_color=ROJO,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=master.destroy,
                        ).grid(row = 6, column = 1, pady = 12)
        
        #boton guardar
        ctk.CTkButton(master = frame_formulario,
                      text='Guardar',
                      fg_color=VERDE1,
                      hover_color=VERDE2,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=guardar,
                        ).grid(row = 6, column = 2, pady = 12)

    def ver_detalle_transaccion(self, master):

        transaccion = list(basedatos.ver_transaccion(self.selec[0]))
        transaccion[1] = self.selec[1]
        transaccion.insert(4, self.selec[4]) 
        #fecha vendria siendo 5, area 6, y motivo 7

        descripcion = ['ID de Transacción', 'Descripción del Artículo', 'Tipo de Transacción', 'Cantidad', 'Unidad de Medida', 'Fecha y Hora', 'Área', 'Motivo']

        contenedor = ctk.CTkFrame(master=master, fg_color=GRIS_CLARO4)
        contenedor.pack(fill = 'both', expand = True, padx = 16, pady = (0,10))
        
        contenedor.columnconfigure(index=(0,1,2,3), weight = 1, uniform= 'k')

        for i, (desc, valor) in enumerate(zip(descripcion, transaccion)):
            if i == len(descripcion) - 1:
                fila = (i // 2) + 1  # Nueva fila al final
                label_desc = ctk.CTkLabel(contenedor, text=desc + ": ", text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'))
                label_val = ctk.CTkLabel(contenedor, text=str(valor), text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT))
                label_desc.grid(row=fila, column=0, padx=(8,2), pady=4, sticky="e")
                label_val.grid(row=fila, column=1, columnspan=3, padx=(2,8), pady=4, sticky="w")
            else:
                fila = i // 2
                columna = (i % 2) * 2  # Multiplica por 2 porque cada valor ocupa dos columnas (label y valor)
                label_desc = ctk.CTkLabel(contenedor, text=desc + ": ", text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'))
                label_val = ctk.CTkLabel(contenedor, text=str(valor), text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT))
                label_desc.grid(row=fila, column=columna, padx=(8,2), pady=4, sticky="e")
                label_val.grid(row=fila, column=columna+1, padx=(2,8), pady=4, sticky="w")

        