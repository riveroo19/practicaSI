import json
import sqlite3

#3 tablas para almacenar la información del json en la bd
def sql_create_devices(con,cursorObj):
    cursorObj.execute("CREATE TABLE IF NOT EXISTS responsible (nombre text, telefono int, rol text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS devices (id text, ip text, localizacion text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS analisis(puertos_abiertos text, servicios int, servicios_inseguros int, vulnerabilidades_detectadas int)")
    con.commit()

#añadimos las restrictions para relacionar las 3 tablas entre sí, añadiendo a responsible y analisis el campo id_device que es clave foranea de devices (id)
def sql_alter_tables(con, cursorObj):
    cursorObj.execute("ALTER TABLE responsible ADD id_device text CONSTRAINT constraint1 REFERENCES devices (id)")
    cursorObj.execute("ALTER TABLE analisis ADD id_device text CONSTRAINT constraint2 REFERENCES devices (id)")
    con.commit()

#meramente para ver si se han introducido los datos correctamente
def sql_fetch(cursorObj, tablename):
   print(tablename)
   cursorObj.execute('SELECT * FROM %s' % tablename)
   rows = cursorObj.fetchall()
   for row in rows:
      print(row)

def sql_insert(con, cursorObj, data):
    
    responsible = data["responsable"]
    cursorObj.execute("INSERT INTO responsible (nombre, telefono, rol, id_device) VALUES (?, ?, ?, ?)", (responsible["nombre"], responsible["telefono"], responsible["rol"], data["id"]))

    #json.dumps convierte a una cadena JSON antes de insertar
    analisis = data["analisis"]
    cursorObj.execute("INSERT INTO analisis (puertos_abiertos, servicios, servicios_inseguros, vulnerabilidades_detectadas, id_device) VALUES (?, ?, ?, ?, ?)", (json.dumps(analisis["puertos_abiertos"]), analisis["servicios"], analisis["servicios_inseguros"], analisis["vulnerabilidades_detectadas"], data["id"]))

    #aquí no hay data[devices] porque los dispositivos son el objeto json en si, no objetos dentro de este como en los otros casos
    cursorObj.execute("INSERT INTO devices (id, ip, localizacion) VALUES (?, ?, ?)", (data["id"], data["ip"], data["localizacion"]))

    con.commit()



con = sqlite3.connect("../database.db")
#con = sqlite3.connect("databaseJS.db") # por si queremos guardarlo en otra base de datos por lo que fuera
cursorObj = con.cursor()
sql_create_devices(con, cursorObj)
sql_alter_tables(con, cursorObj)



#LEER ARCHIVO JSON
with open("../devices.json") as file:
    dispositivos = json.load(file)

# iterar sobre los objetos JSON y llamar a la función sql_insert para insertar los datos en la base de datos
for data in dispositivos:
    sql_insert(con, cursorObj, data)

sql_fetch(cursorObj, "responsible")
sql_fetch(cursorObj, "devices")
sql_fetch(cursorObj, "analisis")
# cerrar la conexión a la base de datos
con.close()




