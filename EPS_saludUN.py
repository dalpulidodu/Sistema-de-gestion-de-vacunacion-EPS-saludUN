"""
Creado por:
    
    Luis Alfonso Ramirez Herrera
    Sergio Alejandro Reita Serrano
    David Lizzane Pulido Duquino
    Carlos Jesus Ramirez Guerrero
"""
from datetime import time
from datetime import date
from datetime import timedelta
from datetime import datetime

import os
import sqlite3
from sqlite3 import Error

from PIL import Image, ImageDraw, ImageFont

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
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
    con : sqlite3.Connection
    """
    try:
        con = sqlite3.connect('db.db')
        print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha prodicido un error al crear la conexion',Error)

def create_table_affiliate(con):
    """Crea una tabla con los parametros de un afiliado
    
    Encabezado de la tabla:
    (id,nombre, apellidos,direccion, telefono, email, ciudad, nacimiento,fecha de afiliacion, fecha de desafiliacion, vacunado)
    
    Parameters
    ----------
    con : sqlite3.Connection Conexion con la base de datos SQL
    Returns
    -------
    None.
    """
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS afiliados(id integer PRIMARY KEY,nombre text,apellidos text,direccion text,telefono real,email text, ciudad text,nacimiento text,afiliacion text,desafiliacion text,vacunado text)")
    con.commit()
 
def read_info_affiliate(con):  
    """Lee la informacion de un afiliado.
    
    Retorna una tupla con los datos del afiliado. Con fecha de desafiliacion por defecto 00/00/0000 y estado vacunado 'no'
    
    Excepct
    -------
    TypeError : Cuando se ingresan letras en vez de numeros en los datos de id, telefono
      
    Returns
    -------
    afiliado : tuple
    """
    
    cursorObj = con.cursor()
    #id afiliado        
    correct_type = False
    while correct_type==False:
        try:
            i=int(input("numero de identificacion: "))
            if len(str(i))>12:
                print('''la información suministrada no debe ser mayor a doce digitos
                            intente de nuevo...''')
            else:
                id=str(i)
                if int(id) < 0:
                    print('Debe ser un numero positivo')
                else:
                    buscar_afiliado='SELECT * FROM afiliados' 
                    cursorObj.execute(buscar_afiliado)
                    afiliados = cursorObj.fetchall()
                    for row in afiliados:
                        if int(id)==row[0]:
                            print("Número de identificación repetido")
                            raise    
                    correct_type = True
        except:
            print('''la información suministrada solamente debe tener números
                       intente de nuevo...''')
    #nombre                  
    nombre=(input("nombre: "))
    if len(nombre)>20:
        nombre=nombre[:20]
    else:
        nombre = nombre.ljust(20)
    #apellido
    apellido=(input("apellido: "))
    if len(apellido)>20:
        apellido=apellido[:20]
    else:
        apellido = apellido.ljust(20)
    #direccion
    direccion=(input("direccion: "))
    if len(direccion)>20:
        direccion=direccion[:20]
    else:
        direccion = direccion.ljust(20)
    #telefono
    correct_type = False
    while not correct_type:   
        try:
            t=int(input("telefono: "))
            if len(str(t))>12:
                print('''la información suministrada no debe ser mayor a doce digitos
                            intente de nuevo...''')
            if t < 0:
                    print('Debe ser un numero positivo')
            else:
                telefono=str(t)
                telefono = telefono.ljust(12)
                correct_type = True
        except:
            print('Entrada invalida, intentelo de nuevo')
    #email       
    correct_type=False
    while correct_type==False:
    
        email=(input("email: "))
        
        if email.find("@")>=0 and email.find(".")>=0:
            email = email.ljust(20)
            correct_type=True
        else:
            print('''El correo debe tener un '@' y un '.' para que sea válido
                        intentelo de nuevo''')        
    #ciudad
    ciudad=(input("ciudad: "))
    if len(ciudad)>20:
        ciudad=ciudad[:20]
    else:
        ciudad = ciudad.ljust(20) 
    #fecha de nacimiento
    print('Fecha de nacimiento: ')
    nacimiento = read_date('antes')
    #fecha de afiliacion
    print('Fecha afiliacion: ')
    afiliacion = read_date('antes')
    #fecha de desafiliacion
    desafiliacion = '00/00/0000'        
    #estado de vacunacion
    vacunado='no'

    con.commit()
            
    afiliado=(id ,nombre,apellido ,direccion,telefono ,email, ciudad ,nacimiento,afiliacion,desafiliacion,vacunado )
    
    return afiliado

def insert_affiliate(con,afiliado):
    """ Inserta los datos de un afiliado a la base de datos    
    Parameters
    ----------
    con : sqlite3.Connection
    afiliado : tuple 
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
    con : sqlite3.Connection
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
    """Imprime la informacion de un afiliado de acuerdo a su id.
        
    Parameters
    ----------
    con : sqlite3.Connection
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
    con : sqlite3.Connection
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

def read_info_vaccine_lot(con):
    """Lee la informacion del lote de vacunas
    
    Recibe los datos dados por el usuario y los retorna como una tupla
    
    Returns
    -------
    lote_in : tuple
    """

    cursorObj=con.cursor()
    
    #lote
    correct_type = False
    while not correct_type:   
        try:
            i=int(input("numero de lote: "))
            if len(str(i))>12:
                print('''El número del lote no debe ser mayor a doce dígitos''')
            else:
                lote=str(i)
                lote=lote.ljust(12)
                if int(lote) < 0:
                    print('Debe ser un numero positivo')
                else:
                    buscar_lote='SELECT * FROM lote_Vacuna' 
                    cursorObj.execute(buscar_lote)
                    lotes = cursorObj.fetchall()
                    for row in lotes:
                        if int(lote)==row[0]:
                            print("Número de identificación repetido")
                            raise
                    correct_type = True
        except:
            print('Entrada invalida, intentelo de nuevo')
            
    #fabricante
    lista= {'1':'Sinovac', '2':'Pfizer', '3':'Moderna', '4':'SputnikV', '5':'AstraZeneca', '6':'Sinopharm', '7':'Covaxim'}
    correct_type = False
    while not correct_type:
        menu_factory()
        option = input("Ingrese el numero correspondiente: ")
        if option in lista:
            fabricante = lista[option]
            correct_type = True
        else: 
            print("Opción no valida, por favor ingrese un valor valido")
            
    #tipo de vacuna     
    lista= {'Sinovac':'Virus desactivado', 'Pfizer':'ARN/ADN', 'Moderna':'ARN/ADN', 'SputnikV':'Vector viral', 'AstraZeneca':'Vector viral','Sinopharm':'Virus desactivado','Covaxim':'Virus desactivado'}
    option = fabricante
    tipo_vacuna = lista[option]
    
    #cantidad recibida
    correct_type = False
    while not correct_type:   
        try:
            i=int(input("Cantidad recibida: "))
            if i < 0:
                print('Debe ser un numero positivo')
            else:
                cantidad_recibida=str(i)
                cantidad_recibida=cantidad_recibida.ljust(6)
                correct_type = True
        except:
            print('Entrada invalida, por favor digite solo numeros enteros')
            
    #cantidad usada
    cantidad_usada=0
    
    #dosis necesaria ---- todas son 2, en intervalos diferentes
    lista= {'Sinovac':' en 21 dias', 'Pfizer':' en 21 dias', 'Moderna':' en 28 dias', 'SputnikV':' en 21 dias', 'AstraZeneca':'Vector viral','Sinopharm':'Virus desactivado','Covaxim':'Virus desactivado'}
    option = fabricante
    dosis = '2'+lista[option]
    
    #temperatura
    lista= {'Sinovac':'8°C', 'Pfizer':'8°C', 'Moderna':'-25°C', 'SputnikV':'-18°C', 'AstraZeneca':'8°C', 'Sinopharm':'8°C', 'Covaxim':'40°C'}
    option = fabricante
    temperatura = lista[option]
    
    #efectividad
    lista= {'Sinovac':'50.38%', 'Pfizer':'95%', 'Moderna':'95%', 'SputnikV':'91%', 'AstraZeneca':'76%', 'Sinopharm':'79%', 'Covaxim':'81%'}
    option = fabricante
    efectividad = lista[option]
    
    #tiempo de proteccion
    correct_type = False
    while not correct_type:   
        try:
            i=int(input("Tiempo de proteccion en meses: "))
            if i < 0:
                print('Debe ser un numero positivo')
            else:
                tiempo_proteccion=str(i)
                tiempo_proteccion=tiempo_proteccion.ljust(2)+' meses'
                correct_type = True
        except:
            print('Entrada invalida, por favor digite solo numeros enteros')
            
    #fecha de vencimiento
    print('Fecha de vencimiento: ')
    fecha_vencimiento=read_date('despues')
    
    #ruta de la imagen
    imagen=image(lote,fabricante, fecha_vencimiento)

    con.commit()
    
    lote_in=(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen)
    
    return lote_in

def insert_vaccine_lot(con,vaccine):
    """ Inserta los datos de un lote de vacunacion en la base de datos
    
    Parameters
    ----------
    con : sqlite3.Connection   
    vaccine : tuple
    
    Returns
    -------
    None.
    """
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO lote_Vacuna(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen) VALUES (?,?,?,?,?,?,?,?,?,?,?)", vaccine)
    con.commit()


def update_increment_lot(con,lote,y):
    """ actualiza el numero de vacunas usadas en la base de datos
    
    Parameters
    ----------
    con : sqlite3.Connection   
    lote : id del lote
    y : numero de vacunas
    
    Returns
    -------
    None.
    """

    cursorObj = con.cursor()
    s=y*2
    actualizar='update Lote_Vacuna SET cantidad_usada = "'+str(s)+'" where lote ='+str(lote)
    cursorObj.execute(actualizar)
    con.commit()
    
def sql_fetch_vaccine_lot(con):
    """Imprime la informacion de un lote de vacunacion de acuerdo con su numero de lote. 
    
    Solicita el numero de lote e imprime los elementos de la fila asociada al numero de lote.
    Muestra la imagen asociada a la fabricante con el numero de lote y su fecha de vencimiento.    
        
    Parameters
    ----------
    con : sqlite3.Connection
    
    Returns
    -------
    None.
    """
    
    cursorObj = con.cursor()
    num_lote=input("numero de lote a consultar: ")
    buscar='SELECT * FROM lote_Vacuna where lote='+num_lote
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    header=('Numero de lote: ', 'Fabricante: ','Tipo de vacuna: ', 'Cantidad recibida: ','Cantidad usada: ', 'Dosis: ','Temperatura: ','Efectividad: ', 'Tiempo de protección: ', 'Fecha de vencimiento: ',  'Imagen: ')
    for row in filas:
        for i in range(11):            
            print(header[i]+''+str(row[i]))
        img = Image.open(row[10])
        img.show()
    con.commit()
  
def create_table_plan_vaccine(con): 
    """Crea una tabla para los planes de vacunación
    
    Crea una tabla  con los siguentes encabezados:
    (id_plan, edad_min, edad_max, fecha_inicio, fecha_final)
    
    Parameters
    ----------
    con : sqlite3.Connection
    
    Returns
    -------
    None.
    """
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS planes (idplan integer PRIMARY KEY,edad_min integer, edad_max integer, fecha_inicio text, fecha_final text)")
    con.commit()

def insert_plan_vaccine(con, plan): 
    """ Inserta los datos de un plan de vacunación a la base de datos 
    
    Parameters
    ----------
    con : sqlite3.Connection    
    plan : tuple
    
    Returns
    -------
    None.
    """
        
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO planes(idplan,edad_min, edad_max, fecha_inicio, fecha_final) VALUES(?, ?, ?, ?,?)',plan)    
    con.commit()

def read_info_plan(con):  
    """Lee la informacion de un plan de vacunación.
    
    Retorna una tupla con los datos del plan de vacunación.

    Parameters
    ----------
    con : sqlite3.Connection    
      
    Returns
    -------
    planes : tuple
    """
    
    cursorObj = con.cursor()
    
    #id plan de vacunacion
    correct_type = False
    while not correct_type:   
        try:
            i=int(input("numero de identificacion del plan: "))
            idplan = str(i)
            if len(idplan)>3:
                print('''El id del plan debe ser de máximio 3 digitos''')
            else:
                idplan = idplan.ljust(3)
                if int(idplan) < 0:
                    print('Debe ser un numero positivo')
                else:
                    buscar_plan='SELECT * FROM planes' 
                    cursorObj.execute(buscar_plan)
                    planes = cursorObj.fetchall()
                    for row in planes:
                        if int(idplan)==row[0]:
                            print("Número de identificación repetido")
                            raise
                    correct_type = True         
        except:
            print('Entrada invalida, intentelo de nuevo')
            
    #verificacion de rango de edad       
    correct_plan=False
    while not correct_plan:


        #edad minima plan de vacunacion
        correct_type2 = False
        while not correct_type2:   
            try:
                i=int(input("edad mínima: "))
                if i < 0:
                    print('Debe ser un numero positivo')
                else:
                    edad_min = str(i)
                    edad_min = edad_min.ljust(3)
                    correct_type2 = True
            except:
                print('Entrada invalida, intentelo de nuevo')
            
        #edad maxima plan de vacunacion
        correct_type3 = False
        while not correct_type3:   
            try:
                i=int(input("edad máxima: "))
                if i < 0:
                    print('Debe ser un numero positivo')
                elif int(edad_min)>= i:
                    print('''La edad maxima debe ser mayor a la edad minima
                            intentelo de nuevo...''')
                else:
                    edad_max = str(i)
                    edad_max = edad_max.ljust(3)
                    correct_type3 = True
            except:
                print('Entrada invalida, intentelo de nuevo')
                
        #rango de edad       
        try:
            buscar_plan='SELECT * FROM planes' 
            cursorObj.execute(buscar_plan)
            planes = cursorObj.fetchall()
            for row in planes:
                if (int(edad_min) > row[2]) or (int(edad_max) < row[1]):
                    continue
                else:
                    raise
            correct_plan=True
        except:
            print('''El rango de edad interfiere con otros planes
                        intentelo de nuevo...''')


    correct_type4=False
    #fecha inicio plan de vacunacion
    print('Fecha inicio plan de vacunacion: ')
    fecha_inicio = read_date('despues')
    
    while correct_type4==False:
        #fecha final plan de vacunacion
        print('Fecha final plan de vacunacion: ')
        fecha_final = read_date('despues')       
        if datetime.strptime(fecha_inicio,'%d/%m/%Y')>datetime.strptime(fecha_final,'%d/%m/%Y'):
            print('''La fecha de inicio no puede ser mayor a la fecha final... ''')
        else:
            correct_type4=True

    con.commit()
       
    planes=(idplan,edad_min,edad_max,fecha_inicio,fecha_final)
    
    return planes

def sql_fetch_plan(con): 
    """Imprime la informacion de un plan de vacunacion de acuerdo a su id.
        
    Parameters
    ----------
    con : sqlite3.Connection
    
    Returns
    -------
    None.
    """
    cursorObj = con.cursor()
    plan=input("id del plan a consultar: ")
    buscar='SELECT * FROM planes where idplan= '+plan
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    print()
    header=('idplan: ', 'edad_min: ','edad_max: ', 'fecha_inicio: ','fecha_final:')
    for row in filas:
        for i in range(5):            
            print(header[i]+''+str(row[i]))
    con.commit()
    print()
    
def create_calendar(con): 
    """Crea el calendario de vacunacion
    
    filtra los afiliados disponibles de acuerdo con el plan de vacunacion y la
    disponibilidad de vacunas y les asigna una cita. Retorna la informacion
    (fecha,idafiliado,nombre,apellido,ciudad,direccion,telefono,correo,fabricante,no lote)
    Parameters
    ----------
    con : sqlite3.Connection
    Returns
    -------
    calendario : list
    """
    cursorObj = con.cursor()
    
    #Fecha de inicio del calendario de vacunacion
    print('Fecha de inicio calendario de vacunacion: ')
    fecha_inicio = read_date('despues')
    #Hora de inicio del calendario de vacunacion
    print('Hora de inicio calendario de vacunacion: ')
    hora_inicial = read_hour()    
    
    #Busqueda de afiliados no vacunados y no desafiliados
    buscar_afiliado='SELECT * FROM afiliados WHERE vacunado="no" and desafiliacion="00/00/0000" '
    cursorObj.execute(buscar_afiliado)
    afiliados = cursorObj.fetchall()
        
    #filtra los planes a partir de la fecha de inicio de la agenda   
    buscar_plan='SELECT * FROM planes' 
    cursorObj.execute(buscar_plan)
    all_planes = cursorObj.fetchall()
    planes_habilitados = []
    for row in all_planes:
        plan = []
        if string_to_date(row[4]) >= string_to_date(fecha_inicio):
            plan = list(row)
            if string_to_date(row[3]) <= string_to_date(fecha_inicio):                       
                plan[3] = fecha_inicio 
            planes_habilitados.append(plan)
    
    #calcula los usuarios validos para vacunacion por edad en el plan de vacuancion y les asigna su plan de vacunacion
    afiliados_habilitados = []
    for plan in planes_habilitados:
        for afiliado in afiliados:                
                if calculate_age(afiliado)>=plan[1] and calculate_age(afiliado)<plan[2]:
                    afiliado_aux =list(afiliado)
                    afiliado_aux.append(plan[3])#agrega la fecha inicial de posible vacunacion
                    afiliado_aux.append(plan[4])#agrega la fecha final de posible vacunacion
                    afiliados_habilitados.append(afiliado_aux)                    
    
    
    #cálculo de fecha y hora para los afiliados habilitados
    citas = {}   
    for afiliado in afiliados_habilitados:        
        agenda = date_complete(afiliado[11],str(hora_inicial))#se identifica la fecha  y hora  inical
        
        #valida en que fecha el afiliado puede vacunarse
        while agenda < date_complete(afiliado[12],str(hora_inicial)):
            
            if (agenda not in citas.keys()):#si no existe nadie en esa fecha se asigna
                citas[agenda] = afiliado                
                break
            else:
                agenda += timedelta(hours=1) 
            
    fechas_citas = sorted(citas.keys()) #fecha de las citas de forma ordenada 
               
    #asignacion de vacunas       
    buscar_plan='SELECT * FROM lote_Vacuna' 
    cursorObj.execute(buscar_plan)
    vacunas = cursorObj.fetchall()    
    calendario = []
    indice = 0
    for vacuna in vacunas:
        dosis_disponibles = vacuna[3]//2 #como son 2 dosis por persona la cantidad se reduce a la mitad
        while indice < len(citas):
            if dosis_disponibles > 0:
                #fecha|idafiliado|nombre|apellido|ciudad|direccion|telefono|correo|fabricante|no lote
                cita = fechas_citas[indice]               
                calendario.append((cita,citas[cita][0],citas[cita][1],citas[cita][2],citas[cita][6],citas[cita][3],citas[cita][4],citas[cita][5],vacuna[0],vacuna[1]))
                update_increment_lot(con,vacuna[0],len(citas))
                dosis_disponibles -= 1
                indice += 1
            else:
                break
    return calendario
    
def date_complete(f,h):
    """
    Crea un formato hora fecha del tipo datetime.
    Parameters
    ----------
    f : string fecha
    h : string hora
    Returns
    -------
    fecha_completa : datetime
    """
    h = h.split(':')#convierte la hora inical en una lista
    f = f.split('/')#convierte la fecha de inicio en una lista
    fecha_completa = datetime(int(f[2]),int(f[1]),int(f[0]),int(h[0]),int(h[1]))
    return fecha_completa
    
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
    Identifica el sistema operativo en el que se trabaja y llama a la funcion de limpieza de consola.
    
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
    Imprime el menu de consulta de afiliado
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
    Imprime el menu de consulta lote de vacunacion
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
    2. Consulta del plan de vacunacion
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
    clear_screen()
    print('''#############################################################################################
                                     Calendario de vacunacion
#############################################################################################
    
    Programacion de citas de vacunacion
    1. Consulta general calendario de vacunacion
    2. Consulta individual calendario de vacunacion
    3. Crear calendario de vacunacion
    4. Enviar correos
    b. Volver al menu anterior
    e. Salir
    
    ''')
    
def menu_calendar_vaccune_general():
    """
    Imprime el menu de Consulta general calendario de vacunacion
    Returns
    -------
    None.
    """   
    clear_screen()
    print('''#############################################################################################
                                     Consulta general calendario de vacunacion
#############################################################################################
    
    Ordenar calendario por
    
    0. Fecha
    1. Id afiliado
    2. Nombre afiliado
    3. Apellido afiliado
    4. Ciudd de vacunacion
    5. Direccion de residencia
    6. Telefono de contacto
    7. Correo de contacto
    8. Vacuna asignada
    9. Numero de lote de vacuna
    
    ''')    
    
def menu_calendar_vaccune_individual():
    """
    Imprime el menu de Consulta individual calendario de vacunacion
    Returns
    -------
    None.
    """
    clear_screen()
    print('''#############################################################################################
                                     Consulta individual calendario de vacunacion
#############################################################################################
    
    Consulta por Id de afiliado el calendario de vacunacion
    ''')   
    
def menu_new_calendar_vaccune():
    """
    Imprime el menu de Crear nuevo calendario de vacunacion
    Returns
    -------
    None.
    """
    clear_screen()
    print('''#############################################################################################
                                     Crear nuevo calendario de vacunacion
#############################################################################################
    
     Ingrese la fecha de inicio  y el horario de atención para crear el nuevo 
     calendario de vacunacion.
     
    ''')       

def menu_factory():
    """
    Imprime el menu de seleccion de fabricas
    Returns
    -------
    None.
    """
    print('''  Fabricas:
        1. Sinovak 
        2. Pfizer 
        3. Moderna 
        4. Sputnik V 
        5. AstraZeneca 
        6. Sinopharm 
        7. Covaxim 
    
    ''')   
 
def menu_send_mail():
    """
    Imprime el menu de enviar correos
    Returns
    -------
    None.
    """
    clear_screen()
    print('''#############################################################################################
                                     Enviar Emails
#############################################################################################
         
    ''')  

def print_individual_calendar(calendario):
    """
    Recibe el id del afiliado e imprime la informacion de su cita de vacunacion, 
    los datos del afiliado y la vacuna que se aplicará.
    Parameters
    ----------
    calendario : list
    Returns
    -------
    None.
    """
    idafiliado = input('Ingrese el id del afiliado a consultar: ')
    none_afiliado = True   
    for row in calendario:
        if idafiliado == str(row[1]):
            #fecha|idafiliado|nombre|apellido|ciudad|direccion|telefono|correo|fabricante|no lote
            fecha = str(row[0].day)+'/'+str(row[0].month)+'/'+str(row[0].year)
            hora = str(row[0].hour)+':'+str(row[0].minute)
            print('Fecha de vacunacion: ',fecha)
            print('Hora de vacunacion: ',hora)
            print('Ciudad de vacunacion: ', row[4])
            print('Id afiliado: ', row[1])
            print('Nombre afiliado: ', row[2])
            print('Apellido afiliado: ', row[3])
            print('Direccion de residencia: ', row[5])
            print('Telefono afiliado: ', row[6])
            print('Correo de contacto: ', row[7])
            print('Vacuna aplicada: ', row[8])
            print('Lote de vacuna: ', row[9])  
            none_afiliado = False
    if none_afiliado or len(calendario)==0:
        print("No hay ninguna cita vigente para el afiliado con identificacion: ", idafiliado )            

def print_general_calendar(calendario,indice_orden):
    """
    Imprime los datos ordenados de acuerdo con el indice de ordenamiento.
    Parameters
    ----------
    calendario : list
    indice_orden : integer
    Returns
    -------
    None.
    """
    if len(calendario)==0:
        print("No hay un calendario vigente.")
    else:
        #organiza la lista
        ordenados = sorted(calendario, key=lambda c : c[indice_orden])       
        for row in ordenados:            
            #fecha|idafiliado|nombre|apellido|ciudad|direccion|telefono|correo|fabricante|no lote
            fecha = str(row[0].day)+'/'+str(row[0].month)+'/'+str(row[0].year)
            hora = str(row[0].hour)+':'+str(row[0].minute)
            print('Fecha de vacunacion: ',fecha)
            print('Hora de vacunacion: ',hora)
            print('Ciudad de vacunacion: ', row[4])
            print('Id afiliado: ', row[1])
            print('Nombre afiliado: ', row[2])
            print('Apellido afiliado: ', row[3])
            print('Direccion de residencia: ', row[5])
            print('Telefono afiliado: ', row[6])
            print('Correo de contacto: ', row[7])
            print('Vacuna aplicada: ', row[8])
            print('Lote de vacuna: ', row[9]) 
            print('---------------------------------------------------------------------------')
            
         
##########################################################################################################
#                                        Bussisnes logic
##########################################################################################################
def send_mail(calendario):
    """
    Envia un correo a cada afiliado con la fecha, hora y ciudad de vacunacion 
    establecidas en el calendario de vacunacion, e imprime si el envio fue exitoso 
    Parameters
    ----------
    calendario : list
    Returns
    -------
    None.
    """
       
    for row in calendario:
                
        # crea una instancia de objeto message
        msg = MIMEMultipart()
        #fecha|idafiliado|nombre|apellido|ciudad|direccion|telefono|correo|fabricante|no lote
        
        fecha  = row[0]
        idafiliado = str(row[1])
        nombre = str(row[2])
        apellido = str(row[3])
        ciudad = str(row[4])
        correo = str(row[7])
        
        message = "Señor afiliado "+nombre+' '+ apellido+' identificado con '+ idafiliado
        message += ' , tiene una cita de vacunacion el dia '+str(fecha.day)+'/'+str(fecha.month)+'/'+str(fecha.year)+ ' a la hora '+str(fecha.hour)+':'+str(fecha.minute)+' en la ciudad ' + ciudad
        message += '. Att: EPS UN'
        
        # configura los parametros del mensaje
        password = "proyectopoo"
        msg['From'] = "vacunacionepssaludun@gmail.com"
        msg['To'] = correo
        msg['Subject'] = "Cita de vacunacion"
         
        # añade al mensaje el cuerpo del mensaje
        msg.attach(MIMEText(message, 'plain'))
         
        #crea un servidor
        server = smtplib.SMTP('smtp.gmail.com: 587')
         
        server.starttls()
         
        # Credenciales de inicio de sesion para enviar el email
        server.login(msg['From'], password)
         
         
        # envia el mensaje via server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
         
        server.quit()
         
        print ("successfully sent email to: " + msg['To'])
   
def calculate_age(afiliado):
    """
    Calcula la edad de un afiliado.
    Parameters
    ----------
    afiliado : tuple
    Returns
    -------
    edad : integer
    """
    dias = (date.today()- string_to_date(afiliado[7])).days    
    edad= dias // 365    
    return edad
 
def image(lote,fabricante, fecha_vencimiento):
    """Crear una imagen de acuerdo a numero de lote, el fabricante y la fecha de vencimiento
        
    Parameters
    ----------
    lote : integer
    fabricante : string
    fecha_vencimiento : date
    Returns
    -------
    ruta : string  ruta en la que se guarda la imagen.
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
    date : date
    Returns
    -------
    new_date_string : string dd/mm/aaaa.
    """
    f = date.isoformat().split('-')
    new_date_string = str(f[2])+'/'+str(f[1])+'/'+str(f[0])
    return new_date_string

def string_to_date(str_date):
    """
    Retorna un objeto date de acuerdo a una fecha de tipo string
    Parameters
    ----------
    str_date : string
    Returns
    -------
    new_date : date
    """    
    f = str_date.split('/')    
    new_date = date.fromisoformat(str(f[2])+'-'+str(f[1])+'-'+str(f[0]))
    
    return new_date

def read_date(type_date):
    """
    Funcion que lee una fecha ingresada por el usuario y la retorna en formato de texto DD/MM/AAAA
    Comprueba que se ingresen datos numericos. 
    Si type_date es 'antes' valida que las entradas de fechas sean menores 
    a la fecha en la que se hace la solicitud. Si type_date es 'despues'  
    valida que las entradas de fechas sean mayores  a la fecha en la que se 
    hace la solicitud.
    
    Parameters
    ----------
    type_date : string - tipo de fecha 
    Raises
    ------
    Fecha fuera de rango o cuando se ingresan valores no numericos en la fecha
    Returns
    -------
    date_aux: string - fecha
    """
    
    correct_date = False
    while not correct_date :
        correct_type = False
        while not correct_type:   
            try:
                d=int(input("dia: "))
                if(d>0 and d<=31):
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
                m=int(input("mes: "))
                if(m>0 and m<=12):
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
                
                a=int(input("ano: "))
                if(a>0):
                    ano = str(a)
                    ano= ano.rjust(4,"0")
                    correct_type = True
                else:
                    raise 
            except:
                print('Entrada invalida, intentelo de nuevo')         
                  
        date_aux =ano+"-"+mes+"-"+dia
        
        if (type_date =='despues'):
            if date.fromisoformat(date_aux) < date.today():
                print('La fecha ingresada es anterior a la fecha actual, intentelo de nuevo.')
            else:
                correct_date = True
        elif (type_date =='antes'):
            
            if date.fromisoformat(date_aux) > date.today():
                print('La fecha ingresada es posterior a la fecha actual, intentelo de nuevo.')
            else:
                correct_date = True
            
    date_aux =dia+"/"+mes+"/"+ano          
    return date_aux

def read_hour():
    """
    Lee la hora y la retorna en un tipo time
    Raises
    ------
    
        Error cuando los valores ingresados no estan dentro del rango de horas o minutos
    Returns
    -------
    hora_aux : time
    """    
    correct_type = False
    while not correct_type:   
        try:
            h=int(input("hora: "))
            if(h>=0 and h<=24):
                correct_type = True
            else:                    
                raise 
        except:
            print('Entrada invalida, intentelo de nuevo')
            
    correct_type = False
    while not correct_type:   
        try:
            m=int(input("minuto: "))
            if(m>=0 and m<=60):
                correct_type = True
            else:                    
                raise 
        except:
            print('Entrada invalida, intentelo de nuevo')
            
    hora_aux = time(h,m,0)
    
    return hora_aux 
    
def main():
    """
    Funcion principal con la logica del menu y el llamado a otras funciones
    Returns
    -------
    None.
    """    
       
    con=sql_connection()    
    create_table_affiliate(con)
    create_table_vaccine_lot(con)
    create_table_plan_vaccine(con)
    calendario = []
    
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
                    afiliado=read_info_affiliate(con)
                    insert_affiliate(con,afiliado)
                    input('Nuevo afiliado registrado. Presione cualquier tecla para continuar...')
                    
                elif(option == '2'): # Actualizar estado de afiliado
                    
                    back = False
                    while not back:
                        menu_state_affiliate()
                        option = input('Ingrese una opcion: ')
                        if(option=='1'): #Vacunacion
                            update_affiliate_vaccine(con)
                            input('Presione Enter para continuar...')
                        elif(option == '2'): #Desafiliacion
                            update_disaffiliated(con)
                            input('Presione Enter para continuar...')
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
                    input('Presione Enter para continuar...')
                    
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
                    vaccine=read_info_vaccine_lot(con)
                    insert_vaccine_lot(con,vaccine)
                    input('Presione Enter para continuar...')
                elif(option == '2'): #consultar lote vacunacion
                    menu_info_vaccine()
                    sql_fetch_vaccine_lot(con)
                    input('Presione Enter para continuar...')
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
                    plan = read_info_plan(con)
                    insert_plan_vaccine(con, plan)
                    input('Presione Enter para continuar...')
                    
                elif(option == '2'): #consultar plan de vacunacion
                    menu_info_plan_vaccine()
                    sql_fetch_plan(con)
                    input('Presione Enter para continuar...')
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')
                    
        elif(option == '4'): #menu calendario de vacunacion             
           
            back = False
            while not back:
                menu_calendar_vaccune()               
                    
                #Organizar e ingresar los datos en la tabla calendario
    
                option = input('Ingrese una opcion: ')
                if(option=='1'): #consulta general calendario                    
                    
                    if len(calendario)==0:
                        print('No hay un calendario de vacunaion vigente')
                        input('Presione Enter para continuar...')
                    else: 
                        menu_calendar_vaccune_general()
                        opciones = {'0':'Ordenado por fecha',
                                    '1':'Ordenado por id afiliado',
                                    '2':'Ordenado por nombre',
                                    '3':'Ordenado por apellido',
                                    '4':'Ordenado por ciudad',
                                    '5':'Ordenado por direccion',
                                    '6':'Ordenado por telefono',
                                    '7':'Ordenado por correo',
                                    '8':'Ordenado por fabricante',
                                    '9':'Ordenado por lote'}
                        
                        
                        #fecha|idafiliado|nombre|apellido|ciudad|direccion|telefono|correo|fabricante|no lote
                        while True:
                            option = input('Ingrese la opcion de ordenamiento')
                            if option in opciones.keys():
                                clear_screen()
                                print('    '*5,opciones[option])
                                print('---------------------------------------------------------------------------')
                                print_general_calendar(calendario,int(option))
                                break
                            else:
                                print('Opcion incorrecta')                    
                        input('Presione Enter para continuar...')
                        
                elif(option == '2'): #consulta individual calendario                    
                    menu_calendar_vaccune_individual()
                    print_individual_calendar(calendario)
                    input('Presione Enter para continuar...')
                elif(option == '3'): #crear calendario                    
                    menu_new_calendar_vaccune()
                    calendario = create_calendar(con)
                    input('Presione Enter para continuar...') 
                elif(option == '4'):#Enviar email a los afiliados
                    menu_send_mail()
                    if len(calendario)==0:
                        print('No hay un calendario de vacunaion vigente')
                    else:    
                        send_mail(calendario)
                elif(option == 'b' or option == 'B'): # Volver al menu anterior
                    back = True
                elif(option == 'e' or option == 'E'): # Salir del programa4
                    back = True
                    salir = True
                else:
                    print('Opcion no valida')            
                        
        elif(option == 'e' or option == 'E'):
            salir = True
        else:    
            print('Opcion no valida')
    
    close_db(con)
   
main()
