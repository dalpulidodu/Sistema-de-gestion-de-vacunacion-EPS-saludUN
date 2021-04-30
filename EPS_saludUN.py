
import os
import sqlite3
from sqlite3 import Error
from PIL import Image, ImageDraw, ImageFont

##########################################################################################################
#                                             Data
##########################################################################################################

def sql_connection():
    """
    ==========================================
    
    Funcion que crea/conecta la base de datos
    
    """
    try:
        con = sqlite3.connect('db.db')
        print("Conexion realizada: DB creada")
        return con
    except Error:
        print('Se ha prodicido un error al crear la conexion',Error)


def create_table_vaccine_lot(con):
    """
    ========================================
    
    Funcion que crea una tabla para los lotes de vacunas
    con los elementos:
    
    (lote, fabricante, tipo de vacuna, cantidad recibida, cantidad usada, dosis, temperatura, efectividad, tiempo de proteccion, fecha de vencimiento, imagen)
             
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
    
    """
    =========================================
    
    Funcion que lee la informacion dada por el usuario y la retorna como una tupla
    
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



def insert_vaccine_lot(con,x):
    
    """
    ===================================
    
    Funcion que se utiliza insertar en la base de datos la tubla generada por:
    read_info_vaccine_lot()
    
    """
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO lote_Vacuna(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen) VALUES (?,?,?,?,?,?,?,?,?,?,?)", x)
    con.commit()

def sql_fetch_vaccine_lot(con):
    
    """
    ==========================================
    
    Función que realiza un consulta en la base de datos teniendo en cuenta el numero de lote
    
    Muestra la imagen asociada a la fabricante con el numero de lote y su fecha de vencimiento.
    
    Imprime los elementos de la fila asociada al numero de lote
    """
    cursorObj = con.cursor()
    num_lote=input("numero de lote a consultar: ")
    buscar='SELECT * FROM lote_Vacuna where lote='+num_lote
    cursorObj.execute(buscar)
    filas = cursorObj.fetchall()
    for row in filas:
        img = Image.open(row[10])
        img.show()       
        print(row[0:10])
        print('ruta de imagen: ' +row[10])
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
    dia=(input("dia "+word+": "))
    dia = dia.rjust(2,"0")
    
    mes = (input("mes "+word+": "))
    mes= mes.rjust(2,"0")
    
    ano = (input("año "+word+": "))
    ano= ano.rjust(4)
    
    date=dia+"/"+mes+"/"+ano
    print(word,date)
    
    return date

def image(lote,fabricante, fecha_vencimiento):
    """
    ========================================
    
    Funcion para crear e ingresar una imagen de acuerdo a numero de lote, el fabricante y la fecha de vencimiento
    
    utilizando la libreria pill, crea una imagen de acuerdo al fabricante, y le añade el numero de lote y fecha de vencimiento a la imagen
    
    retorna la ruta en la que se guardo la imagen
    """
        
    if(fabricante=='Sinovac'):
        foto = 'fabrica/Sinovac.jpg'

    if(fabricante=='Pfizer'):
        foto = 'fabrica/Pfizer.jpg'

    if(fabricante=='Moderna'):
        foto = 'fabrica/Moderna.jpg'
       

    if(fabricante=='SputnikV'):
        foto = 'fabrica/SputnikV.jpg'
        

    if(fabricante=='AstraZeneca'):
        foto = 'fabrica/AstraZeneca.jpg'
        
    if(fabricante=='Sinopharm'):
        foto = 'fabrica/Sinopharm.jpg'

    if(fabricante=='Covaxim'):
        foto = 'fabrica/Covaxim.jpg'

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
                            

'''
=========================================================================================================
                                      Inicializacion      
=========================================================================================================
'''

def main():
    
    """
    ==================
    Funcion creada para dar inicio al programa
    """
    
    con=sql_connection()
    #create_table_vaccine_lot(con)
    #x=read_info_vaccine_lot()
    
    #insert_vaccine_lot(con,x)
    sql_fetch_vaccine_lot(con)
    close_db(con)

main()
