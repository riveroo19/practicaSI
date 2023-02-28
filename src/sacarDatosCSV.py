import sqlite3
import csv


def sql_create_alertas(con,cursorObj):
    cursorObj.execute("CREATE TABLE IF NOT EXISTS alertas (timestamp datetime, sid int, msg text, clasificacion text, prioridad int, protocolo text, origen text, destino text, puerto int)")
    con.commit()

def sql_fetch(cursorObj):
   cursorObj.execute('SELECT * FROM alertas')
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

def sql_insert(cursor,timestamp,sid,msg,clasificacion,prioridad,protocolo,origen,destino,puerto):
    cursorObj = con.cursor()
    consulta = "INSERT INTO alertas VALUES ('"+str(timestamp)+"', "+str(sid)+", '"+msg+"','"+clasificacion+"','"+str(prioridad)+"','"+protocolo+"','"+origen+"','"+destino+"',"+str(puerto)+")"
    cursorObj.execute(consulta)

def sql_commit(con):
    con.commit()

#CONEXION BASE DATOS
con = sqlite3.connect("../database.db")
cursorObj = con.cursor()
sql_create_alertas(con,cursorObj)


#LEER ARCHIVO CSV
i=0
with open('../alerts.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        if i!=0:
            print(row)
            timestamp = row[0]
            sid = row[1]
            msg = row[2]
            clasificacion = row[3]
            prioridad = row[4]
            protocolo = row[5]
            origen = row[6]
            destino = row[7]
            puerto = row[8]
            sql_insert(cursorObj,timestamp,sid,msg,clasificacion,prioridad,protocolo,origen,destino,puerto)
            
        i+=1

sql_commit(con)

#MOSTRAR TABLA ALERTAS
sql_fetch(cursorObj)

#DESCONECTAR BASE DATOS
con.close()