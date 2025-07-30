-- SQLite
-- Query por si se me borra la tabla "cliente"
CREATE TABLE IF NOT EXISTS cliente(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    tipo_doc TEXT NOT NULL,
    numero_doc TEXT NOT NULL UNIQUE,
    fecha_nac DATE,
    genero TEXT,
    nacionalidad TEXT,
    telefono TEXT,
    email TEXT UNIQUE
);

INSERT INTO cliente (nombres, apellidos, tipo_doc, numero_doc, fecha_nac, genero, nacionalidad, telefono, email) VALUES
('Juan Carlos', 'Ramírez López', 'Cédula', '00112345678', '1985-07-14', 'Masculino', 'Dominicana', '8095551234', 'juanc.ramirez@example.com'),
('María Elena', 'Pérez Díaz', 'Pasaporte', 'PA1234567', '1990-03-22', 'Femenino', 'Colombiana', '8295552345', 'maria.perez@example.com'),
('Carlos Eduardo', 'Gómez Batista', 'Cédula', '00187654321', '1978-12-05', 'Masculino', 'Dominicana', '8095553456', 'carlos.gomez@example.com'),
('Ana Patricia', 'Martínez Peña', 'Cédula', '00145678901', '1995-06-18', 'Femenino', 'Dominicana', '8495554567', 'ana.martinez@example.com'),
('Luis Alberto', 'Fernández Soto', 'Pasaporte', 'PA7654321', '1982-09-30', 'Masculino', 'Mexicana', '8095555678', 'luis.fernandez@example.com'),
('Laura Isabel', 'Santos Herrera', 'Cédula', '00123456789', '1993-01-10', 'Femenino', 'Dominicana', '8295556789', 'laura.santos@example.com'),
('Pedro José', 'Castillo Vargas', 'Cédula', '00134567890', '1988-11-25', 'Masculino', 'Dominicana', '8095557890', 'pedro.castillo@example.com'),
('Rosa María', 'Herrera Báez', 'Pasaporte', 'PA3456789', '1991-04-08', 'Femenino', 'Venezolana', '8495558901', 'rosa.herrera@example.com'),
('José Manuel', 'Morales Jiménez', 'Cédula', '00156789012', '1980-08-15', 'Masculino', 'Dominicana', '8095559012', 'jose.morales@example.com'),
('Isabel Cristina', 'Almonte Ramírez', 'Cédula', '00167890123', '1994-05-27', 'Femenino', 'Dominicana', '8295550123', 'isabel.almonte@example.com'),
('Francisco Javier', 'Peña Rodríguez', 'Pasaporte', 'PA4567890', '1975-02-03', 'Masculino', 'Española', '8495551230', 'francisco.pena@example.com'),
('Carmen Luisa', 'López García', 'Cédula', '00178901234', '1996-12-12', 'Femenino', 'Dominicana', '8095552340', 'carmen.lopez@example.com'),
('Miguel Ángel', 'Reyes Cabrera', 'Cédula', '00189012345', '1987-10-09', 'Masculino', 'Dominicana', '8295553450', 'miguel.reyes@example.com'),
('Patricia Beatriz', 'García Mendoza', 'Pasaporte', 'PA5678901', '1992-07-19', 'Femenino', 'Argentina', '8495554560', 'patricia.garcia@example.com'),
('Ricardo Andrés', 'Méndez Rivera', 'Cédula', '00190123456', '1983-03-01', 'Masculino', 'Dominicana', '8095555670', 'ricardo.mendez@example.com'),
('Yolanda Esther', 'Jiménez Paredes', 'Cédula', '00201234567', '1997-11-16', 'Femenino', 'Dominicana', '8295556780', 'yolanda.jimenez@example.com'),
('Fernando Luis', 'Núñez Castillo', 'Pasaporte', 'PA6789012', '1981-06-23', 'Masculino', 'Costarricense', '8495557890', 'fernando.nunez@example.com'),
('Luisa Fernanda', 'De la Cruz Mejía', 'Cédula', '00212345678', '1990-02-28', 'Femenino', 'Dominicana', '8095558900', 'luisa.delacruz@example.com'),
('Andrés Felipe', 'Rojas Matos', 'Cédula', '00223456789', '1989-01-17', 'Masculino', 'Dominicana', '8295559010', 'andres.rojas@example.com'),
('Natalia Sofía', 'Tejada Liriano', 'Pasaporte', 'PA7890123', '1998-08-04', 'Femenino', 'Panameña', '8495550120', 'natalia.tejada@example.com');
