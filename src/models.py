from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =db.Column(db.String(80), unique=False, nullable=False)
    is_active =db.Column(db.Boolean(), unique=False, nullable=False)
    prevision=db.Column(db.String(30),unique=False,nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "name":self.name,
            "last_name":self.last_name,
            "id": self.id,
            "email": self.email,
            "prevision":self.prevision

            # do not serialize the password, its a security breach
        }
class Especialidades(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    area=db.Column(db.String(100),nullable=False)
    especialidad=db.Column(db.String(100),unique=True,nullable=False)
    
    def __repr__(self):
        return '<Especialidades %r>' % self.especialidad
    def serialize(self):
        return {
            
            "especialidad":self.especialidad
          
        }
class Medicos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=False,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    valor=db.Column(db.String(30),nullable=False)
    imagen=db.Column(db.String(250),nullable=False)
    especialidad=db.Column(db.String(100),db.ForeignKey("especialidades.especialidad"))
    rel_esp=db.relationship("Especialidades")

   
    def __repr__(self):
        return '<Medicos %r>' % self.name
    def serialize(self):
        return {
            "name":self.name,
            "valor":self.valor
        }


