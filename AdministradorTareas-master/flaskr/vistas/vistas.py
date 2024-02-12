from flask import request
# from modelos.modelos import db, Categoria, CategoriaSchema, Usuario, UsuarioSchema, Tarea, TareaSchema
from ..modelos import db, Categoria, CategoriaSchema, Usuario, UsuarioSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime

categoria_schema = CategoriaSchema()
usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()


class VistaCategorias(Resource):
    def post(self):
        nueva_categoria = Categoria(nombre=request.json["nombre"], descripcion=request.json["descripcion"])
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria)
    
    def get(self):
        return [categoria_schema.dump(ca) for ca in Categoria.query.all()]
    
class VistaCategoria(Resource):
    def get(self, id_categoria):
        return categoria_schema.dump(Categoria.query.get_or_404(id_categoria))
    
    def put(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        categoria.nombre = request.json.get("nombre", categoria.nombre)
        categoria.descripcion = request.json.get("descripcion", categoria.descripcion)
        db.session.commit()
        return categoria_schema.dump(categoria)
    
    def delete(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        db.session.delete(categoria)
        db.session.commit()
        return '',204



class VistaLogIn(Resource):
    @jwt_required()
    def post(self):
            u_nombre = request.json["nombre"]
            u_contrasena = request.json["contrasena"]
            usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena=u_contrasena).all()
            if usuario:
                return {'mensaje':'Inicio de sesión exitoso'}, 200
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401

class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"], imagen=request.json["imagen"])
        token_acceso = create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"mensaje":"Usuario creado exitosamente", "token de acceso":token_acceso}
    
    def get(self):
        return [usuario_schema.dump(usr) for usr in Usuario.query.all()]
    

class VistaUsuario(Resource):
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        usuario.imagen = request.json.get("imagen", usuario.imagen)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204


class VistaTarea(Resource):
    def get(self, id_tarea):
        return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))
    
    def put(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.texto = request.json.get("texto", tarea.texto)
        # tarea.fecha_fin = request.json.get("fecha_fin", tarea.fecha_fin)
        tarea.fecha_fin = datetime.strptime(request.json["fecha_fin"], '%Y-%m-%d').date()
        tarea.estado = request.json.get("estado", tarea.estado)
        db.session.commit()
        return tarea_schema.dump(tarea)
    
    def delete(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return '',204
    


class VistaTareasUsuario(Resource):
    @jwt_required()
    def post(self, id_usuario):
        nueva_tarea = Tarea(texto=request.json["texto"], fecha_inicio=datetime.now().date()
            , fecha_fin=datetime.strptime(request.json["fecha_fin"], '%Y-%m-%d').date()
            , estado=request.json["estado"], categoria=request.json["categoria"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.tareas.append(nueva_tarea)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una tarea con dicha descripción',409
        return tarea_schema.dump(nueva_tarea)
    
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [tarea_schema.dump(t) for t in usuario.tareas]


class VistaTareasCategoria(Resource):
    def get(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        return [tarea_schema.dump(t) for t in categoria.tareas]


