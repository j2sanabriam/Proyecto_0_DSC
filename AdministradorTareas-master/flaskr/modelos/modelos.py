from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum


db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(120))
    descripcion = db.Column(db.String(500))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')

class Estado(enum.Enum):
    No_Iniciada = 1
    En_Curso = 2
    Finalizada = 3

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    imagen = db.Column(db.String(250))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(500))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.Enum(Estado))
    categoria = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class TareaSchema(SQLAlchemyAutoSchema):
    estado = EnumADiccionario(attribute=("estado"))
    class Meta:
         model = Tarea
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

