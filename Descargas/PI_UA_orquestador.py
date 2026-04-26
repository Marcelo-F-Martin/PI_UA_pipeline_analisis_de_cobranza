#!/usr/bin/env python
# coding: utf-8

# # ORQUESTACION - PIPELINE ANALISIS DE COBRANZAS
# ## Preparación del entorno

# In[ ]:


import os


# In[ ]:


# Instalación de dependencias

archivo_de_librerias = "requeriments.txt"
if os.path.exists(archivo_de_librerias):
    print(f"📦 Verificando dependencias desde {archivo_de_librerias}...")
    get_ipython().run_line_magic('pip', 'install --quiet -r {archivo_de_librerias}')
    print("✅ Todas las librerías necesarias están listas.")
else:
    print(f"⚠️ No se encontró {archivo_de_librerias}. Asegúrate de tener las librerías especificadas en 'requeriments.txt' instaladas.")


# In[ ]:


import pandas as pd
import requests
import io
import unicodedata #para manejo de tildes
from sqlalchemy import create_engine, text
import getpass #para manejo de password seguro en conexion a Mysql
import pymysql
from pymysql.constants import CLIENT
from dotenv import load_dotenv


# In[ ]:


# Conexión a repo GitHub

usuario = "Marcelo-F-Martin"
repo = "PI_UA_pipeline_analisis_de_cobranza"

# URL de la API para acceder al último release donde se alojan los archivos en crudo.
api_url = f"https://api.github.com/repos/{usuario}/{repo}/releases/latest"

respuesta = requests.get(api_url)
print('======================================================')
print('✅ Conexión Exitosa al Repositorio!') if respuesta.status_code == 200 else print(f' ✖️ Verificar Conexion al Repo. Código Devuelto: {respuesta.status_code}')
print('======================================================')
archivos_crudos = respuesta.json().get('assets', []) # El segundo argumento [] del .get(), es para que no rompa el codigo si la llave 'assets' no existe.


# ## Inicio proceso ETL
# ### 1- Extracción:
# #####   Obtención de datos crudos desde la fuente y almacenamiento en Dataframe de Pandas

# In[ ]:


df_definitivo_por_libro = []   
total_registros = 0

#====== INICIO bucle externo: recorre archivos dentro del directorio ===============================
for archivo in archivos_crudos:

    # Filtrado para leer solo archivos .xls
    if archivo['name'].endswith('.xls'):
        print(f"Nombre de archivo encontrado: {archivo['name']}")
        print('----------------------------------------------------------------------')

    # lista para incorporar los df por cada hoja de cada libro.
    hojas_consolidadas_por_libro = [] 

    url_archivo = archivo['browser_download_url']
    respuesta_url_archivo = requests.get(url_archivo).content
    archivo = pd.read_excel(io.BytesIO(respuesta_url_archivo), engine='xlrd', sheet_name=None, header=None)

    #====== INICIO bucle interno: recorre hojas del archivo =======================================

        # se considera "df_crudo" a cada hoja sin procesar de un libro ".xls"
    for nombre_hoja, df_crudo in archivo.items():
        print(f" ✅ Hoja '{nombre_hoja}' leída correctamente.")

        #--------- Fragmento para obtener el df_limpio de cada hoja --------
        encabezado_clave = "Periodo"

        indice_encabezado_fila = df_crudo[df_crudo.apply(lambda row: encabezado_clave in row.astype(str).values, axis=1)].index

        if not indice_encabezado_fila.start == 0:

            fila_inicio = indice_encabezado_fila[0]

            print(f"  ✅ Encabezado clave '{encabezado_clave}' encontrado en la Fila: {fila_inicio}")

            fila_encabezado = df_crudo.iloc[fila_inicio]

            col_inicio = fila_encabezado[fila_encabezado.astype(str) == encabezado_clave].index[0]

            df_crudo.columns = df_crudo.iloc[fila_inicio] # Asignar la fila encontrada como nuevo encabezado

            df_limpio = df_crudo[fila_inicio + 1:].reset_index(drop=True) # Eliminar filas superiores haciendo un slicing del df_crudo

            #---------- Fin Fragmento -------------------------------------------

            df_final_hoja = df_limpio.copy()

            df_final_hoja['hoja_origen'] = nombre_hoja # Columna para identificar a quien corresponde la comisión (si al broker o a los asesores)

        else:
            print(f"   ✖️ Encabezado Clave NO encontrado en hoja: {nombre_hoja}. ")
            continue

        if not df_final_hoja.empty:
            hojas_consolidadas_por_libro.append(df_final_hoja)
            print(f"   ✅ DataFrame de Hoja '{nombre_hoja}' incorporada al listado. Registros: {len(df_final_hoja)}\n")

            total_registros += len(df_final_hoja)
        else:
            print(f"  Advertencia: Hoja '{nombre_hoja}' vacía después de la limpieza. No se añadió.")

    if not hojas_consolidadas_por_libro == []:

        df_archivo_unificado = pd.concat(hojas_consolidadas_por_libro, ignore_index=True)
        df_definitivo_por_libro.append(df_archivo_unificado)

    else:
        print('    ❌ No se consolidaron hojas para este archivo excel. \n')

    #====== FIN bucle interno =================================================
#====== FIN bucle externo ====================================================

# Concatenación final
if not df_definitivo_por_libro == []:
    df_final = pd.concat(df_definitivo_por_libro, ignore_index=True)
    print('======================================================')
    print(f'📝 Suma de Registros del total de hojas: {total_registros}')
    print(f'📝 Total de Registros del df_final concatenado: {len(df_final)}')
    print('======================================================')
else:
    print('======================================================')
    print(' ⚠️ No se han generado dataframes para los archivos excel leídos. ')
    print('======================================================')



# ### 2- Transformación

# In[ ]:


df_final.info()


# In[ ]:


def limpiar_tilde(texto):
    # 1. Normaliza el texto a la forma NFD (Descomposición)
    # Esto separa la 'á' en 'a' + 'tilde combinable'
    texto_normalizado = unicodedata.normalize('NFD', texto)

    # 2. Filtra y mantiene solo los caracteres que no sean "marcas" de acento (Mn)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )

    return texto_sin_acentos


# In[ ]:


# 1_estandariza a minusculas
# 2_elimina espacios en blanco
# 3_reemplaza vacíos por '_'
# 4_aplica función definida para limpiar tildes

df_final.columns = df_final.columns.str.lower().str.strip().str.replace(' ','_')
df_final.columns = [limpiar_tilde(col) for col in df_final.columns]
df_final.columns


# In[ ]:


# seleccion de columnas relevantes a importar a la Base de Datos

lista_columnas_seleccionadas = ['periodo','asesor','fecha_operacion','contrato','comision', 'valor_neto', 'porcentaje_comision','forma_pago', 'numero_recibo', 'hoja_origen'  ]
df_final = df_final[lista_columnas_seleccionadas]


# In[ ]:


# Verifica existencia de PK

df_final.nunique()


# In[ ]:


df_final_limpio = df_final.copy()
df_final_limpio.info()


# ### 3- Carga
# #### Opción para descargar dataframe "df_limpio_final" en formato .csv

# In[ ]:


# Función para exportar archivo en formato .CSV al directorio local.

def guardar_archivo():
    try:
        ingreso_ruta = input('Copie y pegue el directorio donde guardar el archivo .CSV: ')
        ruta_archivo = f"{ingreso_ruta}"
        nombre_csv_salida = "comisiones_consolidadas.csv"
        ruta_salida_completa = os.path.join(ruta_archivo, nombre_csv_salida)
        df_final_limpio.to_csv(ruta_salida_completa, index=False, encoding='utf-8')
        mensaje = print('✅ ¡Archivo guardado exitosamente!')

    except Exception as e:
        mensaje = print('⚠️ No se pudo guardar el archivo por el siguiente error:')
        print(type(e))
    return mensaje


# In[ ]:


# Celda Opcional: Descomente la siguiente línea y ejecute esta celda

#guardar_archivo()


# #### Conexión a MySQL

# In[ ]:


# Verifique sus credenciales de acceso a MySQL en el archivo ".env"
load_dotenv()

usuario = os.getenv("BD_USER")
host = os.getenv("BD_HOST")
puerto = os.getenv("BD_PORT")
clave = os.getenv("BD_PASS")
bd_capa_uno = os.getenv("BD_CAPA_UNO")
bd_capa_dos = os.getenv("BD_CAPA_DOS")
tabla_temp = os.getenv("TABLA_TEMP_CAPA_UNO")

print("======= ⏳...Inicio check de conexión a MySQL... ========")
try:
    conn = pymysql.connect(
    host=host,
    user=usuario,
    password=clave,
            )
    if conn.open:
        print(" 1) => Conexion Exitosa !!!")
except pymysql.Error as e:
    print(e)
finally:
    if 'conn' in locals() and conn.open:
        conn.close()
        print(" 2) => Se cierra conexión")
        print("================== Fin check de conexión =================")


# #### Ejecución de scripts SQL
# ##### 1- crea base de datos y tablas | 2- inserta datos en tabla temporal | 3- inserta datos en tabla fact | 4- crea SP tabla_calendario | 5- crea vistas en BD capa_dos

# In[ ]:


# Acceso y descarga de scripts SQL del repositorio.

url_sql_ddl = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/1_PI_UA_DDL.sql'
url_sql_insert_fact = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/2_PI_UA_insert_en_fact.sql'
url_sql_vistas = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/4_PI_UA_capa_dos_vistas.sql'
url_sql_sp = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/3_PI_UA_SP_calendario.sql'

respuesta_1 = requests.get(url_sql_ddl)
respuesta_2 = requests.get(url_sql_sp)  
respuesta_3 = requests.get(url_sql_insert_fact)    
respuesta_4 = requests.get(url_sql_vistas)  


if respuesta_1.status_code == 200 and respuesta_2.status_code == 200 and respuesta_3.status_code == 200 and respuesta_4.status_code == 200:
    script_sql_1 = respuesta_1.text
    script_sql_2 = respuesta_2.text
    script_sql_3 = respuesta_3.text
    script_sql_4 = respuesta_4.text

    print("\n✅ Scripts SQL descargados correctamente desde el repo GitHub.")
    print('---------------------------------------------------------------')

    # Manejo seguro de credenciales de BD.
    # password = getpass.getpass("Ingrese su contraseña de MySQL: ")    

    # se crean motores para diferentes acciones 
    engine_create = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}") # crea nuevas BD.
    engine_insert = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}/{bd_capa_uno}") # inserta datos en tabla temp_cobranzas.
    engine_vista = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}/{bd_capa_dos}") # crea vistas

    #------------------------------------------
    # Inicia proceso de ingesta de datos
    #------------------------------------------
    try:
        print('---------------------------------------------------------------')
        print('⏳Inicio de ingesta en base de datos...\n')

        #__________________________________________________
        # 1.DDL crea base de datos y tablas
        #__________________________________________________
        with engine_create.begin() as connection:

            for statement in script_sql_1.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 1 de 5 ...')
        print(f"✅ Estructuras creadas para las bases de datos:\n - '{bd_capa_uno}'\n - '{bd_capa_dos}'\n")

        #__________________________________________________
        # 2.Crea Stored Procedure en BD cobranzas_capa_uno
        #__________________________________________________
        conn = pymysql.connect(
                                host=host,
                                user=usuario,
                                password=clave,
                                db=bd_capa_uno,
                                port=int(puerto),
                                client_flag=CLIENT.MULTI_STATEMENTS
                               )     

        with conn.cursor() as cursor:
             cursor.execute(script_sql_2)

        conn.commit()
        conn.close()

        print('⏳...script 2 de 5 ...')
        print(f"✅ Stored Procedure 'llenar_calendario' creado en BD '{bd_capa_uno}'\n")        


        #__________________________________________________
        # 3.Ingesta el dataframe en tabla temporal (truncate + insert)
        #__________________________________________________
        with engine_insert.begin() as connection:
            connection.execute(text(f"TRUNCATE TABLE {tabla_temp}"))

            df_final_limpio.to_sql(
                                    name=tabla_temp,
                                    con=connection,
                                    if_exists='append', 
                                    index=False,
                                    chunksize=1000, 
                                    method='multi' # Para que sea masivo y no registro por registro
                                  )
        print('⏳...script 3 de 5 ...')   
        print(f"✅ Datos ingestados en tabla '{tabla_temp}' de BD '{bd_capa_uno}':\n - {len(df_final_limpio)} registros insertados\n")

        #__________________________________________________
        # 4.Pasa datos de tabla_temp a tabla_fact
        #__________________________________________________
        with engine_insert.begin() as connection:

            for statement in script_sql_3.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 4 de 5 ...')
        print(f"✅ Datos transferidos en BD '{bd_capa_uno}':  '{tabla_temp}' => 'fact_cobranzas'\n")

        #__________________________________________________
        # 5.Crea vistas en BD cobranzas_capa_dos
        #__________________________________________________
        with engine_vista.begin() as connection:

            for statement in script_sql_4.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 5 de 5')
        print(f"✅ Vistas creadas en BD '{bd_capa_dos}'\n")

    except Exception as e:
        print(e)
    #------------------------------------------
    # Fin proceso de ingesta de datos
    #------------------------------------------

else:
    print(f'✖️ Error al acceder al archivo Nº 1: Estado {respuesta_1.status_code}')
    print(f'✖️ Error al acceder al archivo Nº 2: Estado {respuesta_2.status_code}')
    print(f'✖️ Error al acceder al archivo Nº 3: Estado {respuesta_3.status_code}')
    print(f'✖️ Error al acceder al archivo Nº 4: Estado {respuesta_4.status_code}')

print('===============================================================')
print('🎉🎉 Orquestación de ETL finalizada con Éxito!! 🎉🎉')
print('===============================================================\n')


# ## Inicialización del Template de Power BI 

# In[ ]:


# Inicializa aplicación Power BI.

if os.path.exists("PI_UA_analisis_cobranzas.pbit"):
    print("===============================================")
    print(" Archivo para Visualizar los datos detectado.")
    print("   ⏳... Espere un instante mientras inicia Power BI...")
    print("===============================================")
    os.startfile("PI_UA_analisis_cobranzas.pbit")
else:
    print("===============================================")
    print("✖️ Archivo Power Bi NO detectado en el directorio actual.")
    print("===============================================")

