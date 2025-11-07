import sqlite3 as sql
from datetime import date, datetime, timedelta

NOMBRE_BASEDATOS = 'base_datos.db'

def conectar_bd():
    try:
        conn = sql.connect(NOMBRE_BASEDATOS, timeout=10)
        conn.row_factory = sql.Row
        return conn
    except sql.Error as e:
        print(f'Error al conectarse a la base de datos: {e}')
        return None

def verificar_tablas():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            cantidad_tablas = len(tablas)
            conn.close()

            if cantidad_tablas == 0:
                print('La base de datos está vacía. Procediendo a crear tablas...')
                crear_tablas()
            elif cantidad_tablas < 16:
                print('La base de datos está incompleta. Procediendo a crear todas las tablas faltantes...')
                crear_tablas()
            else:
                print('Base de datos está completa')

        except sql.Error as e:
            print(f'Error al realizar verificacion de tablas: {e}')
            conn.close()

def crear_tablas():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            #1. tabla de clientes
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                tipo_doc TEXT NOT NULL,
                numero_doc TEXT UNIQUE NOT NULL,
                fecha_nac DATE NOT NULL,
                genero TEXT NOT NULL,
                nacionalidad TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                fecha_registro DATE DEFAULT (date('now')),
                activo BOOLEAN DEFAULT 1
            );
            """)
            conn.commit()
            print('1. Tabla "clientes" creada exitosamente')

            #2. tabla de tipos de habitacion
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_habitacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                capacidad INTEGER NOT NULL,
                precio_base REAL NOT NULL,
                descripcion TEXT
            );
            """)
            conn.commit()
            print('2. Tabla "tipos_habitacion" creada exitosamente')
            
            #3. habitaciones
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                tipo_id INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Disponible',
                ubicacion TEXT NOT NULL,
                capacidad INTEGER NOT NULL,
                notas TEXT,
                fecha_ultima_limpieza DATE,
                fecha_ultimo_mantenimiento DATE,
                FOREIGN KEY (tipo_id) REFERENCES tipos_habitacion(id)
            );
            """)
            conn.commit()
            print('3. Tabla "habitaciones" creada exitosamente')

            #16. ingresos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_ingreso TEXT NOT NULL, -- 'reserva', 'walk_in', 'costo_adicional_checkout', 'evento'
                concepto TEXT NOT NULL, -- Descripción del pago
                monto REAL NOT NULL,
                metodo_pago TEXT NOT NULL, -- 'efectivo', 'tarjeta', 'transferencia', 'cheque'
                fecha_pago DATETIME DEFAULT (datetime('now')),
                numero_transaccion TEXT, -- Número de transacción bancaria
                notas TEXT
            )
            """)
            conn.commit()
            print('16. Tabla "ingresos" creada exitosamente')

            #4. reservas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_hab TEXT NOT NULL,
                tipo_habitacion TEXT NOT NULL,
                id_cliente INTEGER NOT NULL,
                cliente_nombre TEXT NOT NULL,
                cliente_email TEXT NOT NULL,
                fecha_entrada DATE NOT NULL,
                fecha_salida DATE NOT NULL,
                total_personas INTEGER NOT NULL DEFAULT 1,
                id_pago INTEGER NOT NULL,
                monto_pago REAL NOT NULL,
                checked_in BOOLEAN DEFAULT 0,
                checked_out BOOLEAN DEFAULT 0,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                fecha_creacion DATETIME DEFAULT (datetime('now')),
                notas TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                FOREIGN KEY (cliente_email) REFERENCES clientes(email),
                FOREIGN KEY (numero_hab) REFERENCES habitaciones(numero),
                FOREIGN KEY (id_pago) REFERENCES ingresos(id)
            );
            """)
            conn.commit()
            try:
                cursor.execute("ALTER TABLE reservas ADD COLUMN es_walkin INTEGER DEFAULT 0")
            except sql.Error:
                pass
            print('4. Tabla "reservas" creada exitosamente')

            #4.5. areas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            );
            """)
            conn.commit()
            print('4.5. Tabla "areas" creada exitosamente')

            #5. personal
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                puesto TEXT NOT NULL,
                area_id INTEGER NOT NULL,
                salario_hora REAL NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Activo',
                fecha_contratacion DATE NOT NULL,
                fecha_inactivacion DATE,
                telefono TEXT,
                email TEXT,
                FOREIGN KEY (area_id) REFERENCES areas(id)
            );
            """)
            conn.commit()
            print('5. Tabla "personal" creada exitosamente')

            #8. tickets de mantenimiento
            cursor.execute("""
            CREATE TABLE tickets_mantenimiento (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                habitacion         TEXT,
                area_hotel         TEXT,
                descripcion        TEXT NOT NULL,
                estado             TEXT NOT NULL DEFAULT 'Sin asignar',
                prioridad          TEXT NOT NULL DEFAULT 'Media',
                tecnico_id         INTEGER,   -- FK a personal
                fecha_creacion     DATETIME DEFAULT (datetime('now')),
                fecha_asignacion   DATE,
                fecha_inicio       DATE,
                fecha_fin          DATE,
                descripcion_solucion TEXT,
                notas              TEXT,
                
                FOREIGN KEY (habitacion) REFERENCES habitaciones(numero),
                FOREIGN KEY (tecnico_id) REFERENCES personal(id)
            );
            """)
            conn.commit()
            print('8. Tabla "tickets_mantenimiento" creada exitosamente')

            #10. walkins
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS walk_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_hab TEXT NOT NULL,
                cliente_nombre TEXT NOT NULL,
                cliente_email TEXT,
                fecha_entrada DATE NOT NULL,
                fecha_salida DATE NOT NULL,
                total_personas INTEGER NOT NULL DEFAULT 1,
                id_pago INTEGER NOT NULL,
                checked_in BOOLEAN DEFAULT 1,
                checked_out BOOLEAN DEFAULT 0,
                estado TEXT NOT NULL DEFAULT 'En curso',
                notas TEXT,
                FOREIGN KEY (id_pago) REFERENCES ingresos(id)
                FOREIGN KEY (numero_hab) REFERENCES habitaciones(numero)
            );
            """)
            conn.commit()
            print('10. Tabla "walk_ins" creada exitosamente')

            #11. checkins y checkouts
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkins_checkouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reserva_id INTEGER,
                walk_in_id INTEGER,
                tipo TEXT NOT NULL, -- 'checkin' o 'checkout'
                fecha_hora DATETIME DEFAULT (datetime('now')),
                usuario TEXT,
                notas TEXT,
                FOREIGN KEY (reserva_id) REFERENCES reservas(id),
                FOREIGN KEY (walk_in_id) REFERENCES walk_ins(id),
                CHECK ((reserva_id IS NOT NULL AND walk_in_id IS NULL) OR 
                    (reserva_id IS NULL AND walk_in_id IS NOT NULL))
            );
            """)
            conn.commit()
            print('11. Tabla "checkins_checkouts" creada exitosamente')

            #12. buffets
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS buffet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                personas INTEGER NOT NULL,
                menu TEXT NOT NULL,
                precio_por_persona REAL NOT NULL,
                total REAL NOT NULL,
                notas TEXT,
                fecha_creacion DATETIME DEFAULT (datetime('now'))
            );
            """)
            conn.commit()
            print('12. Tabla "buffet" creada exitosamente')

            #13. eventos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                salon TEXT NOT NULL,
                fecha DATE NOT NULL,
                hora TEXT NOT NULL,
                equipamiento TEXT,
                categoria TEXT,
                personas INTEGER NOT NULL,
                tarifa_salon REAL NOT NULL,
                total REAL NOT NULL,
                fecha_creacion DATETIME DEFAULT (datetime('now')),
                notas TEXT,
                mesas_csv TEXT,
                asientos_totales INTEGER DEFAULT 0,
                costo_mesas REAL DEFAULT 0.0
            );
            """)
            conn.commit()
            # Ensure older DBs get new columns (ALTER TABLE will fail silently if column exists)
            try:
                cursor.execute("ALTER TABLE eventos ADD COLUMN mesas_csv TEXT")
            except sql.Error:
                pass
            try:
                cursor.execute("ALTER TABLE eventos ADD COLUMN asientos_totales INTEGER DEFAULT 0")
            except sql.Error:
                pass
            try:
                cursor.execute("ALTER TABLE eventos ADD COLUMN costo_mesas REAL DEFAULT 0.0")
            except sql.Error:
                pass
            try:
                cursor.execute("ALTER TABLE eventos ADD COLUMN hora_inicio TEXT")
            except sql.Error:
                pass
            try:
                cursor.execute("ALTER TABLE eventos ADD COLUMN hora_fin TEXT")
            except sql.Error:
                pass
            conn.commit()
            print('13. Tabla "eventos" creada/actualizada exitosamente')

            #14. plan de housekeeping
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS housekeeping_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habitacion TEXT NOT NULL,
                id_personal INTEGER NOT NULL,
                fecha_asignacion DATE DEFAULT (date('now')),
                completado BOOLEAN DEFAULT 0,
                fecha_finalizacion DATE DEFAULT NULL,
                FOREIGN KEY (habitacion) REFERENCES habitaciones(numero),
                FOREIGN KEY (id_personal) REFERENCES personal(id)
            );
            """)
            conn.commit()
            print('14. Tabla "housekeeping_plan" creada exitosamente')

            #15. inventario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                stock_actual INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 0,
                unidad TEXT NOT NULL,
                precio_unitario REAL DEFAULT 0,
                notas TEXT
            );
            """)
            conn.commit()
            print('15. Tabla "inventario" creada exitosamente')

            # transacciones de inventario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacciones_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_inventario INTEGER NOT NULL,
                tipo TEXT NOT NULL, -- 'entrada' o 'salida'
                cantidad INTEGER NOT NULL,
                fecha DATETIME DEFAULT (datetime('now')),
                area_id INTEGER NOT NULL,
                motivo TEXT,
                FOREIGN KEY (id_inventario) REFERENCES inventario(id),
                FOREIGN KEY (area_id) REFERENCES areas(id)
            );
            """)
            conn.commit()
            print('16. Tabla "transacciones_inventario" creada exitosamente')
                       
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_reserva INTEGER,
                monto_local REAL,
                moneda TEXT,
                tasa REAL,
                monto_equivalente REAL,
                fecha TEXT
            );
            """)
            conn.commit()
            cursor.execute("ALTER TABLE pagos ADD COLUMN fuente_tasa TEXT DEFAULT 'Manual'")
            conn.close()
            print('Todas las tablas creadas exitosamente')
        except sql.Error as e:
            print(f'Error al realizar verificacion de tablas: {e}')
            conn.close()

def insertar_datos_muestra():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Insertar Tipos de Habitación
            cursor.execute("""
            INSERT INTO tipos_habitacion (nombre, capacidad, precio_base, descripcion) VALUES
            ('Individual', 1, 50.00, 'Habitación individual con cama simple'),
            ('Doble', 2, 80.00, 'Habitación doble con cama matrimonial o dos camas individuales'),
            ('Suite', 4, 150.00, 'Suite de lujo con sala de estar y amenities premium'),
            ('Presidencial', 6, 300.00, 'Suite presidencial con todas las comodidades');
            """)

            # Insertar Clientes
            cursor.execute("""
            INSERT INTO clientes (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email) VALUES
            ('María', 'Pérez', 'Cédula', '001-1234567-8', '1995-02-01', 'Femenino', 'Dominicana', '809-555-0000', 'maria@example.com'),
            ('Juan', 'Gómez', 'Pasaporte', 'P123456', '1990-11-10', 'Masculino', 'Argentina', '11-5555-5555', 'juan@example.com'),
            ('Ana', 'Rodríguez', 'Cédula', '001-2345678-9', '1988-07-15', 'Femenino', 'Dominicana', '809-555-1111', 'ana@example.com'),
            ('Carlos', 'López', 'Cédula', '001-3456789-0', '1992-03-20', 'Masculino', 'Dominicana', '809-555-2222', 'carlos@example.com'),
            ('Sofia', 'Martínez', 'Pasaporte', 'P789012', '1993-09-12', 'Femenino', 'Español', '34-666-777-888', 'sofia@example.com'),
            ('Roberto', 'Fernández', 'Cédula', '001-4567890-1', '1985-12-05', 'Masculino', 'Dominicana', '809-555-3333', 'roberto@example.com'),
            ('Carmen', 'García', 'Cédula', '001-5678901-2', '1991-06-18', 'Femenino', 'Dominicana', '809-555-4444', 'carmen@example.com'),
            ('Miguel', 'Santos', 'Cédula', '001-6789012-3', '1987-04-25', 'Masculino', 'Dominicana', '809-555-5555', 'miguel@example.com');
            """)

            # Insertar Habitaciones
            cursor.execute("""
            INSERT INTO habitaciones (numero, tipo_id, estado, ubicacion, capacidad) VALUES
            ('101', 2, 'Ocupada', '1er Piso', 2),
            ('102', 1, 'Ocupada', '1er Piso', 1),
            ('103', 1, 'Limpiando', '1er Piso', 1),
            ('201', 3, 'Disponible', '2do Piso', 4),
            ('202', 2, 'Mantenimiento', '2do Piso', 2),
            ('203', 3, 'Ocupada', '2do Piso', 4),
            ('301', 2, 'Disponible', '3er Piso', 2),
            ('302', 2, 'Ocupada', '3er Piso', 2),
            ('401', 4, 'Disponible', '4to Piso', 6),
            ('402', 3, 'Limpiando', '4to Piso', 4);
            """)

            # Insertar Áreas
            cursor.execute("""
            INSERT OR IGNORE INTO areas (nombre) VALUES
            ('Housekeeping'),
            ('Mantenimiento'),
            ('Front Desk'),
            ('Cocina'),
            ('Admin');
            """)

            # Insertar Personal
            cursor.execute("""
            INSERT INTO personal (codigo, nombre, apellido, puesto, area_id, salario_hora, fecha_contratacion, telefono, email) VALUES
            ('EMP001', 'María', 'López', 'Supervisora', (SELECT id FROM areas WHERE nombre='Housekeeping'), 15.00, '2023-01-15', '809-111-1111', 'maria.lopez@hotel.com'),
            ('EMP002', 'Carlos', 'Méndez', 'Técnico', (SELECT id FROM areas WHERE nombre='Mantenimiento'), 18.00, '2023-02-20', '809-222-2222', 'carlos.mendez@hotel.com'),
            ('EMP003', 'Ana', 'García', 'Recepcionista', (SELECT id FROM areas WHERE nombre='Front Desk'), 12.00, '2023-03-10', '809-333-3333', 'ana.garcia@hotel.com'),
            ('EMP004', 'Roberto', 'Silva', 'Técnico', (SELECT id FROM areas WHERE nombre='Mantenimiento'), 18.00, '2023-04-05', '809-444-4444', 'roberto.silva@hotel.com'),
            ('EMP005', 'Carmen', 'Vega', 'Conserje', (SELECT id FROM areas WHERE nombre='Housekeeping'), 10.00, '2023-05-12', '809-555-5555', 'carmen.vega@hotel.com');
            """)

            # Insertar Ingresos
            cursor.execute("""
            INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago, fecha_pago, numero_transaccion, notas) VALUES
            ('reserva', 'Pago reserva habitación 101 - María Pérez - 2 noches', 160.00, 'tarjeta', date('now'),'TXN001234', 'Pago realizado al check-in'),
            ('reserva', 'Pago reserva habitación 102 - Juan Gómez - 1 noche', 50.00, 'efectivo', date('now'), 'TXN001235', 'Pago realizado al check-in'),
            ('reserva', 'Pago reserva habitación 203 - Roberto Fernández - 2 noches', 300.00, 'tarjeta', date('now', '-1 day'), 'TXN001236', 'Pago realizado al check-in'),
            ('walk_in', 'Pago walk-in habitación 302 - Pedro Ramírez - 1 noche', 80.00, 'efectivo', date('now'), 'TXN001237', 'Pago realizado al check-in walk-in'),
            ('costo_adicional_checkout', 'Servicios adicionales habitación 101 - minibar y llamadas', 45.50, 'tarjeta', date('now'), 'TXN001238', 'Cargos adicionales al check-out'),
            ('costo_adicional_checkout', 'Servicio de lavandería habitación 101', 25.00, 'tarjeta', date('now'), 'TXN001239', 'Servicio de lavandería'),
            ('evento', 'Pago evento buffet - Conferencia Salón A - 50 personas', 750.00, 'transferencia', date('now', '+5 days'), 'TXN001243', 'Pago evento corporativo'),
            ('evento', 'Pago evento buffet - Boda Salón B - 80 personas', 2000.00, 'cheque', date('now', '+15 days'), 'CHK001244', 'Pago pendiente de confirmación'),
            ('walk_in', 'Pago walk-in habitación 103 - Cliente anterior - 1 noche', 50.00, 'efectivo', date('now', '-25 days'), 'TXN000124', 'Ingreso del mes anterior'),
            ('costo_adicional_checkout', 'Servicios adicionales habitación 202 - minibar', 35.75, 'tarjeta', date('now', '-20 days'), 'TXN000125', 'Ingreso del mes anterior'),
            ('reserva', 'Pago reserva habitación 201 - Ana Rodríguez - 2 noches', 300.00, 'tarjeta', date('now', '+1 day'), 'TXN001245', 'Pago realizado al check-in'),
            ('reserva', 'Pago reserva habitación 301 - Carlos López - 2 noches', 160.00, 'tarjeta', date('now', '+2 days'), 'TXN001246', 'Pago realizado al check-in'),
            ('reserva', 'Pago reserva habitación 401 - Sofia Martínez - 2 noches', 600.00, 'transferencia', date('now', '+5 days'), 'TXN001247', 'Pago realizado al check-in'),
            ('reserva', 'Pago reserva habitación 103 - Carmen García - 2 noches', 100.00, 'efectivo', date('now', '+10 days'), 'TXN001248', 'Pago realizado al check-in');
            """)

            # Insertar Reservas
            cursor.execute("""
            INSERT INTO reservas (
                numero_hab, tipo_habitacion, id_cliente, cliente_nombre, cliente_email,
                fecha_entrada, fecha_salida, id_pago, monto_pago,
                checked_in, checked_out, estado, notas
            ) VALUES
            ('101', 'Doble', 1, 'María Pérez', 'maria@example.com', date('now'), date('now', '+2 days'), 1, 160.00, 1, 0, 'En curso', ''),
            ('102', 'Individual', 2, 'Juan Gómez', 'juan@example.com', date('now'), date('now', '+1 day'), 2, 50.00, 1, 0, 'En curso', ''),
            ('203', 'Suite', 6, 'Roberto Fernández', 'roberto@example.com', date('now', '-1 day'), date('now', '+1 day'), 3, 300.00, 1, 0, 'En curso', ''),
            ('201', 'Suite', 3, 'Ana Rodríguez', 'ana@example.com', date('now', '+1 day'), date('now', '+3 days'), 11, 300.00, 0, 0, 'Pendiente', ''),
            ('301', 'Doble', 4, 'Carlos López', 'carlos@example.com', date('now', '+2 days'), date('now', '+4 days'), 12, 160.00, 0, 0, 'Pendiente', ''),
            ('401', 'Presidencial', 5, 'Sofia Martínez', 'sofia@example.com', date('now', '+5 days'), date('now', '+7 days'), 13, 600.00, 0, 0, 'Pendiente', ''),
            ('103', 'Individual', 7, 'Carmen García', 'carmen@example.com', date('now', '+10 days'), date('now', '+12 days'), 14, 100.00, 0, 0, 'Pendiente', ''),
            ('101', 'Doble', 8, 'Luis Pérez', 'luis@example.com', date('now', '-7 days'), date('now', '-5 days'), 15, 160.00, 1, 1, 'Completada', 'Estancia finalizada sin incidencias'),
            ('203', 'Suite', 9, 'Elena Torres', 'elena@example.com', date('now', '-12 days'), date('now', '-10 days'), 16, 300.00, 1, 1, 'Completada', ''),
            ('102', 'Individual', 10, 'Mario Díaz', 'mario@example.com', date('now', '-3 days'), date('now', '-1 day'), 17, 50.00, 0, 0, 'Cancelada', 'Cancelada por el cliente'),
            ('301', 'Doble', 11, 'Ana Ruiz', 'ana.ruiz@example.com', date('now', '+4 days'), date('now', '+6 days'), 18, 160.00, 0, 0, 'Cancelada', 'Cancelada por no show');
            """)

            # Insertar Walk-ins
            cursor.execute("""
            INSERT INTO walk_ins (
                numero_hab, cliente_nombre, cliente_email, fecha_entrada, fecha_salida,
                total_personas, id_pago, checked_in, checked_out, estado, notas
            ) VALUES
            ('302', 'Pedro Ramírez', 'pedro@example.com', date('now'), date('now', '+1 day'), 2, 4, 1, 0, 'En curso', 'Walk-in de ejemplo'),
            ('103', 'Cliente anterior', 'clienteanterior@example.com', date('now', '-25 days'), date('now', '-24 days'), 1, 9, 1, 0, 'Finalizado', 'Walk-in del mes anterior');
            """)

            # Insertar Tickets de Mantenimiento
            cursor.execute("""
            INSERT INTO tickets_mantenimiento 
            (habitacion, area_hotel, descripcion, estado, prioridad, tecnico_id, fecha_asignacion, fecha_fin, descripcion_solucion) VALUES
            ('202', NULL, 'Aire acondicionado no funciona', 'Asignado', 'Alta', 4, '2025-10-05', NULL, NULL),
            ('103', NULL, 'Fuga de agua en baño', 'En Progreso', 'Alta', 2, '2025-10-05', NULL, NULL),
            ('302', NULL, 'Cerradura defectuosa', 'Sin asignar', 'Media', NULL, NULL, NULL, NULL),
            ('102', NULL, 'Luz del baño no funciona', 'Completado', 'Media', 2, '2025-10-04', '2025-10-04', 'Se reemplazó el bombillo y se verificó el circuito'),
            (NULL, 'Piscina', 'Sistema de bombas no arranca', 'En Progreso', 'Alta', 4, '2025-10-05', NULL, NULL),
            (NULL, 'Lobby', 'Falla en aire central', 'Asignado', 'Alta', 2, '2025-10-05', NULL, NULL),
            (NULL, 'Ascensor', 'Botón de emergencia no responde', 'Completado', 'Alta', 4, '2025-10-03', '2025-10-03', 'Se reemplazó el panel de control del botón de emergencia'),
            (NULL, 'Restaurante', 'Horno eléctrico no enciende', 'Sin asignar', 'Media', NULL, NULL, NULL, NULL);
            """)

            # Insertar Housekeeping Plan
            cursor.execute("""
            INSERT INTO housekeeping_plan (habitacion, id_personal, fecha_asignacion, completado, fecha_finalizacion) VALUES
            ('103', 1, date('now'), 0, NULL),
            ('201', 5, date('now'), 1, date('now')),
            ('402', 5, date('now', '+1 day'), 0, NULL);
            """)

            # Insertar Check-ins y Check-outs
            cursor.execute("""
            INSERT INTO checkins_checkouts (reserva_id, walk_in_id, tipo, usuario, notas) VALUES
            (1, NULL, 'checkin', 'Ana García', 'Check-in realizado sin problemas'),
            (2, NULL, 'checkin', 'Ana García', 'Check-in realizado, huésped satisfecho'),
            (NULL, 1, 'checkin', 'Ana García', 'Walk-in check-in realizado'),
            (6, NULL, 'checkin', 'Ana García', 'Check-in realizado'),
            (1, NULL, 'checkout', 'Ana García', 'Check-out realizado, habitación en buen estado');
            """)

            # Insertar Buffet
            cursor.execute("""
            INSERT INTO buffet (fecha, personas, menu, precio_por_persona, total, notas) VALUES
            (date('now', '+5 days'), 50, 'Clásico', 15.00, 750.00, 'Evento corporativo'),
            (date('now', '+15 days'), 80, 'Premium', 25.00, 2000.00, 'Boda'),
            (date('now', '+25 days'), 30, 'Clásico', 15.00, 450.00, 'Reunión familiar'),
            (date('now', '+35 days'), 100, 'Deluxe', 35.00, 3500.00, 'Conferencia empresarial');
            """)

            # Insertar Eventos
            cursor.execute("""
            INSERT INTO eventos (tipo, salon, fecha, hora, equipamiento, categoria, personas, tarifa_salon, total, notas) VALUES
            ('Conferencia', 'Salón A', date('now', '+10 days'), '09:00', 'Proyector, Micrófonos', 'Buffet', 100, 500.00, 2300.00, 'Conferencia anual de empresa'),
            ('Boda', 'Salón B', date('now', '+20 days'), '18:00', 'Iluminación, Sonido', 'Buffet', 150, 800.00, 3500.00, 'Boda de María y Juan'),
            ('Seminario', 'Salón C', date('now', '+30 days'), '14:00', 'Proyector, Pizarra', 'Buffet', 75, 300.00, 1500.00, 'Seminario de capacitación'),
            ('Cena de Gala', 'Salón Principal', date('now', '+40 days'), '19:30', 'Iluminación Premium', 'Buffet', 200, 1200.00, 5000.00, 'Cena de gala anual');
            """)

            # Insertar Inventario
            cursor.execute("""
            INSERT INTO inventario (item, stock_actual, stock_minimo, unidad, precio_unitario) VALUES
            ('Sábanas', 120, 80, 'unidad', 15.00),
            ('Toallas', 200, 150, 'unidad', 8.00),
            ('Jabón', 300, 200, 'unidad', 2.50),
            ('Shampoo', 250, 180, 'unidad', 3.00),
            ('Papel higiénico', 400, 300, 'rollo', 1.50),
            ('Café', 50, 30, 'kg', 12.00),
            ('Azúcar', 25, 15, 'kg', 3.50),
            ('Leche', 40, 25, 'litro', 2.80);
            """)
            
            # Insertar datos de muestra en transacciones de inventario
            cursor.execute("""
            INSERT INTO transacciones_inventario (id_inventario, tipo, cantidad, area_id, motivo) VALUES
            (1, 'Entrada', 50, (SELECT id FROM areas WHERE nombre='Admin'), 'Compra de sábanas'),
            (2, 'Salida', 20, (SELECT id FROM areas WHERE nombre='Housekeeping'), 'Entrega de toallas a habitaciones'),
            (3, 'Entrada', 100, (SELECT id FROM areas WHERE nombre='Admin'), 'Compra de jabón'),
            (4, 'Salida', 10, (SELECT id FROM areas WHERE nombre='Housekeeping'), 'Reposición de shampoo en habitaciones'),
            (5, 'Entrada', 200, (SELECT id FROM areas WHERE nombre='Admin'), 'Compra de papel higiénico'),
            (6, 'Salida', 5, (SELECT id FROM areas WHERE nombre='Cocina'), 'Consumo de café en desayuno'),
            (7, 'Entrada', 10, (SELECT id FROM areas WHERE nombre='Admin'), 'Compra de azúcar'),
            (8, 'Salida', 8, (SELECT id FROM areas WHERE nombre='Cocina'), 'Consumo de leche en cocina');
            """)

            conn.commit()
            print('Datos de muestra insertados correctamente.')
        except sql.Error as e:
            print(f'Error al insertar datos: {e}')
        finally:
            conn.close()

def limpiar_datos():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Borrar datos de todas las tablas (en orden inverso para respetar FK)
            cursor.execute("DELETE FROM ingresos;")
            cursor.execute("DELETE FROM inventario;")
            cursor.execute("DELETE FROM eventos;")
            cursor.execute("DELETE FROM buffet;")
            cursor.execute("DELETE FROM checkins_checkouts;")
            cursor.execute("DELETE FROM walk_ins;")
            cursor.execute("DELETE FROM tickets_mantenimiento;")
            cursor.execute("DELETE FROM housekeeping_plan;")
            cursor.execute("DELETE FROM personal;")
            cursor.execute("DELETE FROM reservas;")
            cursor.execute("DELETE FROM habitaciones;")
            cursor.execute("DELETE FROM tipos_habitacion;")
            cursor.execute("DELETE FROM clientes;")
            cursor.execute("DELETE FROM transacciones_inventario;")

            # Verificar que todas las tablas estén vacías
            cursor.execute("""
            SELECT 'inventario' as tabla, COUNT(*) as registros FROM inventario
            UNION ALL
            SELECT 'transacciones_inventario' as tabla, COUNT(*) as registros FROM transacciones_inventario
            UNION ALL
            SELECT 'eventos', COUNT(*) FROM eventos
            UNION ALL
            SELECT 'buffet', COUNT(*) FROM buffet
            UNION ALL
            SELECT 'checkins_checkouts', COUNT(*) FROM checkins_checkouts
            UNION ALL
            SELECT 'walk_ins', COUNT(*) FROM walk_ins
            UNION ALL
            SELECT 'tickets_mantenimiento', COUNT(*) FROM tickets_mantenimiento
            UNION ALL
            SELECT 'housekeeping_plan', COUNT(*) FROM housekeeping_plan
            UNION ALL
            SELECT 'personal', COUNT(*) FROM personal
            UNION ALL
            SELECT 'reservas', COUNT(*) FROM reservas
            UNION ALL
            SELECT 'habitaciones', COUNT(*) FROM habitaciones
            UNION ALL
            SELECT 'tipos_habitacion', COUNT(*) FROM tipos_habitacion
            UNION ALL
            SELECT 'clientes', COUNT(*) FROM clientes;
            """)
            cursor.execute("""
            DELETE FROM sqlite_sequence WHERE name IN (
                'clientes', 'tipos_habitacion', 'habitaciones', 'reservas', 'personal',
                'turnos', 'tickets_mantenimiento', 
                'mantenimiento', 'walk_ins', 'checkins_checkouts',
                'buffet', 'eventos', 'housekeeping_plan', 'inventario', 'ingresos', 'transacciones_inventario'
            );
            """)
            conn.commit()
            print('Datos eliminados exitosamente')
        except sql.Error as e:
            print(f'Error al eliminar datos: {e}')
        finally:
            conn.close()

def validar_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except Exception:
        return None

def kpi_alojamiento(): #retorna la cantidad de habitaciones ocupadas y la cantidad de personas alojadas en el día de hoy
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                'Personas alojadas hoy' as concepto,
                COUNT(*) as habitaciones_ocupadas,
                SUM(total_personas) as personas_alojadas
            FROM (
                -- Reservas con check-in realizado y sin check-out
                SELECT r.numero_hab, r.total_personas
                FROM reservas r
                WHERE date('now') BETWEEN r.fecha_entrada AND r.fecha_salida
                AND r.checked_in = 1 AND r.checked_out = 0

                UNION ALL

                -- Walk-ins con check-in realizado y sin check-out
                SELECT w.numero_hab, w.total_personas
                FROM walk_ins w
                WHERE date('now') BETWEEN w.fecha_entrada AND w.fecha_salida
                AND w.checked_in = 1 AND w.checked_out = 0
            ) ocupadas;
            """)
            resultado = cursor.fetchone()
            return (resultado[0] if resultado[0] is not None else 0, 
                    resultado[1] if resultado[1] is not None else 0,
                    resultado[2] if resultado[2] is not None else 0,)
            #desgloce de "resultado" q es una tupla
            #[0] = un string descriptivo que dice "Personas alojadas hoy"
            #[1] = la cantidad de habitaciones ocupadas
            #[2] = la cantidad de personas alojadas en el día de hoy
        except sql.Error as e:
            print(f'Error al calcular alojamiento: {e}')
        finally:
            conn.close()

def total_checkin(): #retorna el total de checkin del dia de hoy
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT COUNT(*) as total_checkins_programados_hoy
            FROM reservas 
            WHERE fecha_entrada = date('now') 
            AND checked_in = 0 
            AND checked_out = 0;
            """)
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] is not None else 0
        except sql.Error as e:
            print(f'Error al calcular alojamiento: {e}')
        finally:
            conn.close()

def ingresos_reservas(): #retorna el total de ingresos de reservas del mes
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                SUM(monto) as total_ingresos_reservas_mes
            FROM ingresos 
            WHERE tipo_ingreso = 'reserva'
            AND strftime('%Y-%m', fecha_pago) = strftime('%Y-%m', date('now'));
            """)
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] is not None else 0
        except sql.Error as e:
            print(f'Error al calcular alojamiento: {e}')
        finally:
            conn.close()

def total_habitaciones(): #retorna el total de habitaciones del hotel
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) as total_habitaciones FROM habitaciones;")
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] else 0
        except sql.Error as e:
            print(f'Error al calcular total de habitaciones: {e}')
        finally:
            conn.close()

def reservas_activas(): #retorna el total de reservas activas (próximas)
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT COUNT(*) as reservas_proximas
            FROM reservas 
            WHERE fecha_entrada > date('now');
            """)
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] else 0
        except sql.Error as e:
            print(f'Error al calcular las reservas activas: {e}')
        finally:
            conn.close()

def ingresos_mes(): #retorna el total de ingresos del mes, el total de transacciones y el promedio por transaccion
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                SUM(monto) as ingresos_mes_actual,
                COUNT(*) as total_transacciones,
                AVG(monto) as promedio_por_transaccion
            FROM ingresos 
            WHERE strftime('%Y-%m', fecha_pago) = strftime('%Y-%m', date('now'))
            """)
            resultado = cursor.fetchone()
            return (resultado[0] if resultado[0] is not None else 0, 
                    resultado[1] if resultado[1] is not None else 0,
                    resultado[2] if resultado[2] is not None else 0,)
            #desgloce de "resultado" q es una tupla
            #[0] = el total de ingresos del mes
            #[1] = el total de transacciones del mes
            #[2] = el promedio  por transacción
        except sql.Error as e:
            print(f'Error al calcular los ingresos del mes: {e}')
        finally:
            conn.close()

def obtener_clientes(): #obtiene todos los clientes en la bd
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                id as "ID",
                nombres as "Nombres",
                apellidos as "Apellidos",
                tipo_doc as "Documento",
                numero_doc as "Nro. Doc",
                fecha_nac as "Cumpleaños",
                genero as "Género",
                nacionalidad as "Nacionalidad",
                telefono as "Teléfono",
                email as "E-mail"
            FROM clientes
            ORDER BY id;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener clientes: {e}')
        finally:
            conn.close()

def buscar_cliente(texto): #el query de consulta para buscar cliente
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id, nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email FROM clientes 
                WHERE id LIKE ? OR nombres LIKE ? OR apellidos LIKE ? OR email LIKE ? OR telefono LIKE ? OR numero_doc LIKE ?
                ORDER BY nombres
            """, (f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al buscar: {e}')
        finally:
            conn.close()

def obtener_habitaciones(): #obtiene todas las habitaciones en la bd
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                h.id as "ID",
                h.numero as "Número",
                th.nombre as "Tipo",
                h.estado as "Estado",
                h.ubicacion as "Ubicación",
                h.capacidad as "Capacidad",
                h.notas as "Notas"
            FROM habitaciones h
            JOIN tipos_habitacion th ON h.tipo_id = th.id
            ORDER BY h.numero;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener habitaciones: {e}')
        finally:
            conn.close()

def obtener_reservas():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                r.id as "ID",
                r.numero_hab as "Hab.",
                r.cliente_nombre as "Cliente",
                r.cliente_email as "Email",
                r.fecha_entrada as "Entrada",
                r.fecha_salida as "Salida",
                r.total_personas as "Personas Alojadas",
                r.monto_pago as "Total",
                r.estado as "Estado"
                
            FROM reservas r
            ORDER BY r.fecha_entrada DESC;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener reservas: {e}')
        finally:
            conn.close()

def email_unico(email, cliente_actual = None): #valida que el email de un cliente sea unico 
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if cliente_actual:
                #para edicion: verifica que no exista otro cliente con el mismo email
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = ? AND email != ?", (email, cliente_actual[9]))
            else:
                #para agregar: verifica que no exista ningun cliente con ese email
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = ?", (email,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False, "El correo electrónico ya existe"
            return True, "Email válido"
        except sql.Error as e:
            return False, f'Error al validar email: {e}'
        finally:
            conn.close()
        
def doc_unico(numero_doc, cliente_actual = None): # valida que el doc de identidad de un cliente sea unico
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if cliente_actual:
                #para edicion: verifica que no exista otro cliente con el mismo documento
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE numero_doc = ? AND numero_doc != ?", (numero_doc, cliente_actual[4]))
            else:
                #para agregar: verifica que no exista ningun cliente con ese documento
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE numero_doc = ?", (numero_doc,))
            count = cursor.fetchone()[0]
            if count > 0:
                return False, "El número de documento ya existe"
            return True, "Documento válido"
        except sql.Error as e:
            return False, f'Error al validar documento: {e}'
        finally:
            conn.close()
        
def eliminar_cliente(id): #elimina un cliente de la base de datos
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
            conn.commit()
            return True, 'Cliente eliminado exitosamente'
        except sql.Error as e:
            return False, f'Error al eliminar cliente: {e}'
        finally:
            conn.close()

def guardar_cliente(tipo, datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar": #agregar cliente
                cursor.execute("""
                INSERT INTO clientes(nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email, fecha_registro)
                VALUES (?,?,?,?,?,?,?,?,?, date('now'))
                """, (datos))
            else: #editar cliente
                cursor.execute("""
                UPDATE clientes
                SET nombres = ?, apellidos = ?, tipo_doc = ?, numero_doc = ?, fecha_nac = ?, genero = ?, nacionalidad = ?, telefono = ?, email = ?
                WHERE numero_doc = ?
                """, (*datos[:9], datos[3]))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                if datos[3] in str(e):
                    return False, "El número de documento ya existe"
                elif datos[8] in str(e):
                    return False, "El e-mail ya existe"
            else:
                return False, f"Error de integridad de datos: {e}"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def obtener_tipos_habitaciones():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM tipos_habitacion
            ORDER BY id;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener tipos de habitaciones: {e}')
        finally:
            conn.close()

def buscar_habitacion(texto, estado): #el query de consulta para buscar
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    h.id as "ID",
                    h.numero as "Número",
                    th.nombre as "Tipo",
                    h.estado as "Estado",
                    h.ubicacion as "Ubicación",
                    h.capacidad as "Capacidad",
                    h.notas as "Notas"
                FROM habitaciones h
                JOIN tipos_habitacion th ON h.tipo_id = th.id
                WHERE 
                    (? = 'Todos' OR h.estado = ?)
                    AND (
                        h.numero LIKE ? 
                        OR th.nombre LIKE ? 
                        OR h.ubicacion LIKE ? 
                        OR h.notas LIKE ?
                    )
                ORDER BY h.numero;
            """, (estado, estado, f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al buscar: {e}')
        finally:
            conn.close()

def eliminar_habitacion(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM habitaciones WHERE id = ?", (id,))
            conn.commit()
            return True, 'Habitación eliminada exitosamente'
        except sql.Error as e:
            return False, f'Error al eliminar habitación: {e}'
        finally:
            conn.close()

def id_tipo_hab(tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id, capacidad FROM tipos_habitacion
            WHERE nombre = ?;
            """, (tipo,))
            resultado = cursor.fetchone()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener tipos de habitaciones: {e}')
        finally:
            conn.close()

def hab_por_tipo(tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM habitaciones
            WHERE tipo_id = ?;
            """, (id_tipo_hab(tipo)[0],))
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener habitaciones: {e}')
        finally:
            conn.close()

def precio_por_tipo(tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT precio_base FROM tipos_habitacion
            WHERE nombre = ?;
            """, (tipo,))
            resultado = cursor.fetchone()
            return resultado[0]
        except sql.Error as e:
            print(f'Error al obtener habitaciones: {e}')
        finally:
            conn.close()

def guardar_habitacion(tipo, datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar": #agregar habitacion
                cursor.execute("""
                INSERT INTO habitaciones(numero, tipo_id, estado, ubicacion, capacidad, notas)
                VALUES (?,?,?,?,?,?)
                """, (datos))
            else: #editar cliente
                cursor.execute("""
                UPDATE habitaciones
                SET numero = ?, tipo_id = ?, estado = ?, ubicacion = ?, capacidad = ?, notas = ?
                WHERE numero = ?
                """, (*datos[:6], datos[0]))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def eliminar_tipo_habitacion(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tipos_habitacion WHERE id = ?", (id,))
            conn.commit()
            return True, 'Tipo eliminado exitosamente'
        except sql.Error as e:
            return False, f'Error al eliminar tipo: {e}'
        finally:
            conn.close()

def guardar_tipo_habitacion(tipo, datos, clave):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar": #agregar habitacion
                cursor.execute("""
                INSERT INTO tipos_habitacion(nombre,capacidad,precio_base,descripcion)
                VALUES (?,?,?,?)
                """, (datos))
            else: #editar cliente
                cursor.execute("""
                UPDATE tipos_habitacion
                SET nombre = ?, capacidad = ?, precio_base = ?, descripcion = ? 
                WHERE nombre = ?
                """, (*datos[:4], clave))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def hab_disponibles(fecha_entrada, fecha_salida, tipo = "Todos", capacidad_minima = None):
    query = """
            SELECT h.*
            FROM habitaciones h
            WHERE h.estado = 'Disponible'
            AND h.numero NOT IN (
                SELECT r.numero_hab
                FROM reservas r
                WHERE r.estado != 'Cancelada'
                AND r.fecha_entrada < :fecha_salida
                AND r.fecha_salida > :fecha_entrada
            )
            -- Caso especial: si la fecha de entrada es hoy, excluir habitaciones con check-in activo
            AND (:fecha_entrada != DATE('now')
                OR h.numero NOT IN (
                    SELECT r.numero_hab
                    FROM reservas r
                    WHERE r.checked_in = 1 AND r.checked_out = 0
                )
            );
            """
    
    query2 = """
            SELECT nombre FROM tipos_habitacion
            WHERE id = ?
            """
    
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, {"fecha_entrada": fecha_entrada, "fecha_salida": fecha_salida})
            habitaciones = cursor.fetchall()
            resultado = []
            for habitacion in habitaciones:
                datos_hab = []
                datos_hab.append(habitacion[1])
                cursor.execute(query2, (habitacion[2],))
                tipo_hab = cursor.fetchone()[0]
                datos_hab.append(tipo_hab)
                datos_hab.append(habitacion[4])
                datos_hab.append(habitacion[5])

                resultado.append(datos_hab)
            if tipo != "Todos":
                resultado = [habitacion for habitacion in resultado if habitacion[1] == tipo]
            if capacidad_minima is not None:
                resultado = [habitacion for habitacion in resultado if habitacion[3] >= capacidad_minima]

            return resultado #retorna una lista con los siguientes datos:
            #0: el numero de la habitacion
            #1: el tipo de habitación
            #2: la ubicacion de la habitacion
            #3: la capacidad de la habitacion
        except sql.Error as e:
            print(f'Error al obtener habitaciones: {e}')
        finally:
            conn.close()

def registrar_pago(datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago, fecha_pago, numero_transaccion, notas) 
                VALUES (?, ?, ?, ?, date('now'),?, ?)
                """, (datos))
            conn.commit()
            pago_id = cursor.lastrowid
            return True, "Pago registrado exitosamente", pago_id
        except sql.Error as e:
            return False, f"Error al registrar pago: {e}", None
        finally:
            conn.close()

def guardar_reserva(tipo, datos, clave = None):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar": #agregar reserva
                cursor.execute("""
                INSERT INTO reservas(numero_hab, tipo_habitacion, id_cliente, cliente_nombre, cliente_email, fecha_entrada, fecha_salida, total_personas,id_pago, monto_pago, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (datos))
            else: #editar reserva. las reservas no se editan
                # cursor.execute("""
                # UPDATE tipos_habitacion
                # SET nombre = ?, capacidad = ?, precio_base = ?, descripcion = ? 
                # WHERE nombre = ?
                # """, (*datos[:4], clave))
                pass
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def buscar_reserva(texto, estado):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                r.id as "ID",
                r.numero_hab as "Hab.",
                r.cliente_nombre as "Cliente",
                r.cliente_email as "Email",
                r.fecha_entrada as "Entrada",
                r.fecha_salida as "Salida",
                r.total_personas as "Personas Alojadas",
                r.monto_pago as "Total",
                r.estado as "Estado"
                
                FROM reservas r
                WHERE 
                    (? = 'Todos' OR r.estado = ?)
                    AND (
                        r.id LIKE ? 
                        OR r.numero_hab LIKE ?
                        OR r.cliente_nombre LIKE ?
                        OR r.cliente_email LIKE ?
                        OR r.fecha_entrada LIKE ?
                        OR r.fecha_salida LIKE ?
                    )
                ORDER BY r.fecha_entrada DESC;
            """, (estado, estado, f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al buscar: {e}')
        finally:
            conn.close()

def ver_reserva(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM reservas
            WHERE id = ?;
            """, (id,))
            resultado = cursor.fetchone()

            return [resultado[0], #id de la reserva
                    resultado[1], #numero de habitacion
                    resultado[2], #tipo de habitacion
                    resultado[4], #nombre del cliente
                    resultado[5], #correo del cliente
                    resultado[6], #fecha de entrada
                    resultado[7], #fecha de salida
                    resultado[8], #total de huespedes
                    resultado[10], #monto pagado
                    resultado[13], #estado
                    resultado[14], #fecha de reserva
                    resultado[15] #notas
                    ]
        except sql.Error as e:
            print(f'Error al obtener reserva: {e}')
        finally:
            conn.close()

def kpi_housekeeping():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                estado,
                COUNT(*) as cantidad
            FROM habitaciones
            WHERE estado IN ('Sucia', 'Limpiando', 'Disponible')
            GROUP BY estado;
            """)
            consulta = cursor.fetchall()
            resultado = dict(consulta)
            for estado in ['Sucia', 'Limpiando', 'Disponible']:
                if estado not in resultado:
                    resultado[estado] = 0
            return resultado
        except sql.Error as e:
            print(f'Error al obtener tipos de habitaciones: {e}')
        finally:
            conn.close()

def modificar_estado_reserva(estado, id, motivo = None):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if motivo is None:
                cursor.execute("""
                    UPDATE reservas
                    SET estado = ? 
                    WHERE id = ?
                    """, (estado, id))
            else:
                cursor.execute("""
                    UPDATE reservas
                    SET estado = ?, notas = ? 
                    WHERE id = ?
                    """, (estado, motivo, id))
            conn.commit()
            return True, "Datos modificados exitosamente"
        except sql.Error as e:
            return False, f'Error al modificar estado de reserva: {e}'
        finally:
            conn.close()

def obtener_hab_sucias():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM habitaciones
            WHERE estado = 'Sucia';
            """)
            consulta = cursor.fetchall()
            resultado = []
            for habitacion in consulta:
                resultado.append(f'{habitacion[1]}, {habitacion[4]}')
            return resultado
        except sql.Error as e:
            print(f'Error al obtener tipos de habitaciones: {e}')
        finally:
            conn.close()

def obtener_personal_housekeeping():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM personal
            WHERE area_id = 1 AND estado = 'Activo'
            ORDER BY codigo;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for empleado in consulta:
                resultado.append(f'{empleado[1]} - {empleado[2]} {empleado[3]}')
            return resultado
        except sql.Error as e:
            print(f'Error al obtener empleados: {e}')
        finally:
            conn.close()

def obtener_plan_limpieza():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                hp.id AS "ID",
                h.numero AS "Habitación",
                th.nombre AS "Tipo",
                h.ubicacion AS "Ubicación",
                p.codigo AS "Código Personal",
                p.nombre AS "Nombre Personal",
                p.apellido AS "Apellido Personal",
                hp.fecha_asignacion AS "Fecha Asignación",
                hp.completado AS "Completado",
                hp.fecha_finalizacion AS "Fecha Finalización"
            FROM housekeeping_plan hp
            JOIN habitaciones h ON hp.habitacion = h.numero
            JOIN tipos_habitacion th ON h.tipo_id = th.id
            JOIN personal p ON hp.id_personal = p.id
            WHERE 
                (hp.completado = 0)
                OR
                (hp.completado = 1 AND hp.fecha_finalizacion = date('now'))
            ORDER BY hp.fecha_asignacion DESC;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for fila in consulta:
                resultado.append([fila[0], #ID
                                  f'{fila[1]} ({fila[2]}, {fila[3]})', #Habitación (número, tipo y ubicacion)
                                  f'{fila[4]} - {fila[5]} {fila[6]}', #Empleado (código y nombre completo)
                                  fila[7], #Fecha de asignación
                                  fila[9] if fila[9] is not None else 'N/A', #Fecha de finalización
                                  'En proceso' if fila[8] == 0 else 'Completado' #Estado de la limpieza
                                  ])
            return resultado
        except sql.Error as e:
            print(f'Error al obtener datos: {e}')
        finally:
            conn.close()

def id_empleado(codigo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id FROM personal
            WHERE codigo = ?
            """, (codigo,))
            resultado = cursor.fetchone()
            return resultado[0]
        except sql.Error as e:
            print(f'Error al obtener empleados: {e}')
        finally:
            conn.close()

def asignar_limpieza(datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO housekeeping_plan(habitacion, id_personal)
                VALUES (?, ?)
            """, (datos))
    
            cursor.execute("""
                UPDATE habitaciones
                SET estado = 'Limpiando'
                WHERE numero = ?
            """,(datos[0],))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def completar_limpieza(datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE housekeeping_plan
                SET completado = 1, fecha_finalizacion = date('now')
                WHERE id = ?
            """, (datos[0],))
    
            cursor.execute("""
                UPDATE habitaciones
                SET estado = 'Disponible'
                WHERE numero = ?
            """,(datos[1],))
            conn.commit()
            return True, "Datos actualizados exitosamente"
        except sql.Error as e:
            return False, f"Error al actializar datos: {e}"
        finally:
            conn.close()

def obtener_inventario():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM inventario
            ORDER BY id;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for articulo in consulta:
                resultado.append([
                    articulo[0], #ID
                    articulo[1], #Descripcion
                    articulo[2], #stock actual
                    articulo[4], #unidad de medida
                    articulo[5], #precio unitario
                    'OK' if articulo[3] <= articulo[2] else ('Agotado' if articulo[2] == 0 else 'Bajo'), #nivel de stock
                    articulo[6] if articulo[6] is not None else '', #Notas
                ])
            return resultado
        except sql.Error as e:
            print(f'Error al obtener artículos: {e}')
        finally:
            conn.close()

def obtener_transacciones_inventario():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                ti.id AS "ID Transacción",
                i.item AS "Artículo",
                ti.tipo AS "Tipo",
                ti.cantidad AS "Cantidad",
                i.unidad as "Unidad",
                ti.fecha AS "Fecha y Hora"
            FROM transacciones_inventario ti
            JOIN inventario i ON ti.id_inventario = i.id
            ORDER BY ti.fecha DESC
            LIMIT 10;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener artículos: {e}')
        finally:
            conn.close()

def buscar_articulo(texto):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM inventario
                WHERE 
                        id LIKE ?
                        OR item LIKE ?
                        OR unidad LIKE ?
                        OR precio_unitario LIKE ?
                ORDER BY id DESC;
            """, (f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            consulta = cursor.fetchall()
            resultado = []
            for articulo in consulta:
                resultado.append([
                    articulo[0], #ID
                    articulo[1], #Descripcion
                    articulo[2], #stock actual
                    articulo[4], #unidad de medida
                    articulo[5], #precio unitario
                    'OK' if articulo[3] <= articulo[2] else ('Agotado' if articulo[2] == 0 else 'Bajo'), #nivel de stock
                    articulo[6] if articulo[6] is not None else '', #Notas
                ])
            return resultado
        except sql.Error as e:
            print(f'Error al buscar: {e}')
        finally:
            conn.close()

def stock_minimo(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT stock_minimo FROM inventario
            WHERE id = ?;
            """, (id,))
            consulta = cursor.fetchone()
            resultado = consulta[0]
            return resultado
        except sql.Error as e:
            print(f'Error al obtener artículo: {e}')
        finally:
            conn.close()

def guardar_articulo(data, tipo, id = None):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar" and id is None: #agregar 
                cursor.execute("""
                INSERT INTO inventario(item,stock_actual,stock_minimo,unidad,precio_unitario,notas)
                VALUES (?,?,?,?,?,?)
                """, (data))
            else: #editar
                cursor.execute("""
                UPDATE inventario
                SET item = ?,stock_actual = ?,stock_minimo = ?,unidad = ?,precio_unitario = ?,notas = ?
                WHERE id = ?
                """, (*data[:6], id))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def obtener_areas():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT nombre FROM areas;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for area in consulta:
                resultado.append(area[0])
            return resultado
        except sql.Error as e:
            print(f'Error al obtener areas: {e}')
        finally:
            conn.close()

def ver_area(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT nombre FROM areas
            WHERE id = ?;
            """, (id,))
            consulta = cursor.fetchone()
            resultado = consulta[0]
            return resultado
        except sql.Error as e:
            print(f'Error al obtener dato: {e}')
        finally:
            conn.close()

def ver_id_area(area):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id FROM areas
            WHERE nombre = ?;
            """, (area,))
            consulta = cursor.fetchone()
            resultado = consulta[0]
            return resultado
        except sql.Error as e:
            print(f'Error al obtener dato: {e}')
        finally:
            conn.close()

def ver_transaccion(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM transacciones_inventario
            WHERE id = ?;
            """, (id,))
            resultado = cursor.fetchone()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener información: {e}')
        finally:
            conn.close()

def ajustar_inventario(cantidad, id, tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT stock_actual FROM inventario WHERE id = ?", (id,))
            consulta = cursor.fetchone()
            stock_actual = consulta[0]

            if tipo == 'Entrada':
                cursor.execute("""
                UPDATE inventario
                SET stock_actual = stock_actual + ?
                WHERE id = ?;
                """, (cantidad,id))
            elif tipo == 'Salida':
                if cantidad > stock_actual:
                    return False, f"La cantidad de salida es mayor al stock actual: {stock_actual}"
                cursor.execute("""
                UPDATE inventario
                SET stock_actual = stock_actual - ?
                WHERE id = ?;
                """, (cantidad,id))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def guardar_transaccion(data):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO transacciones_inventario(id_inventario,tipo,cantidad,area_id,motivo)
                VALUES (?,?,?,?,?)
                """, (data))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def insertar_cotizacion_buffet(fecha, personas, menu, precio, total, notas):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO buffet (fecha, personas, menu, precio_por_persona, total, notas) VALUES (?, ?, ?, ?, ?, ?)',
                       (fecha, personas, menu, precio, total, notas))
        conn.commit()
        conn.close()

def obtener_cotizaciones_buffet():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM buffet ORDER BY fecha DESC')
        return cursor.fetchall()
    return []

def eliminar_cotizacion_buffet(id_):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM buffet WHERE id = ?', (id_,))
        conn.commit()
        conn.close()

def obtener_tickets():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                t.id AS ticket_id,
                CASE
                    WHEN t.habitacion IS NOT NULL THEN 'Hab. ' || t.habitacion
                    ELSE t.area_hotel
                END AS ubicacion,
                t.descripcion,
                t.estado,
                t.prioridad,
                p.nombre || ' ' || p.apellido AS tecnico
            FROM tickets_mantenimiento AS t
            LEFT JOIN personal AS p ON t.tecnico_id = p.id
            WHERE 
                -- Mostrar todos excepto los completados antiguos
                t.estado != 'Finalizado' 
                OR (t.estado = 'Finalizado' AND date(t.fecha_fin) = date('now'))
            ORDER BY 
                CASE t.estado
                    WHEN 'Sin asignar' THEN 1
                    WHEN 'Asignado' THEN 2
                    WHEN 'En Progreso' THEN 3
                    WHEN 'Completado' THEN 4
                    ELSE 5
                END,
                t.fecha_creacion ASC;
            """)
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener tickets: {e}')
        finally:
            conn.close()

def lista_habitaciones():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT numero FROM habitaciones
            ORDER BY numero;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for numero in consulta:
                resultado.append(numero[0])
            return resultado
        except sql.Error as e:
            print(f'Error al obtener habitaciones: {e}')
        finally:
            conn.close()

def guardar_ticket(data, tipo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == 'habitacion':
                cursor.execute("""
                    INSERT INTO tickets_mantenimiento(habitacion, descripcion, prioridad, notas)
                    VALUES (?, ?, ?, ?)
                    """, (data))
            else:
                cursor.execute("""
                    INSERT INTO tickets_mantenimiento(area_hotel, descripcion, prioridad, notas)
                    VALUES (?, ?, ?, ?)
                    """, (data))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def descartar_ticket(razon, id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE tickets_mantenimiento
                SET estado = 'Descartado', fecha_inicio = date('now'), fecha_fin = date('now'),descripcion_solucion = ?
                WHERE id = ?
            """,(razon, id))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def ver_detalle_ticket(id):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM tickets_mantenimiento
            WHERE id = ?;
            """, (id,))
            resultado = cursor.fetchone()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener información: {e}')
        finally:
            conn.close()

def obtener_tecnicos():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM personal
            WHERE area_id = 2 AND estado = 'Activo'
            ORDER BY codigo;
            """)
            consulta = cursor.fetchall()
            resultado = []
            for empleado in consulta:
                resultado.append(f'{empleado[1]} - {empleado[2]} {empleado[3]}')
            return resultado
        except sql.Error as e:
            print(f'Error al obtener empleados: {e}')
        finally:
            conn.close() 

def asignar_ticket(datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE tickets_mantenimiento
                SET estado = 'Asignado', tecnico_id = ?, fecha_asignacion = date('now')
                WHERE id = ?
            """,(datos))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def estado_ticket(estado, id, solucion = None, notas = None):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if estado == "En Progreso":
                cursor.execute("""
                    UPDATE tickets_mantenimiento
                    SET estado = ?, fecha_inicio = date('now')
                    WHERE id = ?
                """,(estado, id))
            else:
                cursor.execute("""
                    UPDATE tickets_mantenimiento
                    SET estado = ?, fecha_fin = date('now'), descripcion_solucion = ?, notas = ?
                    WHERE id = ?
                """,(estado, solucion, notas, id))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def obtener_personal_activo():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT 
                p.codigo,
                p.nombre,
                p.apellido,
                p.puesto,
                a.nombre AS area_id,   -- muestra el nombre del área en lugar del ID
                p.estado,
                p.fecha_contratacion
            FROM personal p
            LEFT JOIN areas a ON p.area_id = a.id
            WHERE p.estado = 'Activo'
            ORDER BY p.codigo;
            """)
            consulta = cursor.fetchall()
            return consulta
        except sql.Error as e:
            print(f'Error al obtener empleados: {e}')
        finally:
            conn.close()

def buscar_empleado(texto, estado): #el query de consulta para buscar
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    p.codigo,
                    p.nombre,
                    p.apellido,
                    p.puesto,
                    a.nombre AS area_id,
                    p.estado,
                    p.fecha_contratacion
                FROM personal p
                LEFT JOIN areas a ON p.area_id = a.id
                WHERE (? = 'Activo' OR p.estado = ?)
                    AND (
                        p.codigo LIKE ?
                        OR p.nombre LIKE ?
                        OR p.apellido LIKE ?
                        OR p.puesto LIKE ?
                        OR a.nombre LIKE ?
                    )
                ORDER BY p.codigo;
            """, (estado, estado, f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%', f'%{texto}%'))
            
            resultado = cursor.fetchall()
            return resultado
        except sql.Error as e:
            print(f'Error al buscar: {e}')
        finally:
            conn.close()

def ver_detalle_empleado(codigo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM personal
            WHERE codigo = ?;
            """, (codigo,))
            resultado = cursor.fetchone()
            return resultado
        except sql.Error as e:
            print(f'Error al obtener información: {e}')
        finally:
            conn.close()

def generar_codigo_empleado():
    """
    Genera el siguiente código de empleado en secuencia con formato EMPNNN.
    Usa el mayor número actual extraído del sufijo numérico del campo 'codigo'.
    """
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            # Extrae el máximo valor numérico del sufijo (asumiendo formato EMP###)
            cursor.execute("SELECT MAX(CAST(substr(codigo,4) AS INTEGER)) FROM personal;")
            row = cursor.fetchone()
            max_num = row[0] if row and row[0] is not None else 0
            siguiente = int(max_num) + 1
            return f"EMP{siguiente:03d}"
        except sql.Error as e:
            print(f'Error generando codigo empleado: {e}')
            return None
        finally:
            conn.close()

def guardar_empleado(tipo, datos):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            if tipo == "agregar":
                cursor.execute("""
                    INSERT INTO personal
                    (codigo, nombre, apellido, puesto, area_id, salario_hora, fecha_contratacion, telefono, email, estado)
                    VALUES (?, ?, ?, ?, ?, ?, date('now'), ?, ?, 'Activo')
                """, (datos))
            else:
                cursor.execute("""
                    UPDATE personal
                    SET codigo = ?, nombre = ?, apellido = ?, puesto = ?, area_id = ?, salario_hora = ?, telefono = ?, email = ?
                    WHERE codigo = ?
                """, (*datos[:8], datos[0]))
            conn.commit()
            return True, "Empleado guardado exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar empleado: {e}"
        finally:
            conn.close()

def inactivar_empleado(codigo):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE personal
                SET estado = 'Inactivo', fecha_inactivacion = date('now')
                WHERE codigo = ?
                """,(codigo,))
            conn.commit()
            return True, "Datos insertados exitosamente"
        except sql.Error as e:
            return False, f"Error al guardar datos: {e}"
        finally:
            conn.close()

def obtener_cotizaciones_eventos():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM eventos ORDER BY fecha DESC')
        return cursor.fetchall()
    return []
    

def obtener_columnas_eventos():
    """Return list of column names in eventos table in order."""
    conn = conectar_bd()
    cols = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(eventos)")
            info = cursor.fetchall()
            cols = [c[1] for c in info]
        except sql.Error:
            cols = []
        finally:
            conn.close()
    return cols

def insertar_cotizacion_evento(tipo, salon, fecha, hora, equipamiento, categoria, personas, tarifa_salon, total, notas, hora_inicio=None, hora_fin=None, mesas_csv=None, asientos_totales=0, costo_mesas=0.0):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        # Determine which columns actually exist in the 'eventos' table to avoid INSERT errors on older DBs
        cursor.execute("PRAGMA table_info(eventos)")
        cols_info = cursor.fetchall()
        cols = [c[1] for c in cols_info]
        # base columns we always expect
        base_cols = ['tipo', 'salon', 'fecha', 'hora', 'equipamiento', 'categoria', 'personas', 'tarifa_salon', 'total', 'notas']
        insert_cols = []
        values = []
        for c in base_cols:
            if c in cols:
                insert_cols.append(c)
                values.append(locals()[c])
        # optional columns
        if 'hora_inicio' in cols:
            insert_cols.append('hora_inicio'); values.append(hora_inicio)
        if 'hora_fin' in cols:
            insert_cols.append('hora_fin'); values.append(hora_fin)
        if 'mesas_csv' in cols:
            insert_cols.append('mesas_csv'); values.append(mesas_csv)
        if 'asientos_totales' in cols:
            insert_cols.append('asientos_totales'); values.append(asientos_totales)
        if 'costo_mesas' in cols:
            insert_cols.append('costo_mesas'); values.append(costo_mesas)

        placeholders = ','.join(['?'] * len(insert_cols))
        sql = f"INSERT INTO eventos ({','.join(insert_cols)}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def eliminar_cotizacion_evento(id_):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM eventos WHERE id = ?', (id_,))
        conn.commit()
        conn.close()

def actualizar_cotizacion_evento(id_, tipo, salon, fecha, hora, equipamiento, categoria, personas, tarifa_salon, total, notas, hora_inicio=None, hora_fin=None, mesas_csv=None, asientos_totales=0, costo_mesas=0.0):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        # Determine which columns exist and build SET clause dynamically
        cursor.execute("PRAGMA table_info(eventos)")
        cols_info = cursor.fetchall()
        cols = [c[1] for c in cols_info]
        base_cols = ['tipo', 'salon', 'fecha', 'hora', 'equipamiento', 'categoria', 'personas', 'tarifa_salon', 'total', 'notas']
        set_parts = []
        values = []
        for c in base_cols:
            if c in cols:
                set_parts.append(f"{c} = ?")
                values.append(locals()[c])
        if 'hora_inicio' in cols:
            set_parts.append('hora_inicio = ?'); values.append(hora_inicio)
        if 'hora_fin' in cols:
            set_parts.append('hora_fin = ?'); values.append(hora_fin)
        if 'mesas_csv' in cols:
            set_parts.append('mesas_csv = ?'); values.append(mesas_csv)
        if 'asientos_totales' in cols:
            set_parts.append('asientos_totales = ?'); values.append(asientos_totales)
        if 'costo_mesas' in cols:
            set_parts.append('costo_mesas = ?'); values.append(costo_mesas)

        set_clause = ', '.join(set_parts)
        sql = f"UPDATE eventos SET {set_clause} WHERE id = ?"
        values.append(id_)
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

def obtener_dashboard_frontdesk():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        hoy = date.today().isoformat()
        try:
            cursor.execute("SELECT COUNT(*) FROM checkins_checkouts WHERE tipo='checkin' AND date(fecha_hora) = ?", (hoy,))
            checkins = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM checkins_checkouts WHERE tipo='checkout' AND date(fecha_hora) = ?", (hoy,))
            checkouts = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE estado='Ocupada'")
            ocupadas = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(monto) FROM ingresos WHERE date(fecha_pago) = ?", (hoy,))
            ingresos = cursor.fetchone()[0] or 0.0
        finally:
            conn.close()
        return checkins, checkouts, ocupadas, ingresos
    return 0, 0, 0, 0.0 # Default values if conn is None



def buscar_reserva_frontdesk(query):
    conn = conectar_bd()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.id, c.nombres || ' ' || c.apellidos as cliente_nombre, r.numero_hab,
                   r.fecha_entrada, r.fecha_salida, r.monto_pago, r.estado
            FROM reservas r
            JOIN clientes c ON r.id_cliente = c.id
            WHERE (r.id LIKE ? OR c.nombres LIKE ? OR c.apellidos LIKE ? OR r.numero_hab LIKE ?)
            AND r.estado = 'Pendiente'
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

def registrar_checkin(reserva_id):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("SELECT numero_hab FROM reservas WHERE id=?", (reserva_id,))
        hab = cur.fetchone()
        if not hab:
            raise Exception("Reserva no encontrada")
        numero_hab = hab['numero_hab']

        cur.execute("UPDATE reservas SET estado='checked-in', checked_in=1 WHERE id=?", (reserva_id,))
        cur.execute("UPDATE habitaciones SET estado='Ocupada' WHERE numero=?", (numero_hab,))
        cur.execute("INSERT INTO checkins_checkouts (reserva_id, tipo) VALUES (?, 'checkin')", (reserva_id,))
        conn.commit()
    finally:
        conn.close()

def registrar_early_checkin(reserva_id, monto_cargo):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        registrar_checkin(reserva_id)
        cur.execute("""
            INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago, notas)
            VALUES (?, ?, ?, ?, ?)
        """, ('costo_adicional_checkout', 'Early Check-in', monto_cargo, 'efectivo', f'Reserva ID: {reserva_id}'))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def buscar_habitaciones_disponibles(fecha_entrada, fecha_salida, tipo_hab):
    conn = conectar_bd()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT h.numero, t.nombre as tipo_nombre, t.precio_base
            FROM habitaciones h
            JOIN tipos_habitacion t ON h.tipo_id = t.id
            WHERE t.nombre = ? AND h.estado = 'Disponible' AND h.numero NOT IN (
                SELECT numero_hab FROM reservas
                WHERE fecha_salida > ? AND fecha_entrada < ? AND estado != 'Cancelada'
            )
        """, (tipo_hab, fecha_entrada, fecha_salida))
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def registrar_walkin(nombre, email, f_entrada, f_salida, personas, monto, num_hab):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        # Buscar cliente por email
        cur.execute("SELECT id FROM clientes WHERE email = ?", (email,))
        row = cur.fetchone()
        if row:
            id_cliente = row['id']
        else:
            # Crear cliente genérico
            cur.execute("""
                INSERT INTO clientes (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email)
                VALUES (?, '', 'Otro', '', date('now'), '', '', '', ?)
            """, (nombre, email))
            id_cliente = cur.lastrowid

        # Registrar el ingreso
        cur.execute("INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago) VALUES (?,?,?,?)",
                    ('walk_in', f'Walk-in Hab {num_hab}', monto, 'efectivo'))
        pago_id = cur.lastrowid

        # Insertar en reservas
        cur.execute("""
            INSERT INTO reservas (
                numero_hab, tipo_habitacion, id_cliente, cliente_nombre, cliente_email,
                fecha_entrada, fecha_salida, total_personas, id_pago, monto_pago,
                checked_in, checked_out, estado, es_walkin
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 'En curso', 1)
        """, (
            num_hab, 'Walk-in', id_cliente, nombre, email,
            f_entrada, f_salida, personas, pago_id, monto
        ))
        reserva_id = cur.lastrowid

        # Actualizar estado de la habitación
        cur.execute("UPDATE habitaciones SET estado='Ocupada' WHERE numero=?", (num_hab,))
        # Registrar el check-in
        cur.execute("INSERT INTO checkins_checkouts (reserva_id, tipo) VALUES (?, 'checkin')", (reserva_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def agregar_cargo_checkout(reserva_id, concepto, descripcion, monto):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO ingresos (tipo_ingreso, concepto, monto, metodo_pago, notas)
            VALUES (?, ?, ?, ?, ?)
        """, ('costo_adicional_checkout', concepto, monto, 'efectivo', f'Reserva ID: {reserva_id} - {descripcion}'))
        conn.commit()
    finally:
        conn.close()


def extender_estadia(reserva_id, nueva_salida):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("SELECT fecha_salida, monto_pago, numero_hab FROM reservas WHERE id=?", (reserva_id,))
        res = cur.fetchone()
        if not res:
            raise Exception("Reserva no encontrada para extender.")

        fecha_salida_actual = validar_fecha(res['fecha_salida'])
        fecha_nueva_salida = validar_fecha(nueva_salida)

        if not fecha_salida_actual or not fecha_nueva_salida:
            raise Exception("Fechas inválidas para calcular la extensión.")

        dias_actuales = (fecha_salida_actual - date.today()).days
        dias_nuevos = (fecha_nueva_salida - fecha_salida_actual).days
        
        if dias_nuevos <= 0:
            raise Exception("La nueva fecha de salida debe ser posterior a la actual.")

        precio_noche = res['monto_pago'] / dias_actuales if dias_actuales > 0 else 50
        monto_adicional = dias_nuevos * precio_noche
        cur.execute("UPDATE reservas SET fecha_salida=?, monto_pago=monto_pago+? WHERE id=?", (nueva_salida, monto_adicional, reserva_id))
        agregar_cargo_checkout(reserva_id, "Extensión de estadía", f"{dias_nuevos} noches adicionales", monto_adicional)
        conn.commit()
    finally:
        conn.close()


def registrar_checkout(reserva_id):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("SELECT numero_hab FROM reservas WHERE id=?", (reserva_id,))
        hab = cur.fetchone()
        if not hab:
            raise Exception("Reserva no encontrada")
        numero_hab = hab['numero_hab']
        cur.execute("UPDATE reservas SET estado='Completada', checked_out=1 WHERE id=?", (reserva_id,))
        cur.execute("UPDATE habitaciones SET estado='Sucia' WHERE numero=?", (numero_hab,))
        cur.execute("INSERT INTO checkins_checkouts (reserva_id, tipo) VALUES (?, 'checkout')", (reserva_id,))
        conn.commit()
    finally:
        conn.close()


def registrar_late_checkout(reserva_id, monto_cargo):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        agregar_cargo_checkout(reserva_id, "Late Check-Out", "Cargo por salida tardía", monto_cargo)
        # No se hace el checkout aquí, solo se agrega el cargo. El checkout se confirma por separado.
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def obtener_total_deuda(reserva_id):
    conn = conectar_bd()
    if not conn:
        return 0.0
    cur = conn.cursor()
    total_deuda = 0.0
    try:
        # Obtener el monto original de la reserva
        cur.execute("SELECT monto_pago FROM reservas WHERE id=?", (reserva_id,))
        res = cur.fetchone()
        if res and res['monto_pago']:
            total_deuda += float(res['monto_pago'])

        # Sumar todos los cargos adicionales
        cur.execute("SELECT SUM(monto) FROM ingresos WHERE tipo_ingreso='costo_adicional_checkout' AND notas LIKE ?", (f'%Reserva ID: {reserva_id}%',))
        cargos = cur.fetchone()
        if cargos and cargos[0]:
            total_deuda += float(cargos[0])
            
    except Exception as e:
        print(f"Error al calcular la deuda total: {e}")
    finally:
        conn.close()
    return total_deuda

def registrar_early_checkout(reserva_id):
    conn = conectar_bd()
    if not conn:
        raise Exception("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        cur.execute("SELECT numero_hab FROM reservas WHERE id=?", (reserva_id,))
        hab = cur.fetchone()
        if not hab:
            raise Exception("Reserva no encontrada")
        numero_hab = hab['numero_hab']
        cur.execute("UPDATE reservas SET estado='Completada', checked_out=1 WHERE id=?", (reserva_id,))
        cur.execute("UPDATE habitaciones SET estado='Sucia' WHERE numero=?", (numero_hab,))
        cur.execute("INSERT INTO checkins_checkouts (reserva_id, tipo) VALUES (?, 'checkout_anticipado')", (reserva_id,))
        conn.commit()
    finally:
        conn.close()

