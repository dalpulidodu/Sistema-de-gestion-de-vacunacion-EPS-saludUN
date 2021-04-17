def sql_connection():
    """Funcion que crea la conexion en la Base de datos Sqlite3 """
    try:
        con = sqlite3.connect('BDSQlLiteEjercicioClase.db')
        return con
    except Error:
        print(Error)
