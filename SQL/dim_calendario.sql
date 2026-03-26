

/* dim_calendario
*/
CREATE TABLE IF NOT EXISTS cobranzas_capa_uno.dim_calendario (
    fecha DATE PRIMARY KEY,
    anio INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes VARCHAR(15) NOT NULL,
    mes_corto CHAR(3) NOT NULL,
    dia INT NOT NULL,
    dia_semana INT NOT NULL, -- 1 para Lunes, 7 para Domingo
    nombre_dia VARCHAR(15) NOT NULL,
    trimestre INT NOT NULL,
    es_fin_de_semana BOOLEAN NOT NULL,
    -- Útil para ordenar meses cronológicamente y no alfabéticamente
    mes_id INT NOT NULL -- Ejemplo: 202603
);

DELIMITER //

CREATE PROCEDURE cobranzas_capa_uno.llenar_calendario(IN fecha_inicio DATE, IN fecha_fin DATE)
BEGIN
    DECLARE fecha_actual DATE;
    SET fecha_actual = fecha_inicio;
    
    WHILE fecha_actual <= fecha_fin DO
        INSERT INTO cobranzas_capa_uno.dim_calendario (
            fecha, anio, mes, nombre_mes, mes_corto, dia, 
            dia_semana, nombre_dia, trimestre, es_fin_de_semana, mes_id
        ) VALUES (
            fecha_actual,
            YEAR(fecha_actual),
            MONTH(fecha_actual),
            MONTHNAME(fecha_actual),
            LEFT(MONTHNAME(fecha_actual), 3),
            DAY(fecha_actual),
            WEEKDAY(fecha_actual) + 1,
            DAYNAME(fecha_actual),
            QUARTER(fecha_actual),
            IF(WEEKDAY(fecha_actual) IN (5, 6), 1, 0),
            (YEAR(fecha_actual) * 100) + MONTH(fecha_actual)
        );
        SET fecha_actual = DATE_ADD(fecha_actual, INTERVAL 1 DAY);
    END WHILE;
END //

DELIMITER ;

-- Ejecutar para generar 10 años de fechas
CALL cobranzas_capa_uno.llenar_calendario('2020-01-01', '2030-12-31');

DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_calendario;
CREATE VIEW cobranzas_capa_dos.vista_dim_calendario AS
	select
		fecha,
        anio,
        mes as num_mes,
        nombre_mes,
        mes_corto,
        dia as num_dia,
        nombre_dia,
        trimestre as num_trimestre,
        mes_id        
    from cobranzas_capa_uno.dim_calendario;
