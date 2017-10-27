from flask_restful import Resource
from flask_jwt import jwt_required
from models.stores import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_storename(name)
        if store:
            return store.json(), 200
        return {"message" : "Store not found in database"}, 404

    def post(self, name):
        if StoreModel.find_by_storename(name):
            return {"message" : "Store {} already exists!".format(name)}, 400

        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_storename(name)
        if store:
            store.delete_from_db()
            return {"message" : "Store {} deleted successfully".format(name)}, 200
        else:
            return {"message" : "Store not found to be deleted!"}, 400


class StoreList(Resource):
    def get(self):
        return {"stores" : [store.json() for store in StoreModel.query.all()]}
