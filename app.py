from flask import Flask, request
from config.base_datos import bd
from flask_restful import Api
#from models.autor import AutorModel
from controllers.autor import ( AutoresController,
                                AutorController)
#from models.categoria import CategoriaModel
#from models.libro import 
from controllers.libro import ( LibrosController,
                                LibroModel,
                                RegistroLibroSedeController)
from controllers.categoria import CategoriaController
from controllers.sede import (  SedesController,
                                LibroSedeController,
                                LibroCategoriaSedeController)

#from models.sede import SedeModel
#from models.libro import LibroModel
#from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
#para la documentacion
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '' # esta variable se usa para indicar en que parte del proyecto se encontrara la documentacion
API_URL ='/static/swagger.json' # se usa para indicar en que parte del proyecto se encuentra el archivo de la Documentacion
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Libreria Flask - Swagger Documentation"
    }
    )
app = Flask(__name__)
app.register_blueprint(swagger_blueprint)
#formato://username:password@host:port/databasename 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://fjos2li8txc0v9aa:ctsp2y87vf3f2nfy@z5zm8hebixwywy9d.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/g28x0zwytdb4d2s3'

api = Api(app)
CORS(app)
#para evitar el warnning de la funcionabilidad de sqlalchemy de track modification:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#inicio la aplicacion proveyendo las credenciales indicadas en el app.config pero aun no se ha conectado a la bd
bd.init_app(app)

#recien se conecta a la bd , pero necesita el driver para poder conectarse
#para conectarnos a una base de datos es necesario instalar el driver en este caso mysql el de abajo sera el comando 
#pip install mysqlclient
#bd.drop_all(app=app) 
bd.create_all(app=app)


@app.route('/buscar')
def buscarLibro():
    filtro = request.args.get('palabra')
    if filtro :
        busquedaLibro = LibroModel.query.filter(LibroModel.libroNombre.like('%'+filtro+'%')).all()

        if busquedaLibro:
            lista = []
            for libro in busquedaLibro:
                lista.append(libro.json())
            return{
            'success':True,
            'content':lista,
            'message':None
            }
        return{
        'success':True,
        'content':None ,
        'message':'No se encontro nada para buscar o La busqueda no tuvo efecto '
        }
    #print(request.args['palabra'])
    
# RUTAS DE MI API RESTFULL
api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController,'/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias','/categoria')
api.add_resource(LibrosController, '/libro', '/libros')
api.add_resource(SedesController, '/sede', '/sedes')
api.add_resource(LibroSedeController, '/sedeLibros/<int:id_sede>', '/sedes')
api.add_resource(LibroCategoriaSedeController, '/busquedaLibroSedeCat')
api.add_resource(RegistroLibroSedeController, '/RegistroLibroSede')

if __name__ == '__main__':
    app.run(debug=True)