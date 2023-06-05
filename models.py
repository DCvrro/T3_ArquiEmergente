from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'Admin'
    rowid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable=False)

    def __str__(self):
        #return con lops datos id, user y password
        return 'ID: {} User: {} Password: {}'.format(
            self.rowid,
            self.username,
            self.password)
    
    def serialize(self): 
        #return con lops datos id, user y password 
        return {
            "id": self.rowid,
            "username": self.username,
            "password": self.password
        }