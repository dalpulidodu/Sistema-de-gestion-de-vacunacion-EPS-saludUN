from datetime import datetime
from datetime import date
import os
import sqlite3
from sqlite3 import Error

##########################################################################################################
#                                             Data
##########################################################################################################

def sql_connection():
    """
    Funcion que crea la base de datos
    """
    try:
        con = sqlite3.connect('db.db')
        print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha prodicido un error al crear la conexion',Error)

def create_table_affiliate(con):
    """
    Funcion que crea una tabla con los parametros de un afiliado
    (id,nombre, apellidos,direccion, telefono, email, ciudad, nacimiento,fecha de afiliacion, fecha de desafiliacion, vacunado)
             
    """
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,direccion text,telefono real,email text, ciudad text,nacimiento text,afiliacion text,desafiliacion text,vacunado text)")
    con.commit()
    
def read_info_affiliate():
    
    """
    Funcion que lee la informacion de un afiliado y la retorna como una cadena de caracteres
    """
    correct_type = False
    while not correct_type:   
        try:
            id=(input("numero de identificacion"))
            id=id.ljust(12)
            correct_type = True
        except:
            print('Entrada invalida, intentelo de nuevo')
    
    nombre=(input("nombre: "))
    nombre = nombre.ljust(20)
    
    apellido=(input("apellido: "))
    apellido = apellido.ljust(20)
    
    direccion=(input("direccion: "))
    direccion = direccion.ljust(20)
    
    correct_type = False
    while not correct_type:   
        try:
            telefono=(input("telefono: "))
            telefono = telefono.ljust(12)
            correct_type = True
        except:
            print('Entrada invalida, intentelo de nuevo')
        
    email=(input("email: "))
    email = email.ljust(20)
    
    ciudad=(input("ciudad: "))
    ciudad = ciudad.ljust(20)    
    
       
    nacimiento = read_date('nacimiento')

    afiliacion = read_date('afiliacion')
    
    desafiliacion = read_date('desafiliacion')   
        
    salir=False
    while not salir:
        vacunado=(input("fue vacunado?"))
        if (vacunado=='N' or vacunado=='n'):
            salir=True
            
    afiliado=(id ,nombre,apellido ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado )
    return afiliado

def insert_affiliate(con,afiliado):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''',afiliado)
    con.commit()

def update_affiliate(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    vacunado=input("identificacion del afiliado vacunado: ")
    actualizar='update afiliados SET vacunado = "s" where id ='+vacunado
    cursorObj.execute(actualizar)
    print("No los veo")
    con.commit()

def sql_fetch_affiliate(con):
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

def close_db(con):
    con.close()    

##########################################################################################################
#                                        Bussisnes logic
##########################################################################################################
def read_date(word):
    """
    Funcion que lee una fecha infresada por el usuario y la convierte a formato de texto con el formato ISO 8601
    AAAA/MM/DD
    """
    print(word)
    
    dia=(input("dia "+word+": "))
    dia = dia.rjust(2,"0")
    
    mes = (input("mes "+word+": "))
    mes= mes.rjust(2,"0")
    
    ano = (input("ano "+word+": "))
    ano= ano.rjust(4)
    
    date=ano+"-"+mes+"-"+dia
    print(word,date)
    
    return date


##########################################################################################################
#                                        Presentation
##########################################################################################################
def clear_screen():
    '''
    Limpia la consola
    '''
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def menu():
    clear_screen()
    print(
    '''#############################################################################################
                           Sistema de gestion de vacunacion EPS saludUN   
#############################################################################################
                                  
                                       Menu principal
    
    Seleccione una opcion:
    1. Gestion de afiliados
    2. Gestion lotes de vacunas')
    3. Gestion Plan de vacunacion
    4. Agenda de vacunacion
    e. Salir
    
    ''')

def menu_affiliate():
    clear_screen()
    print('''#############################################################################################
                                     Afiliados  
#############################################################################################
    
    Seleccione una opcion:
    1. Ingresar nuevo afiliado
    2. Actualizar estado de afiliado
    3. Consultar afiliado
    b. Volver al menu anterior
    e. Salir
    
    ''')
    
    
def main():    
    
    con=sql_connection()
    create_table_affiliate(con)
    
    salir=False
    while not salir:
                    
        menu()
        option = input('Ingrese una opcion: ')
            
        if(option == '1'): # menu afiliado
              
            back = False
            while not back:              
                
                menu_affiliate()  
                option = input('Ingrese una opcion: ')
                    
                if(option == '1'):  # ingresar nuevo afiliado                  
                    afiliado=read_info_affiliate()
                    insert_affiliate(con,afiliado)
                elif(option == '2'): # Actualizar estado de afiliado  
                    update_affiliate(con)
                elif(option == '3'): # Consultar afiliado
                    sql_fetch_affiliate(con)
                    input('Presione cualquier tecla para continuar')
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')
        elif(option == '2'):
            print()
        elif(option == '3'): 
            print()
        elif(option == 'e' or option == 'E'):
            salir = True
        else:    
            print('Opcion no valida')
    
    close_db(con)
    
main()
