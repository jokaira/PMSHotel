import customtkinter as ctk
from settings import *
from func_clases import *
from tkinter import messagebox

class GestorLogistica(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #variables
        self.selec = []
        self.hab_sucia = ctk.StringVar()
        self.personal_housekeeping = ctk.StringVar()
        self.busqueda_var = ctk.StringVar()
        self.filtro_estado = ctk.StringVar(value='Activo')

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
                          command= self.mantenimiento,
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
                          command= self.personal,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_personal.pack(side ='left', padx = 5)

    def housekeeping(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_housekeeping.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)

        self.selec = []
        
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

    def inventario(self): 
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_inventario.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_housekeeping.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)
        self.selec = []

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
                            fill=None,
                            metodo= lambda: self.modal_inventario('hacer_trans')
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
        # historial_transacciones.rowconfigure(0, weight=0)
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
            
            if tipo == 'hacer_trans' and len(self.selec) != 7:
                messagebox.showwarning("Advertencia", "Por favor seleccione un artículo para realizar la transacción")
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
                case 'hacer_trans':
                    titulo_ventana = "Hacer Transacción"
                    titulo_modal = "Realizar Transacción de Inventario"

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
                case 'hacer_trans':
                    self.realizar_transaccion(master=dialogo)
    
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
                     text_color=MUTE if tipo == 'editar' else OSCURO,
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
                     text_color=MUTE if tipo == 'editar' else OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS,
                     state='disabled' if tipo == 'editar' else 'normal'
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
        transaccion[6] = basedatos.ver_area(transaccion[6])

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

    def realizar_transaccion(self, master): 
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        id_articulo = self.selec[0]
        nombre_articulo = self.selec[1]
        tipo_trans = ctk.StringVar(value='Entrada')
        cantidad = ctk.IntVar()
        area = ctk.StringVar()
        motivo = ctk.StringVar()

        # letrero de campos obligatorios
        obligatorio = ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios")
        obligatorio.place(relx = 0.95, rely = 0.95, anchor = 'se')

        #detalles del artículo
        ctk.CTkLabel(master=frame_formulario,
                     text='Descripción de artículo',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkLabel(master=frame_formulario,
                     text=nombre_articulo,
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 1, sticky = 'w', pady = 12)
        
        #tipo de transaccion
        ctk.CTkLabel(master=frame_formulario,
                     text='Tipo de Transacción*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', pady = 12)
        ctk.CTkComboBox(master=frame_formulario,
                        variable=tipo_trans,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=['Entrada', 'Salida']
                        ).grid(row=0, column=3, sticky = 'nsew', pady= (0,12))
        
        #cantidad
        ctk.CTkLabel(master=frame_formulario,
                     text=f'Cantidad {self.selec[3]}*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=cantidad,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 1, sticky = 'nsew', pady = 12)
        
        #area
        ctk.CTkLabel(master=frame_formulario,
                     text='Área*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', pady = 12)
        ctk.CTkComboBox(master=frame_formulario,
                        variable=area,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=basedatos.obtener_areas()
                        ).grid(row = 1, column = 3, sticky = 'nsew', pady = 12)
        
        #motivo
        ctk.CTkLabel(master=frame_formulario,
                     text='Motivo*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=motivo,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 2, column = 1, sticky = 'nsew', pady = 12)

        def guardar():
            if cantidad.get() <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            if area.get().strip() is None:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return

            datos = [
                id_articulo,
                tipo_trans.get().strip(),
                cantidad.get(),
                basedatos.ver_id_area(area.get().strip()),
                motivo.get().strip()
            ]

            if not datos[0] or not datos[1] or not datos[2] or not datos[3] or not datos[4]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            #ajustar inventario de acuerdo con la transaccion
            fue_exitoso, mensaje = basedatos.ajustar_inventario(cantidad=datos[2], id=datos[0], tipo=datos[1])
            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return

            #guardar la transacción            
            fue_exitoso1, mensaje1 = basedatos.guardar_transaccion(data=datos)

            if not fue_exitoso1:
                messagebox.showerror("Error", mensaje1)
                return

            messagebox.showinfo("Éxito", mensaje1)
            master.destroy()
            self.tabla_inventario([ENCABEZADOS_INVENTARIO] + [a for a in INVENTARIO()])
            self.tabla_trans([ENCABEZADO_TRANS_INVENT] + [t for t in TRANS_INVENTARIO()])
        
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
        
    def mantenimiento(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_mantenimiento.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_housekeeping.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)
        self.selec = []

        gestion_tickets = ctk.CTkFrame(master=self.logistica,fg_color='transparent')
        gestion_tickets.pack(fill = 'x', anchor = 'n', pady = 8)

        ctk.CTkLabel(master=gestion_tickets, text='Tickets de mantenimiento', text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')).pack(anchor = 'w', padx = 15, pady = (12,8))
        
        self.contenedor_tabla = ctk.CTkFrame(gestion_tickets, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = (0,8))

        #tickets
        self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])

        btn_nuevo = Boton(
            master=gestion_tickets,
            texto="Crear nuevo ticket",
            color=VERDE1,
            hover=VERDE2,
            metodo= lambda: self.modal_mantenimiento("nuevo")
        )

        btn_ver = Boton(
            master=gestion_tickets,
            texto="Ver detalles",
            metodo= lambda: self.modal_mantenimiento("ver")
        )

        btn_asignar = Boton(
            master=gestion_tickets,
            texto="Asignar técnico",
            color=MORADO,
            hover="#A472B7",
            metodo= lambda: self.modal_mantenimiento("asignar")
        )

        btn_descartar = Boton(
            master=gestion_tickets,
            texto="Descartar ticket",
            color=PRIMARIO,
            hover=ROJO,
            metodo= self.descartar_ticket
        )

        btn_en_proceso = Boton(
            master=gestion_tickets,
            texto="Marcar como En Progreso",
            metodo= self.marcar_en_progreso
        )

        btn_completado = Boton(
            master=gestion_tickets,
            texto="Marcar como Completado",
            color=VERDE1,
            hover=VERDE2,
            metodo= self.marcar_completado
        )

    def selec_ticket(self, fila):
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

    def tabla_tickets(self, data):
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

        #resaltado segun estado
        colores = {
                    'Sin asignar': MUTE, 
                    'Asignado': MAMEY,
                    'En Progreso': AZUL,
                    'Completado': VERDE1,
                    'Alta': PRIMARIO,
                    'Media': MAMEY,
                    'Baja': VERDE2,
                    'Descartado': PRIMARIO
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

                  #resaltado de estado con "pilas"
                  if texto in colores:
                      cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                      cont_pila.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                      pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height = 28)
                      pila.pack(fill = 'y')

                      lbl = ctk.CTkLabel(master=pila, text=texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                      lbl.pack(expand = True, padx = 8, pady = 2)
                    
                      if f > 0:
                        lbl.bind("<Button-1>", lambda e, fila=f: self.selec_ticket(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.selec_ticket(fila))
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

    def modal_mantenimiento(self, tipo):
            titulo_ventana = ""
            titulo_modal = ""

            if tipo == 'ver' and len(self.selec) == 0:
                messagebox.showerror("Error", "Debe primero seleccionar un ticket para ver los detalles")
                return
            
            if tipo == 'asignar' and len(self.selec) == 0:
                messagebox.showerror("Error", "Debe primero seleccionar un ticket para asignar un técnico")
                return

            match tipo:
                case "nuevo":
                    titulo_ventana = "Crear nuevo ticket"
                    titulo_modal = titulo_ventana
                case 'descartar':
                    titulo_ventana = "Descartar ticket"
                    titulo_modal = titulo_ventana
                case 'ver':
                    titulo_ventana = "Ver detalles del ticket"
                    titulo_modal = "Detalles del ticket"
                case 'asignar':
                    titulo_ventana = "Asignar técnico de mantenimiento"
                case 'completado':
                    titulo_ventana = "Marcar como Completado"
                    titulo_modal = titulo_ventana

            dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
            dialogo.title(titulo_ventana)
            dialogo.geometry("720x380" if tipo != 'asignar' else '300x200')
            dialogo.resizable(False,False)
            dialogo.transient(self)
            dialogo.grab_set()
            
            #titulo
            if tipo != 'asignar':
                ctk.CTkLabel(dialogo, 
                            text= titulo_modal, 
                            text_color=OSCURO, 
                            font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                            ).pack(anchor = 'w', pady = (16,0), padx = 16)
                
                ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

            match tipo:
                case "nuevo":
                    self.nuevo_ticket(master = dialogo)
                case 'descartar':
                    self.razon_descartar(master=dialogo)
                case 'ver':
                    self.ver_ticket(master=dialogo)
                case 'asignar':
                    self.asignar_tecnico(master = dialogo)
                case 'completado':
                    self.formulario_ticket_completado(master = dialogo)

    def nuevo_ticket(self, master):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        ubicacion = ctk.StringVar()
        descripcion = ctk.StringVar()
        prioridad = ctk.StringVar(value='Media')
        notas = ctk.StringVar()

        # letrero de campos obligatorios
        obligatorio = ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios")
        obligatorio.place(relx = 0.95, rely = 0.95, anchor = 'se')

        tipo_ticket = ""
        es_habitacion = messagebox.askyesno("Tipo de ubicación","¿El problema está en una habitación?")

        if es_habitacion:
            tipo_ticket = 'habitacion'
            habitacion = basedatos.lista_habitaciones()
            ubicacion.set(habitacion[0])
            ctk.CTkLabel(master=frame_formulario,
                        text='Habitación*',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
            ctk.CTkComboBox(master=frame_formulario,
                        variable=ubicacion,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=habitacion
                        ).grid(row=0, column=1, sticky = 'nsew', pady= (0,12))
        else:
            tipo_ticket = 'area_hotel'
            #ubicacion
            ctk.CTkLabel(master=frame_formulario,
                        text='Ubicación*',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
            ctk.CTkEntry(master=frame_formulario,
                     textvariable=ubicacion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)
        
        #descripcion
        ctk.CTkLabel(master=frame_formulario,
                        text='Descripción del ticket*',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 2, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=descripcion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 3, sticky = 'nsew', pady = 12)

        # prioridad
        ctk.CTkLabel(master=frame_formulario,
                        text='Descripción del ticket*',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 1, column = 0, sticky = 'w', pady = 12)
        ctk.CTkComboBox(master=frame_formulario,
                        variable=prioridad,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=['Baja', 'Media', 'Alta']
                        ).grid(row = 1, column = 1, sticky = 'nsew', pady = 12)
        
        #notas
        ctk.CTkLabel(master=frame_formulario,
                        text='Notas',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 1, column = 2, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=notas,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 3, sticky = 'nsew', pady = 12)

        def guardar():
            datos = [
                ubicacion.get().strip(),
                descripcion.get().strip(),
                prioridad.get().strip(),
                notas.get().strip()
            ]

            if not datos[0] or not datos[1] or not datos[2]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje = basedatos.guardar_ticket(data=datos, tipo=tipo_ticket)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return
            
            messagebox.showinfo("Éxito", mensaje)
            master.destroy()
            self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])
        
        #cancelar
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
        
    def razon_descartar(self, master):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        descripcion = ctk.StringVar()

        # letrero de campos obligatorios
        obligatorio = ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios")
        obligatorio.place(relx = 0.95, rely = 0.95, anchor = 'se')

        #descripcion
        ctk.CTkLabel(master=frame_formulario,
                        text='Razon del descarte*',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=descripcion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 0, columnspan = 4, sticky = 'nsew', pady = 12)

        
        def guardar():
            razon = f"Descartado: {descripcion.get().strip()}"
            id_ticket = self.selec[0]

            if not razon or not id_ticket:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje = basedatos.descartar_ticket(razon=razon, id=id_ticket)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return
            
            messagebox.showinfo("Éxito", "El ticket ha sido descartado exitosamente")
            master.destroy()
            self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])
        
        #cancelar
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

    def descartar_ticket(self):
        if len(self.selec) == 0:
            messagebox.showerror("Error", "Debe de seleccionar un ticket")
            return
        
        if self.selec[3] == "DESCARTADO":
            messagebox.showerror("Error", "Este ticket ya fue descartado")
            return
        
        confirmacion = messagebox.askyesno("Advertencia", "¿Está seguro que desea descartar este ticket?")

        if confirmacion:
            self.modal_mantenimiento('descartar')

    def ver_ticket(self, master):
        ticket = list(basedatos.ver_detalle_ticket(self.selec[0]))

        ticket[1] = self.selec[1]
        ticket.pop(2)
        ticket[5] = self.selec[5]
        ticket.pop(8)

        descripcion = ['ID del Ticket', 'Ubicación', 'Descripción', 'Estado', 'Prioridad', 'Técnico asignado', 'Fecha de creación', 'Fecha de asignación', 'Fecha de Cierre', 'Solución', 'Notas adicionales']

        contenedor = ctk.CTkFrame(master=master, fg_color=GRIS_CLARO4)
        contenedor.pack(fill = 'both', expand = True, padx = 16, pady = (0,10))
        
        contenedor.columnconfigure(index=(0,1,2,3), weight = 1, uniform= 'k')

        fila = 0
        lado_izq = True
        
        for desc, valor in zip(descripcion, ticket):
            texto_valor = str(valor) if valor is not None else "No especificado"

            # Campos que deben ocupar una fila completa
            if desc in ['Descripción', 'Solución', 'Notas adicionales']:
                label_desc = ctk.CTkLabel(
                    contenedor, text=desc + ": ", text_color=OSCURO,
                    font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                )
                label_val = ctk.CTkLabel(
                    contenedor, text=texto_valor, text_color=OSCURO,
                    font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                    wraplength=600, justify="left"
                )
                label_desc.grid(row=fila, column=0, padx=(8, 2), pady=4, sticky="ne")
                label_val.grid(row=fila, column=1, columnspan=3, padx=(2, 8), pady=4, sticky="w")

                # Avanzar una fila y reiniciar el lado
                fila += 1
                lado_izq = True
                continue

            # Campos normales (dos por fila)
            if lado_izq:
                col_desc, col_val = 0, 1
            else:
                col_desc, col_val = 2, 3

            label_desc = ctk.CTkLabel(
                contenedor, text=desc + ": ", text_color=OSCURO,
                font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
            )
            label_val = ctk.CTkLabel(
                contenedor, text=texto_valor, text_color=OSCURO,
                font=(FUENTE, TAMANO_TEXTO_DEFAULT)
            )
            label_desc.grid(row=fila, column=col_desc, padx=(8, 2), pady=4, sticky="e")
            label_val.grid(row=fila, column=col_val, padx=(2, 8), pady=4, sticky="w")

            # Alternar lado o avanzar fila si ya se llenaron las dos columnas
            if lado_izq:
                lado_izq = False
            else:
                lado_izq = True
                fila += 1

    def asignar_tecnico(self, master):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 10)

        tecnico = ctk.StringVar()
        tecnicos = basedatos.obtener_tecnicos() if basedatos.obtener_tecnicos() else ['No hay técnicos de mantenimiento']

         #descripcion
        ctk.CTkLabel(master=frame_formulario,
                        text='Técnico a asignar',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 0, columnspan = 2,sticky = 'nsew', pady = 12)
        ctk.CTkComboBox(master=frame_formulario,
                        variable=tecnico,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=tecnicos
                        ).grid(row=1, column=0, columnspan = 2,sticky = 'nsew', pady= (0,12))
        
        def guardar():
            if tecnico.get().strip() == 'No hay técnicos de mantenimiento':
                messagebox.showerror('Error','No hay técnicos de mantenimiento activos')
                return

            id_ticket = self.selec[0]
            cod_emp = tecnico.get().strip()[:6]

            data = [
                basedatos.id_empleado(cod_emp),
                id_ticket,
            ]
            
            ticket_asignado, mensaje = basedatos.asignar_ticket(datos=data)
            if not ticket_asignado:
                messagebox.showerror('Error', mensaje)

            messagebox.showinfo("Técnico asignado", "El técnico fue asignado exitosamente")

            #actualizar tabla
            from settings import TICKETS_MANTENIMIENTO
            self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])
            master.destroy()

        #cancelar
        ctk.CTkButton(master = frame_formulario,
                      text='Cancelar',
                      fg_color=PRIMARIO,
                      hover_color=ROJO,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=master.destroy,
                        ).grid(row = 2, column = 1, pady = 12)
        
        #boton guardar
        ctk.CTkButton(master = frame_formulario,
                      text='Guardar',
                      fg_color=VERDE1,
                      hover_color=VERDE2,
                      text_color=BLANCO,
                      font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                      corner_radius=10,
                      command=guardar,
                        ).grid(row = 2, column = 0, pady = 12)
        
    def marcar_en_progreso(self):
        if len(self.selec) == 0:
            messagebox.showerror("Error", "Debe de seleccionar un ticket")
            return
        
        if self.selec[3] == "DESCARTADO":
            messagebox.showerror("Error", "Este ticket ya fue descartado")
            return
        elif self.selec[3] == "SIN ASIGNAR":
            messagebox.showerror("Error", "Este ticket no tiene un técnico asignado")
            return
        elif self.selec[3] == "EN PROGRESO":
            messagebox.showerror("Error", "Este ticket ya fue marcado en progreso")
            return
        elif self.selec[3] == "COMPLETADO":
            messagebox.showerror("Error", "Este ticket ya fue marcado como completado")
            return

        confirmacion = messagebox.askyesno("Advertencia", '¿Está seguro que desea marcar este ticket como "En progreso"?')

        if confirmacion:
           basedatos.estado_ticket("En Progreso", self.selec[0])  

           messagebox.showinfo("Éxito", "El estado ha sido cambiado exitosamente")
           self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])           

    def marcar_completado(self):
        if len(self.selec) == 0:
            messagebox.showerror("Error", "Debe de seleccionar un ticket")
            return
        
        if self.selec[3] == "DESCARTADO":
            messagebox.showerror("Error", "Este ticket ya fue descartado")
            return
        elif self.selec[3] == "SIN ASIGNAR" or self.selec[3] == "ASIGNADO":
            messagebox.showerror("Error", 'Este ticket no ha sido marcado como "En progreso" y no tiene fecha de inicio de trabajo')
            return
        elif self.selec[3] == "COMPLETADO":
            messagebox.showerror("Error", "Este ticket ya fue marcado como completado")
            return

        confirmacion = messagebox.askyesno("Advertencia", '¿Está seguro que desea marcar este ticket como completado?')

        if confirmacion:
            self.modal_mantenimiento('completado')

    def formulario_ticket_completado(self, master):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        solucion = ctk.StringVar()
        notas = ctk.StringVar()

        #solucion
        ctk.CTkLabel(master=frame_formulario,
                        text='Descripción de la solución',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=solucion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 0, columnspan = 4, sticky = 'nsew', pady = 12)
        
        #notas
        ctk.CTkLabel(master=frame_formulario,
                        text='Notas adicionales',
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                        ).grid(row = 2, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=notas,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 0, columnspan = 4, sticky = 'nsew', pady = 12)

        
        def guardar():
            
            fue_exitoso, mensaje = basedatos.estado_ticket(estado='Completado', id=self.selec[0], solucion=solucion.get().strip(), notas=notas.get().strip())

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return
            
            messagebox.showinfo("Éxito", "El ticket ha sido marcado como completado exitosamente")
            master.destroy()
            self.tabla_tickets([ENCABEZADO_TICKETS_MANT] + [t for t in TICKETS_MANTENIMIENTO()])
        
        #cancelar
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
        
    def personal(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_personal.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_housekeeping.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.logistica.configure(border_width = 0)
        self.selec = []

        gestion_personal = ctk.CTkFrame(master=self.logistica,fg_color='transparent')
        gestion_personal.pack(fill = 'x', anchor = 'n', pady = 8)

        ctk.CTkLabel(master=gestion_personal, text='Gestor del Personal', text_color=OSCURO, font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')).pack(anchor = 'w', padx = 15, pady = (12,8))

        self.barra = self.barra_buscar(master=gestion_personal)
        
        self.contenedor_tabla = ctk.CTkFrame(gestion_personal, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = (0,8))

        #personal
        self.tabla_personal([ENCABEZADO_PERSONAL] + [p for p in PERSONAL_ACTIVO()])

        btn_ver = Boton(
            master=gestion_personal,
            texto="Ver detalles",
            metodo= lambda: self.modal_personal("ver")
        )

        btn_editar = Boton(
            master=gestion_personal,
            texto="Editar datos",
            metodo= lambda: self.modal_personal("editar"),
            color=MORADO,
            hover="#A472B7"
        )
        
        btn_desactivar = Boton(
            master=gestion_personal,
            texto="Desactivar empleado",
            metodo= self.inactivar_empleado,
            color=PRIMARIO,
            hover=ROJO
        )

    def tabla_personal(self, data):
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkScrollableFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

        #resaltado segun estado
        colores = {
                    'Activo': VERDE1,
                    'Inactivo': PRIMARIO
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

                  #resaltado de estado con "pilas"
                  if texto in colores:
                      cont_pila = ctk.CTkFrame(master=frame, fg_color=bg, corner_radius=0)
                      cont_pila.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                      pila = ctk.CTkFrame(master=cont_pila, fg_color=colores[texto], corner_radius=15, height = 28)
                      pila.pack(fill = 'y')

                      lbl = ctk.CTkLabel(master=pila, text=texto.upper(), fg_color='transparent', text_color=BLANCO, font=(FUENTE, 11, 'bold'))
                      lbl.pack(expand = True, padx = 8, pady = 2)
                    
                      if f > 0:
                        lbl.bind("<Button-1>", lambda e, fila=f: self.selec_empleado(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.selec_empleado(fila))
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

    def barra_buscar(self, master):
        contenedor = ctk.CTkFrame(master=master, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=62)
        contenedor.pack(fill = 'x')
        contenedor.pack_propagate(False)

        self.busqueda_var.set("")
        self.filtro_estado.set("Activo")

        ctk.CTkLabel(contenedor, 
                     text='🔍 Buscar:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkEntry(contenedor,
                     placeholder_text='Nombre, código o área...',
                     placeholder_text_color=GRIS_CLARO2,
                     corner_radius=8,
                     text_color=OSCURO,
                     textvariable=self.busqueda_var,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_color= GRIS_CLARO2,
                     border_width=1, height=35
                     ).pack(side = 'left', fill = 'x', expand = True, padx = 6)
        
        ctk.CTkLabel(contenedor, 
                     text='Estado:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkComboBox(contenedor,
                        values = ['Activo', 'Inactivo'],
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
                        border_width=1, height=35,
                        variable=self.filtro_estado,
                        ).pack(side = 'left', padx = 6)

        btn_buscar = Boton (master=contenedor,
                           texto = 'Buscar', 
                           fill=None, 
                           metodo= self.buscar,
                           padx=(12,6))

        btn_limpiar = Boton(master=contenedor,
                            texto='Limpiar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None,
                            metodo = self.limpiar_busqueda
                            )

        btn_agregar = Boton(master=contenedor,
                            texto='➕ Agregar',
                            color=VERDE1,
                            hover=VERDE2,
                            fill=None,
                            padx=(6,12),
                            metodo= lambda: self.modal_personal("nuevo")
                            )
        
    def buscar(self):
        busqueda = self.busqueda_var.get()
        filtro_estado = self.filtro_estado.get().strip()
        
        #buscar habitaciones
        resultado = basedatos.buscar_empleado(texto=busqueda, estado=filtro_estado)
        data = [ENCABEZADO_PERSONAL] + resultado
        self.tabla_personal(data = data)

    def limpiar_busqueda(self):
        self.busqueda_var.set('')
        self.filtro_estado.set('Activo')
        self.tabla_personal([ENCABEZADO_PERSONAL] + [p for p in PERSONAL_ACTIVO()])

    def selec_empleado(self, fila):
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

    def modal_personal(self, tipo):
            titulo_ventana = ""
            titulo_modal = ""

            if tipo == 'ver' and len(self.selec) == 0:
                messagebox.showerror("Error", "Debe primero seleccionar un empleado para ver los detalles")
                return
            elif tipo == 'editar' and len(self.selec) == 0:
                messagebox.showerror("Error", "Debe primero seleccionar un empleado para editar sus datos")
                return

            match tipo:
                case "nuevo":
                    titulo_ventana = "Agregar nuevo empleado"
                    titulo_modal = titulo_ventana
                case 'ver':
                    titulo_ventana = "Ver detalles del empleado"
                    titulo_modal = "Detalles del empleado"
                case 'editar':
                    titulo_ventana = "Editar datos del empleado"
                    titulo_modal = titulo_ventana

            dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
            dialogo.title(titulo_modal)
            dialogo.geometry("720x380")
            dialogo.resizable(False,False)
            dialogo.transient(self)
            dialogo.grab_set()
            
            match tipo:
                case "nuevo":
                    self.ajuste_empleado(master = dialogo, tipo = "agregar")
                case 'ver':
                    self.ver_empleado(master=dialogo)
                case 'editar':
                    self.ajuste_empleado(master = dialogo, tipo= "editar")

    def ajuste_empleado(self, master, tipo):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        #variables de los campos
        codigo = ctk.StringVar() 
        nombres = ctk.StringVar()
        apellidos = ctk.StringVar()
        puesto = ctk.StringVar()
        area = ctk.StringVar() #lista desplegable
        salario_hora = ctk.DoubleVar()
        telefono = ctk.StringVar()
        email = ctk.StringVar()
        
        #modo agregar
        if tipo == "agregar":
            nuevo_codigo = basedatos.generar_codigo_empleado()
            if nuevo_codigo:
                codigo.set(nuevo_codigo)
        #modo editar
        elif tipo == "editar":
            empleado = list(basedatos.ver_detalle_empleado(self.selec[0]))
            empleado[5] = self.selec[4]

            codigo.set(empleado[1])
            nombres.set(empleado[2])
            apellidos.set(empleado[3])
            puesto.set(empleado[4])
            area.set(empleado[5])
            salario_hora.set(empleado[6])
            telefono.set(empleado[10])
            email.set(empleado[11])

        #letrero de campos obligatorios
        ctk.CTkLabel(master=frame_formulario, text="*Todos los campos son obligatorios").place(relx = 0.95, rely = 0.95, anchor = 'se')

        #codigo
        ctk.CTkLabel(master=frame_formulario,
                     text='Código',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=codigo,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS,
                     state= "disabled"
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)
        
        #nombres
        ctk.CTkLabel(master=frame_formulario,
                     text='Nombres',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', padx= (12,0), pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=nombres,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 3, sticky = 'nsew', pady = 12)
        
        #apellidos
        ctk.CTkLabel(master=frame_formulario,
                     text='Apellidos',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=apellidos,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row=1, column=1, sticky = 'nsew', pady= (0,12))
        
        #puesto
        ctk.CTkLabel(master=frame_formulario,
                     text='Puesto',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', padx= (12,0), pady = (0,12))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=puesto,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 3, sticky = 'nsew', pady = (0,12))
        
        #area
        ctk.CTkLabel(master=frame_formulario,
                     text='Área',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w',  pady = (0,12))
        ctk.CTkComboBox(master=frame_formulario,
                        variable=area,
                        text_color=OSCURO,
                        font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        button_color=GRIS_CLARO,
                        button_hover_color=GRIS,
                        dropdown_fg_color=CLARO,
                        dropdown_hover_color=GRIS_CLARO,
                        dropdown_text_color=OSCURO,
                        dropdown_font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                        border_color=GRIS,
                        border_width=1,
                        values=basedatos.obtener_areas()
                        ).grid(row = 2, column = 1, sticky = 'nsew', pady = (0,12))

        #salario
        ctk.CTkLabel(master=frame_formulario,
                     text='Salario/Hora',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 2, sticky = 'w', pady = (0,12), padx= (12,0))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=salario_hora,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row=2, column=3, sticky = 'nsew', pady= (0,12))
        
        #Telefono
        ctk.CTkLabel(master=frame_formulario,
                     text='Teléfono',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 3, column = 0, sticky = 'w', pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=telefono,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 1, sticky = 'nsew', pady = (12,6))
        
        #email
        ctk.CTkLabel(master=frame_formulario,
                     text='E-mail',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 3, column = 2, sticky = 'w', padx= (12,0), pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=email,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 3, sticky = 'nsew', pady = (12,6))

        
        def guardar():
            #datos a guardar en formulario

            datos = [
                codigo.get().strip(), 
                nombres.get().strip(),
                apellidos.get().strip(),
                puesto.get().strip(),
                basedatos.ver_id_area(area.get().strip()),
                salario_hora.get(),
                telefono.get().strip(),
                email.get().strip(),
            ]

            if any(elem is None for elem in datos):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje = basedatos.guardar_empleado(tipo = tipo, datos = datos)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje)
                return
            messagebox.showinfo("Éxito", mensaje)
            master.destroy()
            self.tabla_personal([ENCABEZADO_PERSONAL] + [p for p in PERSONAL_ACTIVO()])

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

    def ver_empleado(self, master):
        empleado = list(basedatos.ver_detalle_empleado(self.selec[0]))

        empleado[5] = self.selec[4]
        empleado.pop(0)

        descripcion = ['Código', 'Nombres', 'Apellidos', 'Puesto', 'Área', 'Salario/Hora ($)', 'Estado', 'Fecha de Ingreso', 'Fecha de Salida', 'Teléfono', 'Correo']

        contenedor = ctk.CTkFrame(master=master, fg_color=GRIS_CLARO4)
        contenedor.pack(fill = 'both', expand = True, padx = 16, pady = (0,10))
        
        contenedor.columnconfigure(index=(0,1,2,3), weight = 1, uniform= 'k')

        fila = 0
        lado_izq = True
        
        for desc, valor in zip(descripcion, empleado):
            texto_valor = str(valor) if valor is not None else "No aplica"

            # Campos que deben ocupar una fila completa
            if desc in ['Descripción', 'Solución', 'Notas adicionales']:
                label_desc = ctk.CTkLabel(
                    contenedor, text=desc + ": ", text_color=OSCURO,
                    font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                )
                label_val = ctk.CTkLabel(
                    contenedor, text=texto_valor, text_color=OSCURO,
                    font=(FUENTE, TAMANO_TEXTO_DEFAULT),
                    wraplength=600, justify="left"
                )
                label_desc.grid(row=fila, column=0, padx=(8, 2), pady=4, sticky="ne")
                label_val.grid(row=fila, column=1, columnspan=3, padx=(2, 8), pady=4, sticky="w")

                # Avanzar una fila y reiniciar el lado
                fila += 1
                lado_izq = True
                continue

            # Campos normales (dos por fila)
            if lado_izq:
                col_desc, col_val = 0, 1
            else:
                col_desc, col_val = 2, 3

            label_desc = ctk.CTkLabel(
                contenedor, text=desc + ": ", text_color=OSCURO,
                font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
            )
            label_val = ctk.CTkLabel(
                contenedor, text=texto_valor, text_color=OSCURO,
                font=(FUENTE, TAMANO_TEXTO_DEFAULT)
            )
            label_desc.grid(row=fila, column=col_desc, padx=(8, 2), pady=4, sticky="e")
            label_val.grid(row=fila, column=col_val, padx=(2, 8), pady=4, sticky="w")

            # Alternar lado o avanzar fila si ya se llenaron las dos columnas
            if lado_izq:
                lado_izq = False
            else:
                lado_izq = True
                fila += 1

    def inactivar_empleado(self):
        if self.selec is None or self.selec[5] == 'INACTIVO':
            messagebox.showerror('Error','Debe seleccionar un empleado activo')
            return
        
        confirmacion = messagebox.askyesno("Advertencia", "Este empleado no podrá ser activado nuevamente. ¿Está seguro que desea desactivar a este empleado?")
        if confirmacion:
            exito, mensaje = basedatos.inactivar_empleado(self.selec[0])
            if not exito:
                messagebox.showerror('Error', mensaje)

            messagebox.showinfo("Desactivación exitosa", "El empleado ha sido desactivado exitosamente")

            #actualizar tabla
            self.tabla_personal([ENCABEZADO_PERSONAL] + [p for p in PERSONAL_ACTIVO()])