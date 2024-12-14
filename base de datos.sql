-- 1. Crear la base de datos
CREATE DATABASE TallerMecanico;
USE TallerMecanico;

-- 2. Crear la tabla principal
CREATE TABLE GestionTaller (
    ID INT AUTO_INCREMENT PRIMARY KEY,         -- Identificador único
    ClienteNombre VARCHAR(100) NOT NULL,       -- Nombre del cliente
    ClienteTelefono VARCHAR(15),               -- Teléfono del cliente
    VehiculoModelo VARCHAR(50),                -- Modelo del vehículo
    VehiculoPlaca VARCHAR(15),                 -- Placa del vehículo
    ServicioTipo VARCHAR(50),                  -- Tipo de servicio o reparación
    EstadoServicio ENUM('Pendiente', 'En Proceso', 'Completado') DEFAULT 'Pendiente', -- Estado del servicio
    FechaIngreso DATE,                         -- Fecha de ingreso del vehículo
    FechaEntrega DATE,                         -- Fecha programada para entrega
    InventarioRepuesto VARCHAR(100),           -- Repuesto utilizado (si aplica)
    CantidadRepuesto INT,                      -- Cantidad de repuestos utilizados
    CostoServicio DECIMAL(10,2),               -- Costo del servicio o reparación
    Notas TEXT,                                -- Notas adicionales o descripción
    RecordatorioMantenimiento DATE,            -- Fecha de recordatorio para mantenimiento futuro
    FechaActualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Registro de cambios
);


--procedimientos almacenados

DELIMITER //
CREATE PROCEDURE RegistrarNuevoVehiculo(
    IN p_ClienteNombre VARCHAR(100),
    IN p_ClienteTelefono VARCHAR(15),
    IN p_VehiculoModelo VARCHAR(50),
    IN p_VehiculoPlaca VARCHAR(15),
    IN p_ServicioTipo VARCHAR(50),
    IN p_FechaIngreso DATE,
    IN p_FechaEntrega DATE,
    IN p_Notas TEXT
)
BEGIN
    INSERT INTO GestionTaller (
        ClienteNombre, ClienteTelefono, VehiculoModelo, VehiculoPlaca, ServicioTipo, EstadoServicio, FechaIngreso, FechaEntrega, Notas
    )
    VALUES (
        p_ClienteNombre, p_ClienteTelefono, p_VehiculoModelo, p_VehiculoPlaca, p_ServicioTipo, 'Pendiente', p_FechaIngreso, p_FechaEntrega, p_Notas
    );
END //
DELIMITER ;

CALL RegistrarNuevoVehiculo(
    'Juan Pérez', '555-1234', 'Toyota Corolla', 'XYZ-123', 'Cambio de aceite', '2024-12-15', '2024-12-16', 'Sin notas'
);



DELIMITER //
CREATE PROCEDURE ProgramarServicio(
    IN p_VehiculoPlaca VARCHAR(15),
    IN p_ServicioTipo VARCHAR(50),
    IN p_FechaIngreso DATE,
    IN p_FechaEntrega DATE
)
BEGIN
    UPDATE GestionTaller
    SET ServicioTipo = p_ServicioTipo,
        EstadoServicio = 'Pendiente',
        FechaIngreso = p_FechaIngreso,
        FechaEntrega = p_FechaEntrega
    WHERE VehiculoPlaca = p_VehiculoPlaca;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE ControlReparaciones(
    IN p_VehiculoPlaca VARCHAR(15),
    IN p_EstadoServicio ENUM('Pendiente', 'En Proceso', 'Completado'),
    IN p_InventarioRepuesto VARCHAR(100),
    IN p_CantidadRepuesto INT
)
BEGIN
    UPDATE GestionTaller
    SET EstadoServicio = p_EstadoServicio,
        InventarioRepuesto = p_InventarioRepuesto,
        CantidadRepuesto = p_CantidadRepuesto
    WHERE VehiculoPlaca = p_VehiculoPlaca;
END //
DELIMITER ;



    IN p_VehiculoPlaca VARCHAR(15),
    IN p_NotasGarantia TEXT
)
BEGIN
    UPDATE GestionTaller
    SET Notas = CONCAT(Notas, '\nGarantía: ', p_NotasGarantia),
        EstadoServicio = 'Garantizado'
    WHERE VehiculoPlaca = p_VehiculoPlaca;
END //
DELIMITER ;


