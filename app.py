from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Admin , Company, Location, Sensor, SensorData
import sqlite3 as sql
from logging import exception


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/Universidad/ArquiEmergente/T3_ArquiEmergente/database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/admins", methods=['GET']) # el get es para leer lo de la base de datos
def getAdmin():
    try:
        adminList = Admin.query.all()
        #for admin in adminList:
        #    print(admin)
        toReturn = [admin.serialize() for admin in adminList] #respuesta en diccionario
        return jsonify(toReturn) , 200 #respuesta en json

    except Exception:
        exception("Error al obtener los datos (Admin)")
        return jsonify({"msg": "Error"}), 500

@app.route("/api/admin/", methods = ['GET'] ) #obtener admin por usuario o nombre
def getAdminByUser():
    try:
        username = request.args['username']
        admin = Admin.query.filter_by(username = username).first()

        if admin is None:
            return jsonify({"msg": "No existe el admin con ese Username"}), 404
        else:
            return jsonify(admin.serialize()), 200
    
    except Exception:
        exception("Error al obtener los datos (Admin por nombre)")
        return jsonify({"msg": "Error"}), 500

@app.route("/api/findadmin", methods = ['GET'])
def findAdmin():
    try:
        username = request.args['username']
        password = request.args['password']
        admin = Admin.query.filter_by(username = username, password = password).first()

        if admin is None:
            return jsonify({"msg": "No existe el admin con ese Username"}), 404
        else:
            return jsonify(admin.serialize()), 200
    
    except Exception:
        exception("Error al obtener los datos (Admin por nombre)")
        return jsonify({"msg": "Error"}), 500

@app.route("/api/sensordata", methods=['POST'])
def receiveSensorData():
    data = request.get_json()
    api_key = data.get('api_key')
    json_data = data.get('json_data')

    # Verificar si el api_key corresponde a un sensor válido
    sensor = Sensor.query.filter_by(sensor_api_key=api_key).first()
    if sensor is None:
        return jsonify({"error": "API key inválido"}), 400

    # Guardar los datos recibidos en la base de datos
    try:
        for item in json_data:
            sensor_data = SensorData(
                sensor_id=sensor.id,
                data_column1=item.get('data_column1'),
                data_column2=item.get('data_column2'),
                data_column3=item.get('data_column3')
            )
            db.session.add(sensor_data)

        db.session.commit()
        return jsonify({"message": "Datos del sensor guardados correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def test_connection():
    conn = None
    try:
        conn = sql.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SQLITE_VERSION()")
        data = cursor.fetchone()
        print("Conexión exitosa. Versión de SQLite:", data[0])

    except sql.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    test_connection()
    app.run(debug=True,port =4000 )
  