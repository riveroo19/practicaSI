import sqlite3

def sql_fetch(cursorObj):
   cursorObj.execute('SELECT * FROM alertas')
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

#CONEXION BASE DATOS
con = sqlite3.connect("./database.db")
cursorObj = con.cursor()

sql_fetch(cursorObj)