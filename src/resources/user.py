import os
import paramiko
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp



_user_paser = reqparse.RequestParser()
_user_paser.add_argument('username',
                         type=str,
                         required=True,
                         help="This field cannot be blank"
                         )
_user_paser.add_argument('password',
                         type=str,
                         required=True,
                         help="This field cannot be blank"
                         )


class UserRegister(Resource):

    def post(self):
        data = _user_paser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username aleardy exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully ~"}


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted ..'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_paser.parse_args()
        host = os.getenv('SSHIP')
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port=22, username=data['username'], password=data['password'])
            print("login Success !!")
            access_token = create_access_token(identity=data['username'], fresh=True)
            refresh_token = create_refresh_token(data['username'])
            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        except Exception as e:
            return {'message': f'Invalid credentials, {e}'}, 401
        finally:
            client.close()

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        print(jti)
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {'access_token':new_token},200