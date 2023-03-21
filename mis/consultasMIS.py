import pandas as pd
import sqlite3
import math

def loadDataframe(query,conn):
    dataframe = pd.read_sql(query,conn)
    return dataframe

def getTopIps():
    #CONEXION BASE DATOS
    conn = sqlite3.connect("../database.db")
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
    conn = sqlite3.connect("../database.db")
    cursorObj = conn.cursor()
    dataframe = loadDataframe("SELECT clasificacion FROM alertas",conn)
    alertas = dict()
    for i in range(0,len(dataframe)):
        if dataframe['clasificacion'][i] in alertas: alertas[dataframe['clasificacion'][i]] += 1
        else: alertas[dataframe['clasificacion'][i]] = 1
    #CERRAR CONEXION
    conn.close()
    return alertas