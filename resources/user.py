from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.users import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str, required=True, help="This is mandatory!")
    parser.add_argument('password',
        type=str, help="This is mandatory!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message":"User {} already exists!".format(data["username"])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return { "message":"User {} created successfully".format(data["username"]) }, 201

    @jwt_required()
    def delete(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            user.delete_from_db()
            return {"message" : "User un-registered successfully"}, 200
        else:
            return {"message" : "User not found!"}
