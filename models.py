from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        #return con lops datos id, user y password
        return 'User: {} Password: {}'.format(
            self.username,
            self.password)
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "username": self.username,
            "password": self.password
        }
#creamos la clase Company
class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(200), unique = True, nullable = False)
    company_api_key = db.Column(db.String(200), unique = True, nullable = False)

    def __str__(self):
        #return con lops datos id, user y password
        return 'Company: {} ApiKey: {}'.format(
            self.company_name,
            self.company_api_key)
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "company_name": self.company_name,
            "company_api_key": self.company_api_key
        }
#Creamos la clase Location
class Location(db.Model):
    __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    location_name = db.Column(db.String(200), unique = True, nullable = False)
    location_country = db.Column(db.String(200), nullable = False)
    location_city = db.Column(db.String(200), nullable = False)
    location_api_key = db.Column(db.String(200), unique = True, nullable = False)
    
    company = db.relationship('Company', backref='Location', lazy=True)

    def __str__(self):
        #return con lops datos id, user y password
        return 'Location: {} ApiKey: {} Company: {}'.format(
            self.location_name,
            self.location_api_key,
            self.company_name)
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "location_name": self.location_name,
            "location_api_key": self.location_api_key,
            "company_name": self.company_name
        }    
#Creamos la clase Sensor
class Sensor(db.Model):
    __tablename__ = 'Sensor'
    id = db.Column(db.Integer, primary_key = True)
    location__id = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable = False)
    sensor_id = db.Column(db.Integer, nullable=False)
    sensor_name = db.Column(db.String(255), nullable=False)
    sensor_category = db.Column(db.String(255), nullable=False)
    sensor_meta = db.Column(db.String(255))
    sensor_api_key = db.Column(db.String(255), nullable=False)

    location = db.relationship('Location', backref='Sensor', lazy=True)


    def __str__(self):
        #return con lops datos id, user y password
        return 'Sensor: {} ApiKey: {} Location: {}'.format(
            self.sensor_name,
            self.sensor_api_key,
            self.location_name)
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "sensor_name": self.sensor_name,
            "sensor_api_key": self.sensor_api_key,
            "location_name": self.location_name
        }
#creamos la clase SensorData
class SensorData(db.Model):
    __tablename__ = 'SensorData'
    id = db.Column(db.Integer, primary_key = True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensor.id'), nullable = False)
    data_column1 = db.Column(db.String(255), nullable=False)
    data_column2 = db.Column(db.String(255), nullable=False)
    data_column3 = db.Column(db.String(255), nullable=False)
    def __str__(self):
        #return con lops datos id, user y password
        return 'Sensor: {} Data: {} Timestamp: {}'.format(
            self.sensor_name,
            self.sensor_data,
            self.sensor_timestamp)
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "sensor_name": self.sensor_name,
            "sensor_data": self.sensor_data,
            "sensor_timestamp": self.sensor_timestamp
        }
