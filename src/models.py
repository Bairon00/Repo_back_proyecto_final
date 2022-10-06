from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rut= db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    prevision = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Medicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rut= db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    prevision = db.Column(db.String(30), unique=False, nullable=False)
    especialidad = db.Column(db.String(30), unique=False, nullable=False)
    valorconsulta = db.Column(db.String(6), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Medicos %r>' % self.medicos

    def serialize(self):
        return {
            "id": self.id,
            "personajes": self.personajes,
            "genero": self.genero,
        }