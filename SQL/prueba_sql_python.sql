CREATE DATABASE prueba_script; 
CREATE TABLE prueba_script.tabla_prueba (
id_cobro int not null auto_increment, -- es PK autoincremental
periodo varchar(10),
ultimo_update DATETIME DEFAULT CURRENT_TIMESTAMP, # se incorpora para tracking de registros
PRIMARY KEY (id_cobro)
); 
INSERT INTO prueba_script.tabla_prueba (id_cobro, periodo)
values
	(1,'202501'),
    (2,'202502'),
    (3,'202503'),
    (4,'202504'),
    (5,'202505');
