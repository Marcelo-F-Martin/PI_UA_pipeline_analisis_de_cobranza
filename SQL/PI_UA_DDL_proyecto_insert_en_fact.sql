/* INGESTA EN TABLA DE HECHOS
	Mueve datos de tabla temporal a tabla principal
*/
DELETE FROM cobranzas_capa_uno.fact_cobranzas 
WHERE periodo IN (SELECT DISTINCT periodo FROM cobranzas_capa_uno.temp_cobranzas);
INSERT INTO cobranzas_capa_uno.fact_cobranzas 
	(periodo, 
	asesor, 
	fecha_operacion, 
	contrato, 
	comision, 
	valor_neto, 
	porcentaje_comision, 
	forma_pago, 
	numero_recibo)
	(SELECT 
		periodo,
		asesor,
		fecha_operacion,
		contrato,
		comision,
		valor_neto,
		porcentaje_comision,
		forma_pago,
		numero_recibo
	FROM cobranzas_capa_uno.temp_cobranzas
	);
