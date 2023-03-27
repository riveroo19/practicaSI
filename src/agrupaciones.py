import pandas as pd
import sqlite3


#primeramente hay que considerar que las vulnerabilidades están en la tabla analisis, que tiene una foreign key procedente de la tabla devices, que a su vez se puede relacionar con 
#la tabla alertas por su campo ip origen e ip destino, luego habrá que unir las 3 tablas y hacer la consulta de los diferentes campos sobre ella.


def giga_query_prioridad(con):
    df = pd.read_sql_query('''
    SELECT * FROM devices JOIN alertas ON alertas.origen=devices.ip OR alertas.destino=devices.ip JOIN analisis ON analisis.id_device=devices.id
    ''', con)
    #print(df, "\n")
    print("Los id de los unicos dispositivos que forman parte de una alerta son: ", df['id'].unique(),"\n")

    print("AGRUPACIONES POR PRIORIDADES\n")
    
    #ver el número de observaciones total (con esto vemos que para las alertas de distinta prioridad, ha habido x número de alertas que han encontrado vulnerabilidades)
    grouped = df.groupby(['prioridad'])
    n_registros = grouped.size()
    print("Número de alertas categorizadas por su prioridad en donde uno de los 2 dispositivos que participan tiene vulnerabilidades:\n", n_registros)
    #numero de missing (alerta)
    df_missings = pd.read_sql_query('''
    SELECT COUNT(*) FROM devices JOIN alertas ON alertas.origen=devices.ip OR alertas.destino=devices.ip JOIN analisis ON analisis.id_device=devices.id
    WHERE msg LIKE '%issing%' OR localizacion LIKE 'None' OR puertos_abiertos LIKE 'None' GROUP BY prioridad
    ''', con)#puertos abiertos, localizacion y msg son los únicos que toman esos valores de los dispositivos, en alertas es missing por el mensaje
    print("\nNumero de campos con valor missing o None:\n",df_missings)
    #alternativa:
    df2 = pd.read_sql_query('''
    SELECT prioridad, COUNT(*) FROM alertas WHERE origen NOT IN (SELECT ip FROM devices) AND destino NOT IN (SELECT ip FROM devices) GROUP BY prioridad
    ''', con)
    print("\nNúmero de alertas en las que los dispositivos registrados no \"participan\"\n", df2)

    #media 
    media = grouped['vulnerabilidades_detectadas'].mean()
    print("\nLa media es:\n",media) #valores muy similares: muchas tuplas cuyo dispositivo origen/destino perteneciente a la tabla devices tiene 15 vulnerabilidades

    #mediana
    mediana = grouped['vulnerabilidades_detectadas'].median()
    print("\nLa mediana es:\n",mediana)

    #varianza
    varianza = grouped['vulnerabilidades_detectadas'].var()
    print("\nLa varianza es:\n", varianza)
    #maximo y minimo (max/min del número de vulnerabilidades de un dispositivo que "participe" en una alerta)
    maximos = grouped['vulnerabilidades_detectadas'].max()
    minimos = grouped['vulnerabilidades_detectadas'].min()
    print("\nLos maximos son:\n", maximos, "\nLos minimos son:\n", minimos)

def giga_query_meses(con):
    df = pd.read_sql_query('''
    SELECT * FROM devices JOIN alertas ON alertas.origen=devices.ip OR alertas.destino=devices.ip JOIN analisis ON analisis.id_device=devices.id
    ''', con)
    #print(df, "\n")
    print("Los id de los unicos dispositivos que forman parte de una alerta son: ", df['id'].unique(),"\n")

    print("AGRUPACIONES POR MESES\n")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    inicio_julio = pd.to_datetime('2022-07-01 00:00:00')
    fin_agosto = pd.to_datetime('2022-09-01 00:00:00') - pd.Timedelta(seconds=1)
    df_rango = df.loc[df['timestamp'].between(inicio_julio, fin_agosto)]

    #numero de observaciones
    grouped = df_rango.groupby(pd.Grouper(key='timestamp', freq='MS'))
    n_registros = grouped.size()
    print("\nEl numero de observaciones es:\n",n_registros)

    #numeros de missing (alerta)
    df_missings = pd.read_sql_query('''
    SELECT strftime('%m', timestamp) as Month, COUNT(*) FROM devices JOIN alertas ON alertas.origen=devices.ip OR alertas.destino=devices.ip JOIN analisis ON analisis.id_device=devices.id
    WHERE msg LIKE '%issing%' OR localizacion LIKE 'None' OR puertos_abiertos LIKE 'None' AND timestamp <= "2022-08-31 23:59:59" GROUP BY strftime("%m-%Y", timestamp) 
    ''', con)#puertos abiertos, localizacion y msg son los únicos que toman esos valores de los dispositivos, en alertas es missing por el mensaje
    df_missings = df_missings.drop(df_missings[df_missings['Month'] == '09'].index)
    print("\nNumero de campos con valor missing o None:\n",df_missings)
    #alternativa:
    df2 = pd.read_sql_query('''
    SELECT strftime('%m', timestamp) as Month, COUNT(*) FROM alertas WHERE origen NOT IN (SELECT ip FROM devices) AND destino NOT IN (SELECT ip FROM devices) GROUP BY strftime("%m-%Y", timestamp)
    ''', con)
    #df2 = df2.drop(df2[df2['Month'] == '09'].index)
    print("\nNúmero de alertas en las que los dispositivos registrados no \"participan\"\n", df2)
    
    #media 
    media = grouped['vulnerabilidades_detectadas'].mean()
    print("\nLa media es:\n",media) #valores muy similares: muchas tuplas cuyo dispositivo origen/destino perteneciente a la tabla devices tiene 15 vulnerabilidades

    #mediana
    mediana = grouped['vulnerabilidades_detectadas'].median()
    print("\nLa mediana es:\n",mediana)

    #varianza
    varianza = grouped['vulnerabilidades_detectadas'].var()
    print("\nLa varianza es:\n", varianza)
    #maximo y minimo (max/min del número de vulnerabilidades de un dispositivo que "participe" en una alerta)
    maximos = grouped['vulnerabilidades_detectadas'].max()
    minimos = grouped['vulnerabilidades_detectadas'].min()
    print("\nLos maximos son:\n", maximos, "\nLos minimos son:\n", minimos)
    
    

con = sqlite3.connect("../database.db")

#giga_query_prioridad(con)
giga_query_meses(con)