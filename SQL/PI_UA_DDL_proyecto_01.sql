/* ================================================
CREACION DE BASE DE DATOS Y DEFINICION DE ESCHEMAS
===================================================
*/

/* 
1 - Crea base de datos capa uno (ingesta sin transformaciones)
*/
CREATE DATABASE IF NOT EXISTS cobranzas_capa_uno; 

/* 
2 - Crea tabla para estacionamiento de datos ingestados, previo a carga en tabla fact_cobranzas.
	Esta tabla se sobreescribe con cada ingesta (truncate + insert) desde script python
*/

DROP TABLE IF EXISTS cobranzas_capa_uno.temp_cobranzas;

CREATE TABLE cobranzas_capa_uno.temp_cobranzas (
id_cobro int not null auto_increment, -- es PK autoincremental
periodo varchar(10),
asesor varchar(10),
fecha_operacion date,
contrato varchar(50),
comision float,
valor_neto float,
porcentaje_comision float,
forma_pago varchar(10),
numero_recibo varchar(20),
ultimo_update DATETIME DEFAULT CURRENT_TIMESTAMP, # se incorpora para tracking de registros
PRIMARY KEY (id_cobro)
); 

/* 
3 - Crea tabla de hechos fact_cobranzas
*/
DROP TABLE IF EXISTS cobranzas_capa_uno.fact_cobranzas;

CREATE TABLE cobranzas_capa_uno.fact_cobranzas (
id_cobro int not null auto_increment, -- es PK autoincremental
periodo varchar(10),
asesor varchar(10),
fecha_operacion date,
contrato varchar(50),
comision float,
valor_neto float,
porcentaje_comision float,
forma_pago varchar(10),
numero_recibo varchar(20),
ultimo_update DATETIME DEFAULT CURRENT_TIMESTAMP, # se incorpora para tracking de registros
PRIMARY KEY (id_cobro)
);

/* 
4 - Crea tablas que dimensionan fact_cobranzas
*/


-- =================================================
-- pureba insertar ciertas columnas en tabla fact
-- incorporar que verifique el periodo antes de insertar
-- ver de incorporar un truncate + insert tambien en tabla fact_cobranzas

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
