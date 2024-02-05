from flask import request
from ..modelos import db, Categoria, CategoriaSchema, Usuario, UsuarioSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

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
        db.session.add(nuevo_usuario)
        db.session.commit()
        return 'Usuario creado exitosamente', 201
    
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
        tarea.fecha_fin = request.json.get("fecha_fin", tarea.fecha_fin)
        tarea.estado = request.json.get("estado", tarea.estado)
        db.session.commit()
        return tarea_schema.dump(tarea)
    
    def delete(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return '',204
    



"""
class VistaAlbumsUsuario(Resource):

    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]

class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]


"""