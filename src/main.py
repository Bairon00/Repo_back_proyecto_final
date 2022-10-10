"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Medicos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
@app.route('/medicos',methods=["GET"])
def all_medicos():
    all_medicos=Medicos.query.all()
    medicos_serialized=[]
    for medicos in all_medicos:
        medicos_serialized.append(medicos.serialize())
    return jsonify(medicos_serialized)
@app.route("/usuarios",methods=["GET"])
def all_user():
    all_user=User.query.all()
    users_serialized=[]
    for users in all_user:
        users_serialized.append(users.serialize())
    return jsonify(users_serialized)
@app.route("/usuario/<int:usuario_id>",methods=["GET"])
def one_usuario(usuario_id):
    one=User.query.get(usuario_id)
    return jsonify(one.serialize())

@app.route("/medico/<int:medico_id>",methods=["GET"])
def one_medico(medico_id):
    one=Medicos.query.get(usuario_id)
    return jsonify(one.serialize())








# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
