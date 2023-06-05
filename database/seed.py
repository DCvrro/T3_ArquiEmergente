import sqlite3 as sql

DB_PATH = "D:/Universidad/ArquiEmergente/T3_ArquiEmergente/database/database.db"

def createDB():
    conn = sql.connect(DB_PATH)  #Conectamos a la base de datos
    cursor = conn.cursor()  #Creamos un cursor para ejecutar comandos
    cursor.execute("""
        CREATE TABLE Admin(
            username string,
            password string
        )""")
    conn.commit()
    conn.close()


def addValues():
    conn = sql.connect(DB_PATH)  #Conectamos a la base de datos
    cursor = conn.cursor()  #Creamos un cursor para ejecutar comandos
    cursor.execute("""
    INSERT INTO Admin VALUES
    ('admin', 'admin')
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    addValues()