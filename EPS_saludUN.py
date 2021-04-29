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
            i=int(input("numero de identificacion: "))
            id = str(i)
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
            t=int(input("telefono: "))
            telefono=str(t)
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
    
    desafiliacion = '00/00/0000'        
    
    vacunado='no'
        
            
    afiliado=(id ,nombre,apellido ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado )
    return afiliado

def insert_affiliate(con,afiliado):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''',afiliado)
    con.commit()

def update_affiliate_vaccine(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    vacunado=input("identificacion del afiliado vacunado: ")
    actualizar='update afiliados SET vacunado = "si" where id ='+vacunado
    cursorObj.execute(actualizar)
    con.commit()
    
def update_disaffiliated(con):
    """ Funcion que se utiliza para operar en la base de datos"""
    cursorObj = con.cursor()
    desafiliado=input("identificacion del afiliado a desafiliar: ")
    fecha = date_to_string(date.today())  
    print(fecha)      
    actualizar='update afiliados SET desafiliacion = "'+fecha+'" where id ='+desafiliado
    cursorObj.execute(actualizar)
    con.commit()

def sql_fetch_affiliate(con):    
    cursorObj = con.cursor()
    afiliad=input("id del afiliado a consultar: ")
    buscar='SELECT * FROM afiliados where id= '+afiliad
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    print()
    header=('id: ', 'Nombre: ','Apellidos: ', 'Direccion: ','Telefono:', 'Email: ','Ciudad: ','Nacimiento: ', 'Fecha de afiliacion: ', 'Fecha de desafiliacion: ', 'Vacunado: ')
    for row in filas:
        for i in range(11):            
            print(header[i]+''+str(row[i]))
    con.commit()
    print()
    
def close_db(con):
    con.close()    


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
    2. Gestion lotes de vacunas
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
    
def menu_new_affiliate():
     clear_screen()
     print('''#############################################################################################
                                     Nuevo Afiliado  
#############################################################################################
    Ingrese los datos del nuevo afiliado:
    
    
    ''')
    
def menu_state_affiliate():
     clear_screen()
     print('''#############################################################################################
                                     Estado del Afiliado  
#############################################################################################
    
    1. Vacunacion
    2. Desafiliacion
    b. Volver
    e. Salir
    
    
    ''')
    
def menu_info_affiliate():
    clear_screen()
    print('''#############################################################################################
                                     Consulta Afiliado  
#############################################################################################
    Ingrese el numero de identificacion del afiliado para ver su informacion:
    
    
    ''')

def menu_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Gestion lotes de vacunas 
#############################################################################################
    
    Seleccione una opcion:
    1. Ingresar nuevo lote de vacunacion
    2. Consultar lote de vacunacion
    b. Volver al menu anterior
    e. Salir
    
    ''')
    
def menu_new_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Nuevo lote de vacunas 
#############################################################################################
    
    Ingrese el nuevo lote de vacunacion:
    
    ''')
    
def menu_info_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Consultar lote de vacunas 
#############################################################################################
    
    Ingrese el numero de lote de vacunacion a consultar:
    
    ''')    
    
def menu_plan_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Gestion plan de vacunacion 
#############################################################################################
    
    Seleccione una opcion:
    1. Crear plan de vacunacion
    2. Consultar plan de vacunacion
    b. Volver al menu anterior
    e. Salir
    
    ''')    

def menu_new_plan_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Nuevo Plan de vacunas 
#############################################################################################
    
    Ingrese el nuevo lote de vacunacion:
    
    ''')
    
def menu_info_plan_vaccine():
    clear_screen()
    print('''#############################################################################################
                                     Consultar Plan de vacunas 
#############################################################################################
    
    Ingrese el numero de plan de vacunacion a consultar:
    
    ''')  

def menu_calendar_vaccune():
    print('''#############################################################################################
                                     Calendario de vacunacion
#############################################################################################
    
    Programacion de citas de vacunacion
    
    ''')
    
##########################################################################################################
#                                        Bussisnes logic
##########################################################################################################
def date_to_string(date):
    
    f = date.isoformat().split('-')
    return str(f[2])+'/'+str(f[1])+'/'+str(f[0])

def read_date(word):
    """
    Funcion que lee una fecha infresada por el usuario y la convierte a formato de texto DD/MM/AAAA
    """
    correct_date = False
    while not correct_date :
        print()
        print(word)
        
        correct_type = False
        while not correct_type:   
            try:
                d=int(input("dia "+word+": "))
                if(d>=0 and d<=31):
                    dia= str(d)
                    dia = dia.rjust(2,"0")
                    correct_type = True
                else:                    
                    raise 
            except:
                print('Entrada invalida, intentelo de nuevo')
                    
        correct_type = False        
        while not correct_type:   
            try:
                m=int(input("mes "+word+": "))
                if(m>=0 and m<=12):
                    mes = str(m)
                    mes= mes.rjust(2,"0")
                    correct_type = True
                else:
                    raise
            except:
                print('Entrada invalida, intentelo de nuevo')
           
        
        correct_type = False        
        while not correct_type:   
            try:
                
                a=int(input("ano "+word+": "))
                if(a>=0):
                    ano = str(a)
                    ano= ano.rjust(4,"0")
                    correct_type = True
                else:
                    raise ValueError
            except:
                print('Entrada invalida, intentelo de nuevo')         
                  
        date_aux =ano+"-"+mes+"-"+dia
        
   
        if date_aux == '0000-00-00':
            correct_date = True
        elif date.fromisoformat(date_aux) > date.today():
            print('Fecha fuera de rango, intentelo de nuevo.')
        else:
            correct_date = True
                 
    return dia+"/"+mes+"/"+ano
    
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
                    menu_new_affiliate()                  
                    afiliado=read_info_affiliate()
                    insert_affiliate(con,afiliado)
                    input('Nuevo afiliado registrado. Presione cualquier tecla para continuar...')
                    
                elif(option == '2'): # Actualizar estado de afiliado
                    
                    back = False
                    while not back:
                        menu_state_affiliate()
                        option = input('Ingrese una opcion: ')
                        if(option=='1'): #Vacunacion
                            update_affiliate_vaccine(con)
                            input('Presione cualquier tecla para continuar...')
                        elif(option == '2'): #Desafiliacion
                            update_disaffiliated(con)
                            input('Presione cualquier tecla para continuar...')
                        elif(option == 'b' or option == 'B'): # Volver al menu anterior
                            back = True
                        elif(option == 'e' or option == 'E'): # Salir del programa
                            back = True
                            salir = True
                        else:
                            print('Opcion no valida')
                
                    
                elif(option == '3'): # Consultar afiliado
                    menu_info_affiliate()
                    sql_fetch_affiliate(con)
                    input('Presione cualquier tecla para continuar...')
                    
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')
                    
        elif(option == '2'):#menu gestion lotes de vacunas
            back = False
            while not back:
                menu_vaccine()
                option = input('Ingrese una opcion: ')
                if(option=='1'): #crear lote Vacunacion
                    menu_new_vaccine()
                    #
                    input('Presione cualquier tecla para continuar...')
                elif(option == '2'): #consultar lote vacunacion
                    menu_info_vaccine()
                    #
                    input('Presione cualquier tecla para continuar...')
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')
                    
        elif(option == '3'):#menu gestion plan de vacunacion 
            back = False
            while not back:
                menu_plan_vaccine()
                option = input('Ingrese una opcion: ')
                if(option=='1'): #crear plan de Vacunacion
                    menu_new_plan_vaccine()
                    #
                    input('Presione cualquier tecla para continuar...')
                    
                elif(option == '2'): #consultar plan de vacunacion
                    menu_info_plan_vaccine()
                    #
                    input('Presione cualquier tecla para continuar...')
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')
                    
        elif(option == '4'): #♦menu agenda de vacunacion
            menu_calendar_vaccune()            
        elif(option == 'e' or option == 'E'):
            salir = True
        else:    
            print('Opcion no valida')
    
    close_db(con)
    
main()
