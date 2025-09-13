import basedatos

#colores
PRIMARIO = '#C0392B'
OSCURO = '#2C3E50'
CLARO = '#F8F9FA'
MUTE = '#95A5A6'
GRIS = '#B9BDBD'
BLANCO = '#FFFFFF'
VERDE1 = '#27AE60'
VERDE2 = '#2ECC71'
MAMEY = '#F39C12'
MAMEY2 = '#F0B555'
AZUL = '#3498DB'
AZUL2 = '#5DA6D7'
MORADO = '#9B59B6'
ROJO = '#E74C3C'
ROJO2= '#E4766A'
VERDE_CLARO = '#D5F4E6'
ROJO_CLARO = '#FADBD8'
AMARILLO_CLARO = '#FEF9E7'
AZUL_CLARO = '#D6EAF8'
MORADO_CLARO = '#E8D4F2'
GRIS_CLARO = '#D5DBDB'
GRIS_CLARO2 = '#DDDDDD'
GRIS_CLARO3 = '#EEEEEE'
GRIS_CLARO4 = '#ecf0f1'

#botones y encabezados
BTN_HEAD = ['📊 Dashboard', '👥 Gestor de Clientes', '🏠 Gestión de Habitaciones', '📅 Gestor de Reservas' ]

#letras
FUENTE = 'Arial'
TAMANO_TEXTO_DEFAULT = 14
TAMANO_1 = 16
TAMANO_2 = 28
TAMANO_3 = 24

#Dashboard
def KPI_DASHBOARD(): return {
    'clientes': {'titulo': '👥 Personas Alojadas', 
                 'cantidad': basedatos.kpi_alojamiento()[2], 
                 'subtitulo': 'Actualmente en el hotel', 
                 'color': AZUL, 
                 'col': 0},
    'habitaciones': {'titulo': '🏠 Habitaciones', 
                     'cantidad': basedatos.total_habitaciones(), 
                     'subtitulo': 'Inventario', 
                     'color': ROJO, 
                     'col': 1},
    'reservas': {'titulo': '📅 Reservas Activas', 
                 'cantidad': basedatos.reservas_activas(), 
                 'subtitulo': 'Próximas', 
                 'color': VERDE2, 
                 'col': 2},
    'ingresos': {'titulo': '💰 Ingresos del Mes', 
                 'cantidad': f'${basedatos.ingresos_mes()[0]:,.2f}', 
                 'subtitulo': 'registrado', 
                 'color': MAMEY, 
                 'col': 3},
}

#Clientes
def CLIENTES(): return basedatos.obtener_clientes()

ENCABEZADOS_CLIENTES = ["ID", "Nombres", "Apellidos", "Documento", "Nro. Doc","Cumpleaños", "Género", "Nacionalidad", "Teléfono", "E-mail"]

#Habitaciones
def HABITACIONES(): return basedatos.obtener_habitaciones()

ENCABEZADOS_HABITACIONES = ['ID', 'Número', 'Tipo', 'Estado', 'Ubicación', 'Capacidad', 'Notas']

ENCABEZADOS_TIPOS_HABITACIONES = ['ID', 'Tipo', 'Capacidad', 'Precio/Noche',  'Descripción']

def TIPOS_HABITACIONES(): return basedatos.obtener_tipos_habitaciones()

#Reservas
def KPI_RESERVAS(): return {
    'reservas': {'titulo': '📅 Reservas Activas', 
                 'cantidad': basedatos.reservas_activas(), 
                 'subtitulo': 'Próximas', 
                 'color': AZUL, 'col': 0},
    'hab_ocup': {'titulo': '🏠 Habitaciones Ocupadas', 
                 'cantidad': basedatos.kpi_alojamiento()[1], 
                 'subtitulo': 'Hoy', 
                 'color': ROJO, 'col': 1},
    'checkin': {'titulo': '✅ Check-ins Hoy', 
                'cantidad': basedatos.total_checkin(), 
                'subtitulo': 'Pendientes', 
                'color': VERDE2, 'col': 2},
    'ingresos': {'titulo': '💰 Ingresos Reservas', 
                 'cantidad': f'${basedatos.ingresos_reservas():,.2f}', 
                 'subtitulo': 'Este mes', 
                 'color': MAMEY, 'col': 3},
}

ENCABEZADOS_RESERVAS = ['ID', '🏠 Hab.', '👤 Cliente', '📧 Email', '📅 Entrada', '📅 Salida', '👥 Personas Alojadas','💰 Total', '✅ Estado']

def RESERVAS(): return basedatos.obtener_reservas()