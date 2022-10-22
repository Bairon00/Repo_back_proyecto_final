"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

#from models import Person
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def getUser():
    all_user = User.query.all()
    serializados = list(map(lambda user: user.serialize(), all_user))
    print(all_user)
    return jsonify({
        "mensaje": "Todos los usuarios",
        "user": serializados
    }), 200


@app.route("/user/<int:user_id>", methods=["GET"])
def one_user(user_id):
    one = User.query.get(user_id)
    return jsonify(one.serialize())


@app.route("/user/<int:user_id>/edit", methods=["PUT"])
def edit(user_id):
    body = request.get_json()
    # coprobar si existe un usuario con mismo correo
    user = User.query.filter_by(email=body['email']).first()
    if (user):
        return jsonify({"mensaje": "El email ya se encuentra en uso, por favor elegir otro."}), 418
    else:
        edit_user = User(email=body['email'],
                         password=body['password'], password_confirm=['password_confirm'], name=body['name'], last_name=body['last_name'], is_active=True)
        db.session.commit()
        return jsonify(body)


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(email=body['email']).first()
    if (user):
        if (user.password == body['password']):

            expiracion = datetime.timedelta(minutes=10)
            token = create_access_token(
                identity=body['email'], expires_delta=expiracion)
            return jsonify({
                "email": body['email'],
                "mensaje": "Bienvenido",
                "token": token

            })
        else:
            return jsonify({"mensaje": 'Los datos son incorrectos'})
    else:
        return jsonify({"mensaje": 'El usuario no existe'})


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return jsonify({"mensaje": "Cerraste sesión exitosamente"})


@app.route('/private', methods=['GET'])
@jwt_required()
def private():
    identidad = get_jwt_identity()
    return jsonify({
        "mensaje": "Bienvenido " + identidad
    })


@app.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    # coprobar si existe un usuario con mismo correo
    user = User.query.filter_by(email=body['email']).first()
    if (user):
        return jsonify({"mensaje": "El usuario ya existe"}), 403
    else:
        new_user = User(email=body['email'],
                        password=body['password'], name=body['name'], last_name=body['last_name'], prevision=body['prevision'], is_active=True)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"mensaje": "El usuario ya fue creado"}), 201  # creado


@app.route('/user/<int:user_id>/getpassword', methods=['GET'])
def getpassword(user_id):
    password = User.query.get(user_id)

    return jsonify(
                password.serialize_password()
            )


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
