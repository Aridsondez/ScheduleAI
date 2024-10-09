from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, JSON
from flask_cors import CORS
from employer import define_empoyer



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
#Efficiency X/100

class Employee(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    efficiency = db.Column(db.Integer, nullable = False)

    relationships = Column(JSON)
    availibility  = Column(JSON)


    #Assume relationship and availibility is empty if so proceed accordingly 
    def __init__(self, name, efficiency, relationships= None, availibility = None):
        self.name = name
        self.efficiency = efficiency
        self.relationships = relationships if relationships else {}
        self.availibility = availibility if availibility else {}


@app.route("/add_employees", methods=['POST'])
def add_employee():
    data = request.get_json()

    for employee_data in data:
        new_employee = Employee(
            name = employee_data.get('name'),
            efficiency= employee_data.get('efficiency'),
            relationships=employee_data.get('relationships'),
            availibility=employee_data.get('availability')
        )
        db.session.add(new_employee)
    
    db.session.commit()
    return jsonify({"message": "Employee added!"}), 201


#update the employee by the name
@app.route("/update_employee/<string:id>", methods = ['PUT'])
def update_employee(id):
    data = request.get_json()#Gets all the data in database
    employee= Employee.query.get_or_404(id)
    
    if not employee:
        return jsonify({{"messege"}:"employee not found"}),404
    
    employee.efficiency = data.get('efficiency', employee.efficiency)
    employee.relationship = data.get("relationship", employee.relationship)
    employee.availibility = data.get("availibility", employee.availibility)

    db.session.commit()
    return jsonify({"message": "Employee updated!"}), 200



@app.route("/delete_employee/<string:id>", methods= ['DELETE'])  
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message":"employee deleted !"})


@app.route("/", methods = ['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'Alpha': employee.name, "efficiency": employee.efficiency, "relationships": employee.relationships, "availiblity": employee.availibility} for employee in employees])   


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
