import sqlite3
from sqlite3 import Error
def sql_connection():
    #funcion que crea la base de datos
    try:
        con = sqlite3.connect('db.db')
        print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha prodicido un error al crear la conexion',Error)

def creartable(con):
    """
             Se crea el objeto de conexión.
             El objeto cursor se crea utilizando el objeto de conexión
             se ejecuta el método execute con la consulta CREATE TABLE como parámetro         """
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,direccion text,telefono real,email text, ciudad text,nacimiento text,afiliacion text,desafiliacion text,vacunado text)")
    con.commit()
def leer_info():
    id=(input("numero de identificacion"))
    id=id.ljust(12)
    #id=int(id)
    nombre=(input("nombre"))
    nombre = nombre.ljust(20)
    apellido=(input("apellido"))
    apellido = apellido.ljust(20)
    direccion=(input("direccion"))
    direccion = direccion.ljust(20)
    telefono=(input("telefono"))
    telefono = telefono.ljust(12)
    email=(input("email"))
    email = email.ljust(20)
    ciudad=(input("ciudad"))
    ciudad = ciudad.ljust(20)
    dianac=(input("dia nacimiento:  "))
    dianac = dianac.rjust(2,"0")
    mesnac = (input("mes nacimiento:  "))
    mesnac = mesnac.rjust(2,"0")
    anonac = (input("ano nacimiento:  "))
    anonac = anonac.rjust(4)
    nacimiento=dianac+"/"+mesnac+"/"+anonac
    print("nacimiento",nacimiento)

    afiliacion = (input("afiliacion"))
    desafiliacion = (input("desafiliacion"))
    #vacunado = (input("vacunado"))
    salir=False
    while not salir:
        vacunado=(input("fue vacunado?"))
        if (vacunado=='N' or vacunado=='n'):
            salir=True
    afiliado=(id ,nombre,apellido ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado )
    return afiliado


def insertar_tabla(con,afiliado):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''',afiliado)


    con.commit()

def update_table(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    vacunado=input("identificacion del afiliado vacunado: ")
    actualizar='update afiliados SET vacunado = "s" where id ='+vacunado
    cursorObj.execute(actualizar)
    print("No los veo")
    con.commit()


def sql_fetch(con):
    cursorObj = con.cursor()
    afiliad=input("id del afiliado a consultar: ")
    buscar='SELECT * FROM afiliados where id= '+afiliad
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    print("Vere:  ", len(filas), " filas")
    for row in filas:
        print("el tipo de datos de row es:", type(row))
        id=row[0]
        nombre=row[1]
        print(" la info de la tupla es: ", id, " y ", nombre)

        print(row)
    con.commit()

def cerrar_db(con):
    con.close()
def main():
    con=sql_connection()
    #creartable(con)
    #afiliado=leer_info()
    #insertar_tabla(con,afiliado)
    #update_table(con)
    sql_fetch(con)
    cerrar_db(con)
main()
