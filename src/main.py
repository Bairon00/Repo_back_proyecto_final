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
from models import db, User,Medicos,Especialidades
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
#from models import Person

app = Flask(__name__)
jwt=JWTManager(app)
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

@app.route("/especialidades",methods=["GET"])
def all_especialidades():
    all_especialidades=Especialidades.query.all()
    especialidades_serialized=[]
    for esp in all_especialidades:
        especialidades_serialized.append(esp.serialize())
    return jsonify(especialidades_serialized)

@app.route("/usuario/<int:usuario_id>",methods=["GET"])
def one_usuario(usuario_id):
    one=User.query.get(usuario_id)
    return jsonify(one.serialize())

@app.route("/logUsuario/<email>",methods=["GET"])
def log_user(email):
    log_user=User.query.filter_by(email=email).first()
    return jsonify(log_user.serialize())

@app.route("/medico/<int:medico_id>",methods=["GET"])
def one_medico(medico_id):

    uno=Medicos.query.get(medico_id)
    return jsonify(uno.serialize())

    one=Medicos.query.get(medico_id)
    return jsonify(one.serialize())





@app.route("/add_user",methods=["POST"])
def add_user():
    body=request.get_json()
    new_user=User()
    new_user.name=body["name"]
    new_user.last_name=body["last_name"]
    new_user.email=body["email"]
    new_user.password=body["password"]
    new_user.previcion=body["previcion"]
    new_user.is_active=body["is_active"]
    db.session.add(new_user)
    db.session.commit()

    return "agregado!"
@app.route("/add_medico",methods=["POST"])
def add_medico():
    body=request.get_json()
    new_medico=Medicos()
    new_medico.name=body["name"]
    new_medico.email=body["email"]
    new_medico.valor=body["valor"]
    new_medico.imagen=body["imagen"]
    db.session.add(new_medico)
    db.session.commit()
    return "medico agregado"

@app.route("/add_especialidad",methods=["POST"])
def add_especialidad():
    body=request.get_json()
    new_especialidad=Especialidades()
    new_especialidad.especialidad=body["especialidad"]
    db.session.add(new_user)
    db.session.commit()
    return "espeecialidad agregada"

@app.route("/cambiar/<int:especialidad_id>",methods=["PUT"])
def cambair(especialidad_id):
    body=request.get_json()
    esp=Especialidades.query.get(especialidad_id)
    if "especialidad" in body:
            esp.especialidad = body["especialidad"]
    db.session.commit()
    return "cambiado"
@app.route("/user/<int:user_id>",methods=["PUT"])
def cambio(user_id):
    body=request.get_json()
    user=User.query.get(user_id)
    if "name" in body:
        user.name=body["name"]
    if "email" in body:
        user.email=body["email"]
    if "last_name" in body:
        user.last_name=body["last_name"]
    if "password" in body:
        user.password=body["password"]
    if "is_active" in body:
        user.is_active=body["is_active"]
    if "prevision" in body:
        user.prevision=body["prevision"]
    if "token" in body:
        user.token=body["token"]
    db.session.commit()
    return "cambio exitoso"
    
@app.route("/user/<int:user_id>",methods=["DELETE"])
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    if(user):
        db.session.delete(user)
        db.session.commit()
        return "User eliminado"
    else:
        raise APIException("No existe este usuario",status_code=404)
@app.route("/medico/<int:medico_id>",methods=["DELETE"])
def delete_medico(medico_id):
    medico=Medicos.query.filter_by(id=medico_id).first()
    if(medico):
        db.session.delete(medico)
        db.session.commit()
        return "Eliminado"
    else:
        raise APIException("No existe este medico",status_code=404)
@app.route("/especialidad/<especialidad>",methods=["DELETE"])
def delete_esp(especialidad):
    especialidad=Especialidades.query.filter_by(especialidad=especialidad).first()
    if(especialidad):
        db.session.delete(especialidad)
        db.session.commit()
        return "especialidad eliminada"
    else:
        raise APIException("No existe esta especialidad",status_code=404)
@app.route("/login",methods=["POST"])
def login():
    body=request.get_json()
    user=User.query.filter_by(email=body["email"],password=body["password"]).first()
    if(user is None):
        return jsonify({"mensaje":"usuario no existe"})
    else:
        expiracion=datetime.timedelta(minutes=1)
        acceso=create_access_token(identity=body["email"],expires_delta=expiracion)
        return jsonify({
            "login":"ok",
            "token":acceso
        })
@app.route("/perfil",methods=["GET"])
@jwt_required()
def perfil():
    identidad=get_jwt_identity()
    user=User.query.filter_by(email=identidad).first()
    return jsonify({
        "user":user.serialize()
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
        password=body['password'], 
        name=body['name'], 
        last_name=body['last_name'], 
        prevision=body['prevision'], 
        is_active=True)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"mensaje": "El usuario ya fue creado"}), 201  # creado

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)