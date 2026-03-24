/* CREA VISTAS PARA BD: cobranzas_capa_dos
   El propósito es aislar los datos para consumo, de la base principal de ingesta y transformaciones.
   Las vistas se crean en base a la lógica del negocio, dejando solo los campos relevantes para su análisis,
   y agrupando algunas tabla de dimensiones para simplificar el modelado
*/

/* Vista fact_cobranzas
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_fact_cobranzas;
CREATE VIEW cobranzas_capa_dos.vista_fact_cobranzas AS
	SELECT 
		asesor,
        contrato,
        comision,
        valor_neto,
        porcentaje_comision AS porc_liquidado_comision,
        fecha_operacion AS 'fecha_cobro',
        CASE WHEN forma_pago = 'efe' THEN 'efectivo'
			 WHEN forma_pago = 'transf' THEN 'transferencia'
             WHEN forma_pago = 'tc' THEN 'tarejeta de credito'
             ELSE 'no disponible'
		END AS medio_de_pago
	FROM cobranzas_capa_uno.fact_cobranzas;

/* Vista dim_contratos
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_contratos ;
CREATE VIEW cobranzas_capa_dos.vista_dim_contratos AS
	SELECT 
		dc.id_contrato,
		dc.id_cliente,
		de.especialidad,
		de.rama,
		de.com_broker AS 'comision_broker',
		de.com_asesor AS 'comision_asesor'
	FROM cobranzas_capa_uno.dim_contratos dc
	LEFT JOIN cobranzas_capa_uno.dim_especialidad de ON dc.id_especialidad = de.id_especialidad;

/* Vista dim_clientes
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_clientes ;
CREATE VIEW cobranzas_capa_dos.vista_dim_clientes AS
	SELECT 
		id_cliente,
		nombre_cliente,
		id_ciudad
	FROM cobranzas_capa_uno.dim_clientes;
    
-- vista ciudad
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_ciudad ;
CREATE VIEW cobranzas_capa_dos.vista_dim_ciudad AS
	SELECT 
		dc.id_ciudad,
		dc.nombre_ciudad AS 'ciudad',
		dp.nombre_provincia AS 'provincia'
	FROM cobranzas_capa_uno.dim_ciudad dc
    LEFT JOIN cobranzas_capa_uno.dim_provincia dp ON dc.id_provincia = dp.id_provincia;

/* Vista dim_comercial
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_comercial ;
CREATE VIEW cobranzas_capa_dos.vista_dim_comercial AS
	SELECT 
		id_comercial,
		nombre_comercial,
		tipo_comercial,
        id_ciudad
	FROM cobranzas_capa_uno.dim_comercial;
    
