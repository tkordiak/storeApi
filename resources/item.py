from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        print(item)
        if item:
            return item.json()
        else:
            return {'message': f'Item {item} not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item {name} already exists'}, 400

        request_data = Item.parser.parse_args()

        print(request_data)
        item = ItemModel(name, request_data['price'], request_data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting item to database'}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
