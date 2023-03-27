import sqlite3

def sql_fetch_alertas(cursorObj):
   cursorObj.execute('SELECT * FROM alertas')
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

def sql_fetch_devices(cursorObj, tablename):
   print(tablename)
   cursorObj.execute('SELECT * FROM %s' % tablename)
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)
#CONEXION BASE DATOS
con = sqlite3.connect("../database.db")
cursorObj = con.cursor()

#sql_fetch_alertas(cursorObj)
sql_fetch_devices(cursorObj, "responsible")
sql_fetch_devices(cursorObj, "devices")
sql_fetch_devices(cursorObj, "analisis")