from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import datetime

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
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "username": self.username,
            "password": self.password
        }
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return True
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
    def __init__(self, company_name, company_api_key):
        self.company_name = company_name
        self.company_api_key = company_api_key
    
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
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=False)
    location_name = db.Column(db.String(200), unique = True, nullable = False)
    location_country = db.Column(db.String(200), nullable = False)
    location_city = db.Column(db.String(200), nullable = False)
    location_meta = db.Column(db.String(200), nullable = True)
    #location_api_key = db.Column(db.String(200), unique = True, nullable = False)
    
    company = db.relationship('Company', backref='Location', lazy=True, primaryjoin='Location.company_id == Company.id')

    def __str__(self):
        return 'Location: {} Company: {}'.format(
            self.location_name,
            self.company.company_name)
#      return 'Location: {} ApiKey: {} Company: {}'.format(
#            self.location_name,
#            self.location_api_key,
#            self.company.company_name)
    def __init__(self, company_id,location_name, location_country, location_city,location_meta):
        self.company_id = company_id
        self.location_name = location_name
        self.location_country = location_country
        self.location_city = location_city
        self.location_meta = location_meta
        
        #self.location_api_key = location_api_key
    def serialize(self): 
        #return con lops datos  user y password 
        return {
            "location_name": self.location_name,
            "company_name": self.company.company_name
        } 
    
  #      def serialize(self): 
  #      #return con lops datos  user y password 
  #      return {
  #          "location_name": self.location_name,
  #          "location_api_key": self.location_api_key,
  #          "company_name": self.company.company_name
  #      }  
#Creamos la clase Sensor
class Sensor(db.Model):
    __tablename__ = 'Sensor'
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable = False)
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
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensor.id'), nullable=False)
    data_column1 = db.Column(db.String(255), nullable=False)
    data_column2 = db.Column(db.String(255), nullable=False)
    data_column3 = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return 'SensorData: {}'.format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "data_column1": self.data_column1,
            "data_column2": self.data_column2,
            "data_column3": self.data_column3,
            "timestamp": self.timestamp
        }