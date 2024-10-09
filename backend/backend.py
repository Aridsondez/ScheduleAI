from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


#Creating the Flask App
#CORS so front-end has access
app = Flask(__name__)
CORS(app)

#Configuring the app and defining the database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creating the datapbase in the app
db = SQLAlchemy(app)



#Defining an Employee based on criterias
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    efficiency = db.Column(db.Integer, nullable = False)

    
