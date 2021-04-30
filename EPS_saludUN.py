
import os
import sqlite3
from sqlite3 import Error
from PIL import Image, ImageDraw, ImageFont

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


def create_table_vaccine_lot(con):
    """
    Funcion que crea una tabla para los lotes de vacunas
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
    Funcion que lee la informacion del lote y la retorna como una cadena de caracteres
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
    """ Funcion que se utiliza insertar en la base de datos"""
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO lote_Vacuna(lote, fabricante, tipo_vacuna, cantidad_recibida, cantidad_usada, dosis, temperatura, efectividad, tiempo_proteccion, fecha_vencimiento, imagen) VALUES (?,?,?,?,?,?,?,?,?,?,?)", x)
    con.commit()

def sql_fetch_vaccine_lot(con):
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
    Funcion para crear e ingresar una imagen
    """
        
    if(fabricante=='Sinovac'):
        foto = 'fabrica/Sinovac.jpg'

    if(fabricante=='Pfizer'):
        foto = 'fabrica/Pfizer.jpg'

    if(fabricante=='Moderna'):
        foto = 'fabrica/Moderna.jpg'
       

    if(fabricante=='SputnikV'):
        foto = 'fabrica/SputnikV.jpg', 'rb'
        

    if(fabricante=='AstraZeneca'):
        foto = 'fabrica/AstraZeneca.jpg'
        
    if(fabricante=='Sinopharm'):
        foto = 'fabrica/Sinopharm.jpg'

    if(fabricante=='Covaxim'):
        foto = 'fabrica/Covaxim.jpg', 'rb'

    img = Image.new('RGB', (200, 150), "white")
    im = Image.open('fabrica/'+fabricante+'.jpg')
    img.paste(im,(0,0))
    fnt = ImageFont.truetype('fuente/Arial.ttf', 12)
    d=ImageDraw.Draw(img)
    d.text((2, 100),'Fecha de vencimiento: '+str(fecha_vencimiento), font=fnt, fill=(0, 0, 0))
    d.text((2, 125),'No.lote: ' +str(lote), font=fnt, fill=(0, 0, 0))
    img.save('imagenes/'+str(lote)+'.jpg')
    ruta='imagenes/'+str(lote)+'.jpg'
       
    return ruta
                            

'''
=========================================================================================================
                                      Inicializacion      
=========================================================================================================
'''

def main():
    
    con=sql_connection()
    #create_table_vaccine_lot(con)
    #x=read_info_vaccine_lot()
    
    #insert_vaccine_lot(con,x)
    sql_fetch_vaccine_lot(con)
    close_db(con)

main()
