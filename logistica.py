import customtkinter as ctk
from settings import *
from func_clases import *
from tkinter import messagebox

class GestorLogistica(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both', expand = True)

        #variables
        self.selec = None

        #pestañas
        self.contenedor_pestanas = ctk.CTkFrame(master=self, fg_color='transparent')
        self.contenedor_pestanas.pack(anchor = 'n',fill = 'x', pady = (0,10))
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
                          command= "",
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

    def housekeeping(self):
        for w in self.logistica.winfo_children():
             w.destroy()
        self.btn_housekeeping.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO) 
        self.btn_mantenimiento.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_inventario.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_personal.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
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
        
        ctk.CTkLabel(master=frame_asignar, text="📋 Asignar Limpieza", font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'), text_color=OSCURO).pack(anchor = 'w', padx = 15, pady = (15,12))
        
        frame_entrys = ctk.CTkFrame(master=frame_asignar, fg_color='transparent')
        frame_entrys.pack(fill = 'x', anchor = 'n', padx = 15, pady = (0,12))

        #habitacion
        ctk.CTkLabel(master=frame_entrys, text="Habitación:", font=(FUENTE, TAMANO_TEXTO_DEFAULT), text_color=OSCURO).pack(side = 'left', anchor = 'w', padx = (0,15))
        hab_sucias = basedatos.obtener_hab_sucias() if basedatos.obtener_hab_sucias() else ['No hay habitaciones sucias']

        ctk.CTkComboBox(master=frame_entrys,
                        values = hab_sucias,
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
        emp_hk = basedatos.obtener_personal_housekeeping() 
        ctk.CTkComboBox(master=frame_entrys,
                        values = emp_hk,
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
        btn_asignar = Boton(master=frame_entrys,texto='🔄 Asignar Limpieza') #TODO: definir método

        frame_plan = ctk.CTkFrame(master=self.logistica, 
                                     fg_color='transparent',
                                     border_color=GRIS_CLARO3,
                                     border_width=1,
                                     corner_radius=12
                                     )
        frame_plan.pack(fill = 'x', anchor = 'n', pady = 10)

        ctk.CTkLabel(master=frame_plan, text="📊 Plan de Limpieza del Día", font=(FUENTE, TAMANO_TEXTO_DEFAULT, 'bold'), text_color=OSCURO).pack(anchor = 'w', padx = 15, pady = (15,12))

        #contenedor de tabla del plan de housekeeping
        self.contenedor_tabla = ctk.CTkFrame(frame_plan, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla.pack(fill='both', expand=True, padx = 12, pady = 12)

        #plan de housekeeping
        self.plan_housekeeping(data=[ENCABEZADOS_HOUSEKEEPING] + [p for p in PLAN_HOUSEKEEPING()])

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
                           )
    
    def plan_housekeeping(self, data): 
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

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
                        lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_housekeeping(fila))

                      widget_celda = (lbl, True)
                  else:
                    lbl = ctk.CTkLabel(frame, text=texto, anchor='center', width = 140, height = 28, fg_color=bg, text_color=fg, font=font)
                    lbl.grid(row = f*2, column = c, sticky = 'nsew', padx = 1, pady = 1)

                    if f > 0:
                      lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_housekeeping(fila))
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

    def seleccion_housekeeping(self, fila):
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