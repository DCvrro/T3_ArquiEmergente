from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from sqlalchemy import join 
from models import db, Admin , Company, Location, Sensor, SensorData
import sqlite3 as sql
from logging import exception
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/Universidad/ArquiEmergente/T3_ArquiEmergente/database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager(app)
app.secret_key = 'key'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
basic_auth = BasicAuth(app)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route("/api/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username = username, password = password).first()

        if admin is None:
            return jsonify({"msg": "No existe el admin con ese Username"}), 404
        else:
            login_user(admin)
            return redirect(url_for('visor'))

    return render_template("login.html")

@app.route("/api/visor")
@login_required
def visor():
    return render_template("visor.html")

@app.route('/api/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/new_company', methods=['GET','POST'])
@login_required
def new_company(): #creamos nuevas compañias
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_api_key = request.form['company_api_key']

        company = Company.query.filter_by(company_name = company_name).first()

        if company is None:
            new_company = Company(company_name, company_api_key)
            db.session.add(new_company)
            db.session.commit()
            return redirect(url_for('visor'))
        else:
            return jsonify({"msg": "Ya existe una compañia con ese nombre"}), 404

    return render_template("new_company.html")


@app.route('/api/new_location', methods=['GET','POST'])
@login_required
def new_location(): #creamos nuevas localizaciones
    if request.method == 'POST':
        company_name = request.form['company_name']
        location_name = request.form['location_name']
        location_country = request.form['location_country']
        location_city = request.form['location_city']
        location_meta = request.form['location_meta']

        company = Company.query.filter_by(company_name = company_name).first()

        if company is None:
            return jsonify({"msg": "No existe la compañia con ese nombre"}), 404
        
        existing_location = Location.query.filter_by(company_id=company.id, location_name=location_name).first()

        if existing_location is not None:
            return jsonify({"msg": "Ya existe una locacion con ese nombre"}), 404
        
        new_location = Location(company.id, location_name, location_country, location_city, location_meta)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('visor'))
    return render_template("new_location.html")

@app.route('/api/new_sensor', methods=['GET','POST'])
@login_required
def new_sensor():
    if request.method == 'POST':
        location_id = request.form['location_id']
        sensor_name = request.form['sensor_name']
        sensor_category = request.form['sensor_category']
        sensor_meta = request.form['sensor_meta']
        sensor_api_key = request.form['sensor_api_key']

        #reviso si existe esa location
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"msg": "No existe la locacion con ese id"}), 404

        sensor = Sensor.query.filter_by(sensor_name = sensor_name).first()
        if sensor: 
            return jsonify({"msg": "Ya existe un sensor con ese nombre"}), 404

        key = Sensor.query.filter_by(sensor_api_key = sensor_api_key).first()
        if key:
            return jsonify({"msg": "Ya existe un sensor con esa api key"}), 404

        new_sensor = Sensor(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
        db.session.add(new_sensor)
        db.session.commit()
        return redirect(url_for('visor'))
    return render_template("new_sensor.html")
@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

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

@app.route('/api/v1/sensor_data', methods=['POST']) #SOLICITADO
@basic_auth.required
def insert_sensor_data(): # Estructura JSON   {"api_key":<sensor_api_key>, "json_data":[{…}, {….}] }
    request_data = request.get_json()

    if 'api_key' not in request_data: 
        return jsonify({"error": "No se ha enviado la api_key"}), 400
    if 'json_data' not in request_data: 
        return jsonify({"error": "No se ha enviado el json_data"}), 400

    sensor_api_key = request_data['api_key']
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if sensor is None:
        return jsonify({"error": "API key inválido"}), 400
    
    json_data = request_data['json_data']
    if not isinstance(json_data, list):
        return jsonify({"error": "json_data debe ser una lista de diccionarios"}), 400
    
    for data in json_data:
        if 'timestamp' not in data:
            return jsonify({"error": "No se ha enviado el timestamp"}), 400
        timestamp = datetime.fromtimestamp(data['timestamp'])
        variable_data = {key:value for key, value in data.items() if key != 'timestamp'}

        sensor_data = SensorData(
            sensor_id=sensor.id,
            timestamp=timestamp,
        )

        sensor_data.set_data(variable_data)
        db.session.add(sensor_data)
    db.session.commit()
    return jsonify({"message": "Datos del sensor guardados correctamente"}), 200

@app.route('/api/v1/sensor_data', methods=['GET'])  #SOLICITADO
@basic_auth.required
def get_sensor_data():

    request_data = request.get_json()
    company_api_key = request_data.get('company_api_key')
    from_timestamp = request_data.get('from')
    to_timestamp = request_data.get('to')
    sensor_ids = request_data.get('sensor_ids')

    if not company_api_key:
        return jsonify({"error": "No se ha enviado la company_api_key"}), 400
    
    company = Company.query.filter_by(company_api_key=company_api_key).first()
    if company is None:
        return jsonify({"error": "API key inválido"}), 400
    
    sensor_data = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.timestamp >= from_timestamp,
        SensorData.timestamp <= to_timestamp
    ).all()

    if not sensor_data:
        return jsonify({"error": "No hay datos de sensores para mostrar"}), 404
    
    response_data = {
        "company_name": company.company_name,
        "company_api_key": company.company_api_key,
        "sensor_data": [data.serialize() for data in sensor_data]
    }
    print(request_data)
    return jsonify(response_data), 200

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
  