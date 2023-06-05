from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Admin
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
  