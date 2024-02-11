from .main import create_app
from flask_restful import Api
# from modelos import db
from .modelos import db
# from vistas import VistaCategoria, VistaCategorias, VistaLogIn, VistaSignIn, VistaTarea, VistaUsuario, VistaTareasUsuario, VistaTareasCategoria
from .vistas import VistaCategoria, VistaCategorias, VistaLogIn, VistaSignIn, VistaTarea, VistaUsuario, VistaTareasUsuario, VistaTareasCategoria
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCategorias, '/categorias')
api.add_resource(VistaCategoria, '/categoria/<int:id_categoria>')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaTarea, '/tarea/<int:id_tarea>')
api.add_resource(VistaTareasUsuario, '/usuario/<int:id_usuario>/tareas')
api.add_resource(VistaTareasCategoria, '/categoria/<int:id_categoria>/tareas')


jwt = JWTManager(app)