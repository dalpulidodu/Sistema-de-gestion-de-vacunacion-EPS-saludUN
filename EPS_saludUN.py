from datetime import datetime
from datetime import date
import os
import sqlite3
from sqlite3 import Error

from PIL import Image, ImageDraw, ImageFont

##########################################################################################################
#                                             Data
##########################################################################################################

def sql_connection():
    """Crea la base de datos.
    
    Crea  y retorna un objeto sqlite3.connect() que creara una conexion a la base de datos llamada db.db
    
    Except
    -------
    Error : Si no se puede crear la conexion a la base de datos
        
    Returns
    -------
    con : TYPE
        DESCRIPTION.

    """
    try:
        con = sqlite3.connect('db.db')
        print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha prodicido un error al crear la conexion',Error)

def create_table_affiliate(con):
    """Crea una tabla con los parametros de un afiliado
    
    Crea una tabla  con los siguentes encabezados:
    (id,nombre, apellidos,direccion, telefono, email, ciudad, nacimiento,fecha de afiliacion, fecha de desafiliacion, vacunado)
    
    Parameters
    ----------
    con : Conexion con la base de datos SQL

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,direccion text,telefono real,email text, ciudad text,nacimiento text,afiliacion text,desafiliacion text,vacunado text)")
    con.commit()
#Y   
def read_info_affiliate():  
    """Lee la informacion de un afiliado.
    
    Retorna una tupla con los datos del afiliado. Con fecha de desafiliacion por defecto 00/00/0000 y estado vancuado 'no'
    
    Excepct
    -------
    TypeError : Cuando se ingresan letras en vez de numeros en los datos de id, telefono
      
    Returns
    -------
    afiliado : tuple

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
    """ Inserta los datos de un afiliado a la base de datos    

    Parameters
    ----------
    con : Conexion con la base de datos SQL
    afiliado : Tupla con la informacion del afiliado

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO afiliados (id ,nombre,apellidos ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado) VALUES(?, ?, ?, ?,?,?,?, ?, ?, ?,?)''',afiliado)
    con.commit()

def update_affiliate_vaccine(con):
    """ Actualiza el estado de vacunacion de un afiliado
    
    Recibe el id de afiliado del usuario y cambia el campo de vacunado a 'si'
        
    Parameters
    ----------
    con : Conexion con la base de datos SQL

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    vacunado=input("identificacion del afiliado vacunado: ")
    actualizar='update afiliados SET vacunado = "si" where id ='+vacunado
    cursorObj.execute(actualizar)
    con.commit()
    
def update_disaffiliated(con):
    """Actualiza la fecha de desafiliacion de un afiliado
    
    Recibe el id de afiliado del usuario y cambia el campo de desafiliacion a 
    la fecha en la que se realiza la solicitud de desafiliacion. 
    
    Parameters
    ----------
    con : conexion a la base de datos SQL

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    desafiliado=input("identificacion del afiliado a desafiliar: ")
    fecha = date_to_string(date.today())  
    print(fecha)      
    actualizar='update afiliados SET desafiliacion = "'+fecha+'" where id ='+desafiliado
    cursorObj.execute(actualizar)
    con.commit()

def sql_fetch_affiliate(con): 
    """Consulta la informacion de un afiliado de acuerdo a su id.
    
    Solicita el id del afiliado, e imprime la informacion asociada a ese afiliado.
    
    Parameters
    ----------
    con : conexion a la base de datos SQL

    Returns
    -------
    None.

    """
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

def create_table_vaccine_lot(con):
    """Funcion que crea una tabla para los lotes de vacunas
    
    Crea una tabla  con los siguentes encabezados:
    (lote, fabricante, tipo de vacuna, cantidad recibida, cantidad usada, dosis, 
    temperatura, efectividad, tiempo de proteccion, fecha de vencimiento, imagen)
    
    Parameters
    ----------
    con : Conexion a la base de datos SQL

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS lote_Vacuna(
                      lote integer PRIMARY KEY,
                      fabricante text,
                      tipo_vacuna text,
                      cantidad_recibida integer,
                      cantidad_usada integer,
                      dosis integer,
                      temperatura integer,
                      efectividad text,
                      tiempo_proteccion integer,
                      fecha_vencimiento text,
                      imagen text)""")
    con.commit()

def read_info_vaccine_lot():
    """Lee la informacion del lote de vacunas
    
    Recibe los datos dados por el usuario y los retorna como una tupla

    Returns
    -------
    lote_in : tuple

    """
    correct_type = False
    while not correct_type:   
        try:
            lote=(input("numero de lote: "))
            correct_type = True
        except:
            print('Entrada invalida, intentelo de nuevo')
    
    fabricante=(input("fabricante: "))
    
    tipo_vacuna=(input("tipo de vacuna: "))
    tipo_vacuna = tipo_vacuna.ljust(21)
    
    cantidad_recibida=(input("cantidad recibida: "))
    cantidad_recibida = cantidad_recibida.ljust(6)
    
    cantidad_usada=(input("cantidad usada: "))
    cantidad_usada = cantidad_usada.ljust(6)

    dosis=(input("dosis necesaria: "))
    dosis = dosis.ljust(1)
    
    temperatura=(input("temperatura: "))
    temperatura = temperatura.ljust(3)

    efectividad=(input("efectividad: "))
    efectividad = efectividad.ljust(3)
    efectividad = (str(efectividad))+"%"
        
    tiempo_proteccion=(input("tiempo de proteccion: "))
    tiempo_proteccion = tiempo_proteccion.ljust(3)

    fecha_vencimiento=read_date('de vencimiento')

    imagen=image(lote,fabricante, fecha_vencimiento)
    
    lote_in=(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen)
    return lote_in

def insert_vaccine_lot(con,vaccine):
    """ Inserta los datos de un lote de vacunacion en base de datos
    
    Parameters
    ----------
    con : Conexion a la base de datos SQL    
    vaccine : Tupla con la informacion del lote de vacunacion

    Returns
    -------
    None.

    """
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO lote_Vacuna(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen) VALUES (?,?,?,?,?,?,?,?,?,?,?)", vaccine)
    con.commit()
    
def sql_fetch_vaccine_lot(con):
    """Función que realiza un consulta en la base de datos teniendo en cuenta el numero de lote. 
    
    Solicita el numero de lote e imprime los elementos de la fila asociada al numero de lote.
    Muestra la imagen asociada a la fabricante con el numero de lote y su fecha de vencimiento.    
        
    Parameters
    ----------
    con : conexion a la base de datos SQL.

    Returns
    -------
    None.

    """
    
    cursorObj = con.cursor()
    num_lote=input("numero de lote a consultar: ")
    buscar='SELECT * FROM lote_Vacuna where lote='+num_lote
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    
    for row in filas:
               
        print(row[0:10])
        print('ruta de imagen: ' +row[10])
        
        img = Image.open(row[10])
        img.show()
    con.commit()    
    
def close_db(con):
    """Cierra la conexion a la base de datos
    

    Parameters
    ----------
    con : Conexion a la base de datos SQL

    Returns
    -------
    None.

    """
    con.close()    


##########################################################################################################
#                                        Presentation
##########################################################################################################

def clear_screen():
    """Limpia la consola

    identifica el sistema operativo en el que se trabaja y llama a la funcion de limpieza de consola.
    
    Returns
    -------
    None.

    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def menu():
    """
    Imprime el menu principal.

    Returns
    -------
    None.

    """
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
    """
    Imprime el menu de gestion de afiliados

    Returns
    -------
    None.

    """
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
    """
    Imprime el menu de nuevo afiliado

    Returns
    -------
    None.

    """    
    clear_screen()
    print('''#############################################################################################
                                     Nuevo Afiliado  
#############################################################################################
    Ingrese los datos del nuevo afiliado:
    
    
    ''')
    
def menu_state_affiliate():
    """
    Imprime el menu de estado de afiliado

    Returns
    -------
    None.

    """    
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
    """
    Imprime el menu de consulata de afiliado

    Returns
    -------
    None.

    """
    clear_screen()
    print('''#############################################################################################
                                     Consulta Afiliado  
#############################################################################################
    Ingrese el numero de identificacion del afiliado para ver su informacion:
    
    
    ''')

def menu_vaccine():
    """
    Imprime el menu de gestion de lotes de vacunacion

    Returns
    -------
    None.

    """
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
    """
    Imprime el menu de nuevo lote de vacunacion

    Returns
    -------
    None.

    """
    clear_screen()
    print('''#############################################################################################
                                     Nuevo lote de vacunas 
#############################################################################################
    
    Ingrese el nuevo lote de vacunacion:
    
    ''')
    
def menu_info_vaccine():
    """
    Imprime el menu de consulta lote de cavunacion

    Returns
    -------
    None.

    """
    clear_screen()
    print('''#############################################################################################
                                     Consultar lote de vacunas 
#############################################################################################
    
    Ingrese el numero de lote de vacunacion a consultar:
    
    ''')    
    
def menu_plan_vaccine():
    """
    Imprime el menu de gestion del plan de vacunacion

    Returns
    -------
    None.

    """
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
    """
    Imprime el menu de nuevo plan de vacunacion

    Returns
    -------
    None.

    """
    clear_screen()
    print('''#############################################################################################
                                     Nuevo Plan de vacunas 
#############################################################################################
    
    Ingrese el nuevo lote de vacunacion:
    
    ''')
    
def menu_info_plan_vaccine():
    """
    Imprime el menu de consultar plan de vacunacion

    Returns
    -------
    None.

    """
    clear_screen()
    print('''#############################################################################################
                                     Consultar Plan de vacunas 
#############################################################################################
    
    Ingrese el numero de plan de vacunacion a consultar:
    
    ''')  

def menu_calendar_vaccune():
    """
    Imprime el menu de calendario de vacunacion

    Returns
    -------
    None.

    """
    print('''#############################################################################################
                                     Calendario de vacunacion
#############################################################################################
    
    Programacion de citas de vacunacion
    
    ''')
    
##########################################################################################################
#                                        Bussisnes logic
##########################################################################################################
def image(lote,fabricante, fecha_vencimiento):
    """Funcion para crear e ingresar una imagen de acuerdo a numero de lote, el fabricante y la fecha de vencimiento
    
    Utilizando la libreria pill, crea una imagen de acuerdo al fabricante, y le 
    añade el numero de lote y fecha de vencimiento a la imagen
    
    Parameters
    ----------
    lote : numero de lote.
    fabricante : nombre del fabricante.
    fecha_vencimiento : fecha de vencimiento del lote.

    Returns
    -------
    ruta : la ruta en la que se guardo la imagen.

    """
     
    
    img = Image.new('RGB', (200, 150), "white")
        #crea una plantilla en blanco llamada img
    im = Image.open('fabrica/'+fabricante+'.jpg')
        #trae la imagen asociada al fabricante
    img.paste(im,(0,0))
        #inserta la imganen en la plantilla
    fnt = ImageFont.truetype('fuente/Arial.ttf', 12)
        #define la fuente del texto
    d=ImageDraw.Draw(img)
        #nombra el metodo para escribir como d
    d.text((2, 100),'Fecha de vencimiento: '+str(fecha_vencimiento), font=fnt, fill=(0, 0, 0))
        #escribe la fecha de vencimiento
    d.text((2, 125),'No.lote: ' +str(lote), font=fnt, fill=(0, 0, 0))
        #escribe el numero de lote
    img.save('imagenes/'+str(lote)+'.jpg')
        #guarda la imagen creada en la carpeta imagenes
    ruta='imagenes/'+str(lote)+'.jpg'
        #nombra la ruta donde se guardo la imagen creada  
    return ruta

def date_to_string(date):
    """
    Funcion que convierte un objeto fecha a un string en formato dd/mm/aaaa.

    Parameters
    ----------
    date : objeto tipo fecha

    Returns
    -------
    new_date_string : string dd/mm/aaaa.

    """
    f = date.isoformat().split('-')
    new_date_string = str(f[2])+'/'+str(f[1])+'/'+str(f[0])
    return new_date_string

def read_date(word):
    """
    Funcion que lee una fecha ingresada por el usuario y la retorna en formato de texto DD/MM/AAAA

    Imprime un encabezado con el tipo de fecha que solicita, y pide al usuario 
    ingresar el dia, mes y año. Comprobando que se ingresen datos numericos. 
    Retorna un string con el frmato de fecha  DD/MM/AAAA
    
    Parameters
    ----------
    word : string tipo de fecha.

    Raises
    ------
    Fecha fuera de rango o cuando se ingresan valores no numericos en la fecha

    Returns
    -------
    date_aux: String fecha

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
                    raise 
            except:
                print('Entrada invalida, intentelo de nuevo')         
                  
        date_aux =ano+"-"+mes+"-"+dia
        
   
        if date_aux == '0000-00-00':
            correct_date = True
        elif date.fromisoformat(date_aux) > date.today():
            print('Fecha fuera de rango, intentelo de nuevo.')
        else:
            correct_date = True
            
    date_aux =dia+"/"+mes+"/"+ano          
    return date_aux

    
def main():    
    
    con=sql_connection()
    create_table_affiliate(con)
    create_table_vaccine_lot(con)
    
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
                    vaccine=read_info_vaccine_lot()
                    insert_vaccine_lot(con,vaccine)
                    input('Presione cualquier tecla para continuar...')
                elif(option == '2'): #consultar lote vacunacion
                    menu_info_vaccine()
                    sql_fetch_vaccine_lot(con)
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
