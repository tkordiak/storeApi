from flask_restful import Resource, reqparse
from models.employee import EmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role', type=str, required=True, help='Employee role is required')
    parser.add_argument('email', type=str, required=True, help='Employee email is required')
    parser.add_argument('store_id', type=str, required=True, help='Store id is required')

    def get(self, name):
        employee = EmployeeModel.find_by_name(name)
        if not employee:
            return {'message': f'Employee {name} not found'}, 404
        return employee.json()

    def post(self, name):
        if EmployeeModel.find_by_name(name):
            return {'message': f'Employee {name} already exists'}, 400

        data = Employee.parser.parse_args()
        employee = EmployeeModel(name, **data)

        try:
            employee.save_to_db()
        except:
            return {'message': 'Error while inserting to DB'}, 500

        return employee.json(), 201

    def put(self, name):
        data = Employee.parser.parse_args()
        employee = EmployeeModel.find_by_name(name)

        if not employee:
            employee = EmployeeModel(name, **data)
        else:
            employee.role = data['role']
            employee.email = data['email']
            employee.store_id = data['store_id']
        employee.save_to_db()

        return employee.json()

    def delete(self, name):
        if not EmployeeModel.find_by_name(name):
            return {'message': f'Employee {name} does not exists'}

        employee = EmployeeModel.find_by_name(name)
        employee.delete_from_db()
        return {'message': f'Employee {name} deleted'}


class EmployeeList(Resource):
    def get(self):
        return {'employees': [employee.json() for employee in EmployeeModel.query.all()]}
