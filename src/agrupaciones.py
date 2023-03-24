import pandas as pd
import sqlite3


#primeramente hay que considerar que las vulnerabilidades están en la tabla analisis, que tiene una foreign key procedente de la tabla devices, que a su vez se puede relacionar con 
#la tabla alertas por su campo ip origen e ip destino, luego habrá que unir las 3 tablas y hacer la consulta de los diferentes campos sobre ella.

#generaremos un dataframe que se corresponda con la tabla resultante de los join


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

    grouped = df_rango.groupby(pd.Grouper(key='timestamp', freq='MS'))
    n_registros = grouped.size()
    print(n_registros)
    

con = sqlite3.connect("../database.db")

giga_query_prioridad(con)
#giga_query_meses(con)