# Pipeline para Análisis y Control de Cobranzas

Proyecto Integrador presentado en el marco del BootCamp de Data Analyst Full Program otorgado por Unicorn Academy [https://unicornacademy.es/](https://unicornacademy.es/)
<hr />

## 🎙️ Presentación
Este proyecto pretende exponer como una problemática real y concreta relacionada con la manipulación de datos que enfrenta una empresa en el desarrollo de sus operaciones habituales, puede ser resuelta satisfactoriamente combinando con buen criterio la gestión de flujo de trabajo y el empleo de herramientas adecuadas.
<hr />

## ❌ Problemática

Una compañía percibe sus ingresos por comisiones sobre cobranzas realizadas, sin realizar controles sobre la correcta liquidación de esas comisiones. Esto se debe a que la fuente de datos consiste en varios archivos excel sin formato tabular limpio, de un tamaño que tornan difícil su manipulación manual con herramientas convencionales y que a su vez requieren tareas de limpieza complejas.
<hr />

## 💡 Propuesta

Dar solución a la problemática planteada a partir de la orquestación de un pipeline de ETL end-to-end de datos en python que recorra un directorio específico (para este proyecto es este repositorio), lea y recupere todos los archivos dentro del mismo, los manipule para unificar todo en un solo dataframe final. Luego, ejecutar varios scripts SQL para definir la estructura de la Base de Datos en MySQL, ingestar el dataframe en una tabla utilizada como “landing”, mover los datos dentro del DWH emulando una arquitectura medallion para que finalicen en vistas accesibles. Por último conectar Power BI a la BD para consumir esos datos y visualizarlos.
<hr />

## 🛠️ Stack Tecnológico - Requisitos Previos
- [x] **Windows** (orquestación diseñada para este OS).
- [x] **Python 3.9+** (se recomienda el uso de Anaconda).
- [x] **MySQL Server 8.0+** y **Connector/NET** (funcionando localmente) .
- [x] **Power BI Desktop** (visualización final).
<hr />

## ⚠️ Ejecución: 
> [!IMPORTANT]  
> Siga estos pasos para reproducir el pipeline en su entorno local:

1. Descargue todos los archivos dentro de ‘**Descargas**’ en el mismo directorio local
2. Modifique el archivo ‘.env.example’con sus credenciales de MySQL, y luego renombre el archivo a ‘**.env**’
3. Abra su editor (Jupyter Notebook, VS Code).
4. Ejecute el archivo ‘**PI_UA_orquestador.ipynb**’.
5. El script validará la conexión, procesará los datos e informará el avance. 
6. Al terminar el proceso, se da inicio a la plantilla de Power BI para visualizar los resultados.
<hr />

## 🖊️ Autor
Marcelo F. Martin - Contador Público & Analista de Datos
