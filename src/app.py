from flask import Flask, jsonify
from flask_restful import  Api
from flask_jwt_extended import JWTManager

from resources.user import (
    User, 
    UserLogin,
    UserLogout
)
from resources.item import Item


app = Flask(__name__)
app.secret_key = 'secretKey'
api = Api(app)


app.config['JWT_SECRET_KEY'] = 'howhow'  
app.config['JWT_BLACKLIST_ENABLED'] = True  
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin':True}
    return {'is_admin':False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expored ..',
        'error' : 'token_expired'
    }),401

@jwt.invalid_token_loader
def invalid_token_callback(error):  
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401





@app.route("/")
def home():
    return "<h1>Hello OCP ~</h1>"


api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout, '/logout')

if __name__ == "__main__":

    app.run(port=5000, debug=True, host='0.0.0.0')
