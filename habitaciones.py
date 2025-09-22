import customtkinter as ctk
from settings import *
from func_clases import *
import basedatos
from tkinter import messagebox

class GestorHabitaciones(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, fg_color='transparent')
        self.pack(fill = 'both')

        #datos
        self.hab_actual = None
        self.tipo_actual = None
        self.busqueda_var = ctk.StringVar()
        self.filtro_estado = ctk.StringVar(value='Todos')

        #pestañas
        self.contenedor_pestanas = ctk.CTkFrame(master=self, fg_color='transparent')
        self.contenedor_pestanas.pack(anchor = 'n',fill = 'x', expand = True, pady = (0,10))
        self.boton_pestanas(master=self.contenedor_pestanas)

        self.habitaciones = ctk.CTkFrame(master=master, fg_color='transparent')
        self.habitaciones.pack(anchor = 'n',fill = 'x')

        #gestionar habitaciones
        self.gestionar_habitaciones()

    def boton_pestanas(self, master):
            self.btn_gest = ctk.CTkButton(master=master, 
                          text= '🏠 Gestionar Habitaciones',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.gestionar_habitaciones,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_gest.pack(side ='left')

            self.btn_tipos = ctk.CTkButton(master=master, 
                          text= '📋 Tipos de Habitación',
                          fg_color=GRIS_CLARO,
                          hover_color=GRIS,
                          command= self.tipos_habitaciones,
                          text_color=OSCURO,
                          font = (FUENTE,TAMANO_TEXTO_DEFAULT), 
                          height=44,
                          corner_radius=10
                          )
            self.btn_tipos.pack(side ='left', padx = 10)

    #metodos de la primera pestaña
    def gestionar_habitaciones(self):
        for widget in self.habitaciones.winfo_children():
            widget.destroy()

        self.barra = self.barra_buscar()
        self.contenedor_tabla2 = ctk.CTkFrame(self.habitaciones, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=10)
        self.contenedor_tabla2.pack(fill='both', expand=True, padx = 12, pady = 12)

        self.tabla_habitaciones([ENCABEZADOS_HABITACIONES] + [h for h in HABITACIONES()])
        self.btn_gest.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO)
        self.btn_tipos.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)

        self.hab_actual = None
        
    def barra_buscar(self):
        contenedor = ctk.CTkFrame(master=self.habitaciones, fg_color='transparent', border_color=GRIS_CLARO3, border_width=1, corner_radius=12, height=62)
        contenedor.pack(fill = 'x')
        contenedor.pack_propagate(False)

        ctk.CTkLabel(contenedor, 
                     text='🔍 Buscar:',
                     text_color=OSCURO,
                     font=(FUENTE, 13, 'bold')
                     ).pack(side = 'left', padx = 6)
        
        ctk.CTkEntry(contenedor,
                     placeholder_text='Nombre, tipo o ubicación...',
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
                        values = ['Todos', 'Disponible', 'Ocupada', 'Sucia', 'Limpiando', 'Mantenimiento', 'Fuera de Servicio'],
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
                            metodo= lambda: self.modal_habitacion("agregar")
                            )
  
    def tabla_habitaciones(self, data):
        for w in self.contenedor_tabla2.winfo_children():
             w.destroy()

        #resaltado segun estado
        colores = {
                    'Disponible': VERDE1, 
                    'Ocupada': AZUL, 
                    'Sucia': MAMEY, 
                    'Limpiando': MORADO, 
                    'Mantenimiento': ROJO, 
                    'Fuera de servicio': MUTE
                  }

        frame = ctk.CTkFrame(master=self.contenedor_tabla2, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

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


        btn_frame = ctk.CTkFrame(self.contenedor_tabla2, fg_color="transparent")
        btn_frame.pack(fill = 'x', padx = 12, pady = 12)

        btn_editar = Boton(master=btn_frame,
                           texto='Editar',
                           color=MAMEY,
                           hover=MAMEY2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo= lambda: self.modal_habitacion("editar")
                           )

        btn_eliminar = Boton(master=btn_frame,
                           texto='Eliminar',
                           color=ROJO,
                           hover=ROJO2,
                           tamano_texto=12,
                           altura=28,
                           padx=2,
                           pady=2,
                           fill=None,
                           metodo= self.eliminar_habitacion
                           )
        
    def buscar(self):
        busqueda = self.busqueda_var.get().strip()
        filtro_estado = self.filtro_estado.get().strip()
        if not busqueda:
            self.tabla_habitaciones([ENCABEZADOS_HABITACIONES] + [h for h in HABITACIONES()])
            return
        
        #buscar habitaciones
        resultado = basedatos.buscar_habitacion(busqueda, estado=filtro_estado)
        data = [ENCABEZADOS_HABITACIONES] + resultado
        self.tabla_habitaciones(data = data)
    
    def limpiar_busqueda(self):
        self.busqueda_var.set('')
        self.filtro_estado.set('Todos')
        self.tabla_habitaciones([ENCABEZADOS_HABITACIONES] + [h for h in HABITACIONES()])

    def seleccion(self, fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w, _ in self.celdas[fila]]
        self.hab_actual = valores
        print(self.hab_actual)

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

    def modal_habitacion (self, tipo):
        if tipo == "editar" and not self.hab_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione una habitación para editar")
            return

        dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
        dialogo.title("Agregar Nueva Habitación" if tipo == "agregar" else "Editar Habitación")
        dialogo.geometry("720x380")
        dialogo.resizable(False,False)
        dialogo.transient(self)
        dialogo.grab_set()
        
        #titulo
        ctk.CTkLabel(dialogo, 
                     text= "➕ Nueva Habitación" if tipo == "agregar" else "✏️ Editar Habitación", 
                     text_color=OSCURO, 
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', pady = (16,0), padx = 16)
        
        ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

        self.crear_formulario(master=dialogo, tipo= tipo)

    def eliminar_habitacion(self):
        if not self.hab_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione una habitación para eliminar")
            return
        
        confirmacion = messagebox.askyesno("Eliminar habitación", f"¿Está seguro que desea eliminar esta habitación?\n{self.hab_actual[1]} {self.hab_actual[2]} {self.hab_actual[4]}")

        if confirmacion:
            try:
              eliminacion = basedatos.eliminar_habitacion(self.hab_actual[0])
              messagebox.showinfo("Éxito", eliminacion[1])
            except:
              messagebox.showerror("Error", eliminacion[1])
        
        #actualizar tabla
        from settings import HABITACIONES
        self.tabla_habitaciones(data = [ENCABEZADOS_HABITACIONES] + [c for c in HABITACIONES()])

    def crear_formulario(self, master, tipo):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        #variables de los campos
        numero = ctk.StringVar()
        tipo_hab = ctk.StringVar()
        estado = ctk.StringVar(value='Disponible')
        ubicacion = ctk.StringVar()
        notas = ctk.StringVar()
                
        #modo editar
        if tipo == "editar":
            numero.set(self.hab_actual[1])
            tipo_hab.set(self.hab_actual[2])
            estado.set(self.hab_actual[3].capitalize())
            ubicacion.set(self.hab_actual[4])
            notas.set(self.hab_actual[6])

        #letrero de campos obligatorios
        ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios").place(relx = 0.95, rely = 0.95, anchor = 'se')

        #numero
        ctk.CTkLabel(master=frame_formulario,
                     text='Número*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=numero,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)

        #tipo habitacion
        valores = [row[1] for row in basedatos.obtener_tipos_habitaciones()]

        ctk.CTkLabel(master=frame_formulario,
                     text='Tipo*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', pady = (0,12), padx= (12,0))
        ctk.CTkComboBox(master=frame_formulario,
                        variable=tipo_hab,
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
                        state='readonly',
                        values=valores,
                        ).grid(row=0, column=3, sticky = 'nsew', pady= (0,12))
        
        #estado de habitacion
        ctk.CTkLabel(master=frame_formulario,
                     text='Estado*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkComboBox(master=frame_formulario,
                        variable=estado,
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
                        values=['Disponible', 'Ocupada', 'Sucia', 'Limpiando', 'Mantenimiento', 'Fuera de servicio']
                        ).grid(row=1, column=1, sticky = 'nsew', pady= (0,12))
        
        #ubicacion
        ctk.CTkLabel(master=frame_formulario,
                     text='Ubicación*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 2, sticky = 'w', pady = (12,6), padx= (12,0))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=ubicacion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 1, column = 3, sticky = 'nsew', pady = (12,6))
        
        #notas
        ctk.CTkLabel(master=frame_formulario,
                     text='Notas',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=notas,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 2, column = 1, columnspan = 3,sticky = 'nsew', pady = (12,6))
        
        def guardar():
            #datos a guardar en formulario

            datos = [
                numero.get().strip(),
                basedatos.id_tipo_hab(tipo_hab.get().strip())[0], #id del tipo de habitacion
                estado.get().strip(),
                ubicacion.get().strip(),
                basedatos.id_tipo_hab(tipo_hab.get().strip())[1], #capacidad de la habitacion de acuerdo al tipo
                notas.get().strip()
            ]

            if not datos[0] or not datos[1] or not datos[2] or not datos[3]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje4 = basedatos.guardar_habitacion(tipo = tipo, datos = datos)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje4)
                return
            messagebox.showinfo("Éxito", mensaje4)
            master.destroy()
            self.tabla_habitaciones(data=[ENCABEZADOS_HABITACIONES] + [h for h in HABITACIONES()])

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

    #metodos de la segunda pestaña
    def tipos_habitaciones(self):
        for widget in self.habitaciones.winfo_children():
            widget.destroy()

        self.btn_gest.configure(fg_color = GRIS_CLARO, hover_color = GRIS, text_color = OSCURO)
        self.btn_tipos.configure(fg_color = AZUL, hover_color = AZUL,text_color = BLANCO)

        contenedor = ctk.CTkFrame(master=self.habitaciones, fg_color='transparent',border_color='#eee', border_width=1, corner_radius=12)
        contenedor.pack(fill = 'x', expand = True, anchor = 'n')

        ctk.CTkLabel(master = contenedor,
                     text = '📋 Gestión de Tipos de Habitación',
                     text_color=PRIMARIO,
                     font = (FUENTE, TAMANO_1, 'bold')
                     ).pack(anchor = 'w', padx = 15, pady = 15)
        
        self.contenedor_tabla = ctk.CTkFrame(master=contenedor, fg_color='transparent')
        self.contenedor_tabla.pack(fill = 'both', expand = True, padx = 12, pady = 12)

        self.tabla_tipos(data=[ENCABEZADOS_TIPOS_HABITACIONES] + [t for t in TIPOS_HABITACIONES()])
        self.botones_accion()

        self.hab_actual = None
        
    def tabla_tipos(self,data):
        for w in self.contenedor_tabla.winfo_children():
             w.destroy()

        frame = ctk.CTkFrame(master=self.contenedor_tabla, fg_color='transparent')
        frame.pack(fill = 'both', expand = True, padx = 12, pady = 12)

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
                    lbl.bind("<Button-1>", lambda e, fila=f: self.seleccion_tipo(fila))
                  fila_widgets.append(lbl)
            self.celdas.append(fila_widgets)        

    def botones_accion(self):
        contenedor_botones = ctk.CTkFrame(master = self.habitaciones, fg_color='transparent')
        contenedor_botones.pack(fill = 'x')
        btn_editar = Boton (master=contenedor_botones,
                           texto = 'Editar', 
                           fill=None,
                           metodo= lambda: self.modal_tipo("editar"), 
                           padx=(12,6))

        btn_eliminar = Boton(master=contenedor_botones,
                            texto='Eliminar',
                            color=PRIMARIO,
                            hover=ROJO,
                            padx=6,
                            fill=None,
                            metodo=self.eliminar_tipo
                            )

        btn_agregar = Boton(master=contenedor_botones,
                            texto='➕ Agregar',
                            color=VERDE1,
                            hover=VERDE2,
                            fill=None,
                            padx=(6,12),
                            metodo = lambda: self.modal_tipo("agregar")
                            )

    def seleccion_tipo(self, fila):
        if fila == 0:
            return
        valores = [w.cget('text') for w in self.celdas[fila]]
        self.tipo_actual = valores
        print(self.tipo_actual)

        # resaltado
        for f, fila_widgets in enumerate(self.celdas):
             for w in fila_widgets:
                w.configure(fg_color = AZUL_CLARO if f == fila else ('transparent' if f%2 == 0 else GRIS_CLARO4))

    def modal_tipo(self,tipo):
        if tipo == "editar" and not self.tipo_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione una un tipo de habitación para editar")
            return

        dialogo = ctk.CTkToplevel(self, fg_color=CLARO)
        dialogo.title("Agregar Nuevo Tipo" if tipo == "agregar" else "Editar Tipo")
        dialogo.geometry("720x380")
        dialogo.resizable(False,False)
        dialogo.transient(self)
        dialogo.grab_set()
        
        #titulo
        ctk.CTkLabel(dialogo, 
                     text= "➕ Nuevo Tipo de Habitación" if tipo == "agregar" else "✏️ Editar Tipo de Habitación", 
                     text_color=OSCURO, 
                     font = (FUENTE, TAMANO_TEXTO_DEFAULT, 'bold')
                     ).pack(anchor = 'w', pady = (16,0), padx = 16)
        
        ctk.CTkFrame(dialogo, height=2, fg_color=OSCURO).pack(fill = 'x',  padx = 15, pady =10)

        self.crear_formulario_tipo(master=dialogo, tipo= tipo)

    def eliminar_tipo(self):
        if not self.tipo_actual:
            messagebox.showwarning("Advertencia", "Por favor seleccione un tipo de habitación para eliminar")
            return
        
        confirmacion = messagebox.askyesno("Eliminar tipo de habitación", f"¿Está seguro que desea eliminar este tipo de habitación?\n{self.tipo_actual[1]} para {self.tipo_actual[2]} personas")

        if confirmacion:
            try:
              eliminacion = basedatos.eliminar_tipo_habitacion(self.tipo_actual[0])
              messagebox.showinfo("Éxito", eliminacion[1])
            except:
              messagebox.showerror("Error", eliminacion[1])
        
        #actualizar tabla
        from settings import TIPOS_HABITACIONES
        self.tabla_tipos(data=[ENCABEZADOS_TIPOS_HABITACIONES] + [t for t in TIPOS_HABITACIONES()])

    def crear_formulario_tipo(self, master, tipo):
        frame_formulario = ctk.CTkFrame(master = master, fg_color='transparent')
        frame_formulario.pack(fill = 'both', expand = True, padx = 15)

        frame_formulario.columnconfigure(index=(0,1,2,3), weight = 1, uniform='x')

        #variables de los campos
        nombre = ctk.StringVar()
        capacidad = ctk.IntVar()
        precio = ctk.DoubleVar()
        descripcion = ctk.StringVar()
                
        #modo editar
        if tipo == "editar":
            nombre.set(self.tipo_actual[1])
            capacidad.set(int(self.tipo_actual[2]))
            precio.set(float(self.tipo_actual[3]))
            descripcion.set(self.tipo_actual[4])

        #letrero de campos obligatorios
        ctk.CTkLabel(master=frame_formulario, text="*: Campos obligatorios").place(relx = 0.95, rely = 0.95, anchor = 'se')

        #nombre del tipo
        ctk.CTkLabel(master=frame_formulario,
                     text='Nombre del Tipo*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 0, sticky = 'w', pady = 12)
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=nombre,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 0, column = 1, sticky = 'nsew', pady = 12)

        #capacidad
        ctk.CTkLabel(master=frame_formulario,
                     text='Capacidad*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 0, column = 2, sticky = 'w', pady = (0,12), padx= (12,0))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=capacidad,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                    ).grid(row=0, column=3, sticky = 'nsew', pady= (0,12))
        
        #precio pro noche
        ctk.CTkLabel(master=frame_formulario,
                     text='Precio por Noche (RD$)*',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 1, column = 0, sticky = 'w', pady = (0,12))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=precio,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                    ).grid(row=1, column=1, sticky = 'nsew', pady= (0,12))
        
        #descripción
        ctk.CTkLabel(master=frame_formulario,
                     text='Descripción',
                     text_color=OSCURO,
                     font=(FUENTE, TAMANO_TEXTO_DEFAULT)
                     ).grid(row = 2, column = 0, sticky = 'w', pady = (12,6))
        ctk.CTkEntry(master=frame_formulario,
                     textvariable=descripcion,
                     text_color=OSCURO,
                     font= (FUENTE, TAMANO_TEXTO_DEFAULT),
                     border_width=1,
                     border_color=GRIS
                     ).grid(row = 3, column = 0, rowspan = 3, columnspan = 3,sticky = 'nsew', pady = (12,6))
                
        def guardar():
            #datos a guardar en formulario

            datos = [
                nombre.get().strip(),
                capacidad.get(),
                precio.get(),
                descripcion.get().strip(),
            ]

            nombre_viejo = None
            
            if tipo == "editar":
                #valor referencia
                nombre_viejo = self.tipo_actual[1]

            if not datos[0] or not datos[1] or not datos[2] or not datos[3]:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            fue_exitoso, mensaje5 = basedatos.guardar_tipo_habitacion(tipo = tipo, datos = datos, clave= nombre_viejo)

            if not fue_exitoso:
                messagebox.showerror("Error", mensaje5)
                return
            messagebox.showinfo("Éxito", mensaje5)
            master.destroy()

            self.tabla_tipos(data=[ENCABEZADOS_TIPOS_HABITACIONES] + [t for t in TIPOS_HABITACIONES()])

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