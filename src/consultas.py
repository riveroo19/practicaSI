import pandas as pd
import sqlite3
import math

def stringToPorts(fila):
    if fila == '"None"': return []
    else:
        fila = fila.replace("[","").replace("]","")
        splitFila = fila.split(",")
        ports=set()
        for i in range(0,len(splitFila)):
            port = splitFila[i].replace(" ","").replace('"',"")
            ports.add(port)
        return list(ports)

def loadDataframe(query,conn):
    dataframe = pd.read_sql(query,conn)
    return dataframe

#NUMERO DE DISPOSITIVOS (Y MISSING)
def numeroDispositivos(con):
    dataframe = loadDataframe("SELECT * FROM devices",con)
    return len(dataframe)
#NUMERO DE ALERTAS
def numeroAlertas(dataframeAlertas):
    return len(dataframeAlertas)
#MEDIA Y DESVIACION ESTANDAR DEL TOTAL DE PUERTOS ABIERTOS
def media_desviacion_PuertosAbiertos(dataframePuertos):
    contadorPuertos = 0
    for i in range(0,len(dataframePuertos)):
        fila = dataframePuertos['puertos_abiertos'][i]
        puertos = stringToPorts(fila)
        contadorPuertos += len(puertos)
    media = contadorPuertos/len(dataframePuertos)

    acumulador = 0
    for i in range(0,len(dataframePuertos)):
        fila = dataframePuertos['puertos_abiertos'][i]
        puertos = stringToPorts(fila)
        acumulador += (len(puertos) - media)**2

    varianza = acumulador / len(dataframePuertos)
    desviacion = math.sqrt(varianza)
    return media, desviacion
#MEDIA Y DESVIACION ESTANDAR DEL NUMERO DE VULNERABILIDADES DETECTADAS
def media_desviacion_VulnerabilidadesDetectadas(dataframeVulnerabilidades):
    contadorVulnerabilidades = 0
    for i in range(0,len(dataframeVulnerabilidades)):
        nvul = dataframeVulnerabilidades['vulnerabilidades_detectadas'][i]
        contadorVulnerabilidades += nvul
    media = contadorVulnerabilidades/len(dataframeVulnerabilidades)

    acumulador = 0
    for i in range(0,len(dataframeVulnerabilidades)):
        nvul = dataframeVulnerabilidades['vulnerabilidades_detectadas'][i]
        acumulador += (nvul - media)**2
    varianza = acumulador / len(dataframeVulnerabilidades)
    desviacion = math.sqrt(varianza)

    return media, desviacion

#VALOR MINIMO Y MAXIMO DEL TOTAL DE PUERTOS ABIERTOS
def min_max_puertos_abiertos(dataframe_puertos):
    minimo = -1
    maximo = -1
    for i in range(0,len(dataframe_puertos)):
        fila = dataframe_puertos['puertos_abiertos'][i]
        puertos = stringToPorts(fila)
        for puerto in puertos:
            split = puerto.split("/")
            numero_puerto = int(split[0])
            if minimo == -1: minimo = numero_puerto
            elif numero_puerto<minimo: minimo = numero_puerto
            if maximo == -1: maximo = numero_puerto
            elif numero_puerto>maximo: maximo=numero_puerto
    return minimo, maximo
        
#VALOR MINIMO Y MAXIMO DEL NUMERO DE VULNERABILIDADES DETECTADAS
def min_max_vulnerabilidades_detectadas(dataframeVulnerabilidades):
    minimo = -1
    maximo = -1
    for i in range(0,len(dataframeVulnerabilidades)):
        vulnerabilidades =dataframeVulnerabilidades['vulnerabilidades_detectadas'][i]
        if minimo == -1: minimo = vulnerabilidades
        elif vulnerabilidades<minimo: minimo = vulnerabilidades
        if maximo == -1: maximo = vulnerabilidades
        elif vulnerabilidades>maximo: maximo=vulnerabilidades
    return minimo, maximo

#CONEXION BASE DATOS
con = sqlite3.connect("../database.db")
cursorObj = con.cursor()

#NUMEROS DISPOSITIVOS
print("NUMERO DISPOSITIVOS => " + str(numeroDispositivos(con)))
#NUMERO ALERTAS
dataframeAlertas = loadDataframe("SELECT * FROM alertas",con)
print("NUMERO ALERTAS => " + str(numeroAlertas(dataframeAlertas)))

#MEDIA Y DESVIACION DE PUERTOS ABIERTOS
dataframeAnalisis = loadDataframe("SELECT puertos_abiertos FROM analisis",con)
mediaPuertos, desviacionPuertos = media_desviacion_PuertosAbiertos(dataframeAnalisis)
print("MEDIA PUERTOS ABIEROTS => " + str(mediaPuertos))
print("DESVIACION ESTANDAR PUERTOS ABIEROTS => " + str(desviacionPuertos))

#MEDIA Y DESVIACION DE VULNERABILIDADES DETECTADAS
dataframeVulnerabilidades = loadDataframe("SELECT vulnerabilidades_detectadas FROM analisis",con)
mediaVulnerabilidades, desviacionVulnerabilidades = media_desviacion_VulnerabilidadesDetectadas(dataframeVulnerabilidades)
print("MEDIA VULNERABILIDADES DETECTADAS => " + str(mediaVulnerabilidades))
print("DESVIACION ESTANDAR VULNERABILIDADES DETECTADAS => " + str(desviacionVulnerabilidades))

#MAXIMO Y MINIMO PUERTOS
minimoPuerto, maximoPuerto = min_max_puertos_abiertos(dataframeAnalisis)
print("PUERTO MINIMO => " + str(minimoPuerto))
print("PUERTO MAXIMO => " + str(maximoPuerto))

#MAXIMO Y MINIMO VULNERABILIDADES
minimoVulnerabilidades, maximoVulnerabilidades = min_max_vulnerabilidades_detectadas(dataframeVulnerabilidades)
print("VULNERABILIDADES MINIMAS => " + str(minimoVulnerabilidades))
print("VULNERABILIDADES MAXIMAS => " + str(maximoVulnerabilidades))

#CERRAR CONEXION
con.close()