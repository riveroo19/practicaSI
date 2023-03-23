import pandas as pd
import sqlite3

            #numero de observaciones 
#por prioridad de alerta
def prioridad_observaciones(con):
    print()
    df = pd.read_sql("SELECT prioridad, COUNT(*) as N_OCURRENCIAS FROM alertas GROUP BY prioridad", con)
    print(df)
#por fecha (mes julio y agosto)
def fecha_observaciones(con):
    print()
    df = pd.read_sql("SELECT COUNT(*) as JULIO FROM alertas WHERE timestamp>='2022-07-01 00:00:00' AND timestamp<='2022-07-31 23:59:59'", con)
    print(df)
    print()
    df = pd.read_sql("SELECT COUNT(*) as AGOSTO FROM alertas WHERE timestamp>='2022-08-01 00:00:00' AND timestamp<='2022-08-31 23:59:59'", con)
    print(df)

            #numero de missings (ni idea)

            #media
def prioridad_mediana(con):
    df = pd.read_sql("SELECT prioridad, AVG(*) FROM alertas GROUP BY prioridad", con)
    print(df)

def fecha_mediana(con):
    df = pd.read_sql("SELECT AVG")

con = sqlite3.connect("../database.db")

prioridad_observaciones(con)
fecha_observaciones(con)
        

