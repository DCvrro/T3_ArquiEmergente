from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Admin
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/Universidad/ArquiEmergente/T3_ArquiEmergente/database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/admin")
def getAdmin():
    admin = Admin.query.filter_by(username='admin').first()
    return admin.username + " " + str(admin)

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
  