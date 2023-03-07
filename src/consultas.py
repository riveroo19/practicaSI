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
    for i in range(0,len(dataframeAnalisis)):
        fila = dataframeAnalisis['puertos_abiertos'][i]
        puertos = stringToPorts(fila)
        contadorPuertos += len(puertos)
    media = contadorPuertos/len(dataframePuertos)

    acumulador = 0
    for i in range(0,len(dataframeAnalisis)):
        fila = dataframeAnalisis['puertos_abiertos'][i]
        puertos = stringToPorts(fila)
        acumulador += (len(puertos) - media)**2

    varianza = acumulador / len(dataframeAnalisis)
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
#VALOR MINIMO Y MAXIMO DEL NUMERO DE VULNERABILIDADES DETECTADAS


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

con.close()