import pandas as pd
import sqlite3
import math

def loadDataframe(query,conn):
    dataframe = pd.read_sql(query,conn)
    return dataframe

def getTopIps():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT origen FROM alertas where prioridad=1",conn)
    ips = dict()
    for i in range(0,len(dataframe)):
        if dataframe['origen'][i] in ips: ips[dataframe['origen'][i]] += 1
        else: ips[dataframe['origen'][i]] = 1
    maximo = 0
    for ip in ips:
        if ips[ip]>maximo: maximo=ips[ip]
    ips_sorted = sorted(ips.items(), key= lambda x:x[1], reverse=True)
    #CERRAR CONEXION
    conn.close()
    return ips_sorted[:10]

def getAlertsByCategory():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT clasificacion FROM alertas",conn)
    alertas = dict()
    for i in range(0,len(dataframe)):
        if dataframe['clasificacion'][i] in alertas: alertas[dataframe['clasificacion'][i]] += 1
        else: alertas[dataframe['clasificacion'][i]] = 1
    #CERRAR CONEXION
    conn.close()
    return alertas

def getAlertsInTime():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT timestamp FROM alertas",conn)
    serie = dict()
    for i in range(0,len(dataframe)):
        time = dataframe['timestamp'][i].split(" ")[0]
        if time in serie: serie[time] += 1
        else: serie[time] = 1
    dates = list(serie.keys())
    alerts = []
    for date in dates:
        alerts.append(serie[date])
    df = pd.DataFrame({'Date':dates,'Alerts':alerts})
    #CERRAR CONEXION
    conn.close()
    return df

def getDispositivosVulnerables():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT devices.id, analisis.servicios_inseguros, analisis.vulnerabilidades_detectadas FROM devices INNER JOIN analisis ON devices.id=analisis.id_device",conn)
    values = dict()
    for i in range(0,len(dataframe)):
        values[dataframe['id'][i]] = dataframe['servicios_inseguros'][i] + dataframe['vulnerabilidades_detectadas'][i]
    values_sorted = sorted(values.items(), key= lambda x:x[1], reverse=True)
    ids = []
    value_id = []
    for dispositivo in values_sorted:
        ids.append(dispositivo[0])
        value_id.append(dispositivo[1])
    #CERRAR CONEXION
    conn.close()
    return ids, value_id


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

def mediaPuertosAbiertos(dataframePuertos):
    contadorPuertos = 0
    for i in range(0,len(dataframePuertos)):
        fila = dataframePuertos[i]
        puertos = stringToPorts(fila)
        contadorPuertos += len(puertos)
    media = contadorPuertos/len(dataframePuertos)

    return media

def getPuertosMetricas():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT servicios_inseguros, servicios, puertos_abiertos FROM analisis",conn)
    servicios_inseguros = sum(list(dataframe['servicios_inseguros']))
    servicios = sum(list(dataframe['servicios']))
    media_puertos = mediaPuertosAbiertos(dataframe['puertos_abiertos'])
    #CERRAR CONEXION
    conn.close()
    return media_puertos, servicios_inseguros, servicios