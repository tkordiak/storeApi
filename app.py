import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.employee import Employee, EmployeeList
from db import db

app = Flask(__name__)
app.secret_key = 'tomek'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# this is not creating /auth
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Employee, '/employee/<string:name>')
api.add_resource(EmployeeList, '/employees')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
