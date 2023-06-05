import sqlite3 as sql

DB_PATH = "D:/Universidad/ArquiEmergente/T3_ArquiEmergente/database/database.db"

def createDB():
    conn = sql.connect(DB_PATH)  #Conectamos a la base de datos
    cursor = conn.cursor()  #Creamos un cursor para ejecutar comandos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )""")
    #creo la tabla company
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Company(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_api_key TEXT NOT NULL
        )""")
    #CREO LA TABLA LOCATION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Location(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            location_name TEXT NOT NULL,
            location_country TEXT NOT NULL,
            location_city TEXT NOT NULL,
            location_meta TEXT,
            FOREIGN KEY (company_id) REFERENCES Company(id)
        )""")    
    #creo la tabla Sensor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sensor(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            sensor_id TEXT NOT NULL,
            sensor_name TEXT NOT NULL,
            sensor_category TEXT NOT NULL,
            sensor_meta TEXT,
            sensor_api_key TEXT NOT NULL,
            FOREIGN KEY (location_id) REFERENCES Location(id)
        )""")
    #creo la tabla SensorData
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SensorData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            data_column1 TEXT,
            data_column2 TEXT,
            data_column3 TEXT,
            FOREIGN KEY (sensor_id) REFERENCES Sensor (id)
        )""")
    conn.commit()
    conn.close()


def addValues():
    conn = sql.connect(DB_PATH)  # Conectamos a la base de datos
    cursor = conn.cursor()  # Creamos un cursor para ejecutar comandos
    
    # Agregar datos de ejemplo
    # Agregar admin
    cursor.execute("""
        INSERT INTO Admin (username, password) VALUES ('admin', 'admin')
    """)
    
    # Agregar compañía
    cursor.execute("""
        INSERT INTO Company (company_name, company_api_key) VALUES ('Company A', 'api_key_123')
    """)
    
    # Agregar ubicación
    cursor.execute("""
        INSERT INTO Location (company_id, location_name, location_country, location_city) 
        VALUES (1, 'Location A', 'Country A', 'City A')
    """)
    
    # Agregar sensor
    cursor.execute("""
        INSERT INTO Sensor (location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) 
        VALUES (1, 1, 'Sensor A', 'Category A', 'Meta A', 'api_key_sensor_123')
    """)
    
    # Agregar datos de sensor
    cursor.execute("""
        INSERT INTO SensorData (sensor_id, data_column1, data_column2, data_column3) 
        VALUES (1, 'Value 1', 'Value 2', 'Value 3')
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    addValues()