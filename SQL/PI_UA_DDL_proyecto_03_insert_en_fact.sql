insert into cobranzas_capa_uno.fact_cobranzas (	
	periodo, 
	asesor, 
	fecha_operacion, 
	contrato, 
	comision, 
	valor_neto, 
	porcentaje_comision, 
	forma_pago, 
	numero_recibo)
(select 
	periodo,
	asesor,
	fecha_operacion,
	contrato,
	comision,
	valor_neto,
	porcentaje_comision,
	forma_pago,
	numero_recibo
from cobranzas_capa_uno.temp_cobranzas
    );

select * from cobranzas_capa_uno.temp_cobranzas limit 10;
select count(*) from cobranzas_capa_uno.temp_cobranzas;