create database prueba; 

create table prueba.tabla_prueba (
id int,
campo_1 char(5),
campo_2 char(5)
); 

insert into prueba.tabla_prueba (id, campo_1, campo_2)
values 
(1, 'hola', 'mundo'),
(2, 'chau', 'mundo'),
(3, 'volvi', 'mundo');

create database prueba_dos; 

create table prueba_dos.tabla_prueba_dos (
id int,
campo_1 char(5)
); 

insert into prueba_dos.tabla_prueba_dos (id, campo_1)
(select 
	id ,
    campo_1
from prueba.tabla_prueba);

select	*
from prueba_dos.tabla_prueba_dos;

select * from prueba.tabla_prueba;