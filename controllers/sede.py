from flask_restful import Resource ,reqparse
from models.sede import SedeModel
#from models.sedeLibro import SedeLibroModel
from models.libro import LibroModel
#get all sede
#create sede 
#vincula una sede con varios libros y viceversa(un libro con varias sedes)

#busqueda de todos los libros de una sede 
#busqueda de todos los libros de una sede segun su categoria


serializer= reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    location='json',
    dest='latitud'
)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Falta la sede_ubicacion',
    location='json',
    dest='ubicacion'
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    location='json',
    dest='longitud'  #es como se va a llamar una vez que hemos usado el metodo parse_args()
)


class SedesController(Resource):
    def post(self):
        data = serializer.parse_args()        
        print(data)
        # Los tipos de datos que no son ni numericos ni strings = decimal, fecha, 
        # no se pueden serializar hay que convertirlos en string en el modelo
        nuevaSede = SedeModel(data['ubicacion'], data['latitud'] , data['longitud'])
        nuevaSede.save()
        return {
            'success':True,
            'content':nuevaSede.json(),
            'message':'Se creo la sede correctamente'
        }

    def get(self):
        sedes = SedeModel.query.all()
        lista = []
        for sede in sedes:
            lista.append(sede.json())
        return {
            'success':True,
            'content':lista,
            'message':None
        }

#busqueda de todos los libros de una sede que
class LibroSedeController(Resource):
    def get(self,id_sede):
        sede = SedeModel.query.filter_by(sedeId = id_sede).first()
        libros=[]
        sedelibros = sede.libros # todos mis sedelibros
        for sedeLibro in sedelibros:
            libro = sedeLibro.libroSede.json()
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            ##forma abreviada pero no recomendada
            libro['Categoria'] = sedeLibro.libroSede.categorialibro.categoriadescripcion
            # otra forma de hacerlo segun buenas Practicas
            libro['Categoria2'] = sedeLibro.libroSede.categorialibro.json()
            #del libro['categoria']['categoria_id']
            #del libro['autor_id']
            libros.append(libro)
            
            # print(sedeLibro.libroSede.json())
            resultado = sede.json()
        resultado['libros'] = libros
        return {
            'success': True,
            'content': resultado
        }

class LibroCategoriaSedeController(Resource):
    
    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')
        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta el categoria_id',
            location='args' # sirve para que me lo mande por el querystring (de forma dinamica)
        )       
        serializer.add_argument(
        'sede',
        type=int,
        required =True, 
        help='Falta la sede',
        location ='args' # con json me lo envia por el body
        )
        data = serializer.parse_args()
        #la del profe
        sede = SedeModel.query.filter_by(sedeId = data['sede']).first()
        resultado=[]
        for sedelibro in sede.libros:
            print (sedelibro.libroSede.categoria)
            if(sedelibro.libroSede.categoria == data['categoria']):
                resultado.append(sedelibro.libroSede.json())
        # mi forma revisar 
        #sede = SedeModel.query.filter_by(sedeId= data['sede']).first()
        #sedeLibros = sede.libros
        #resultado = []
        #for sedeLibro in sedeLibros:
        #    libro =sedeLibro.libroSede.categorialibro
        #    print(libro.json())
        #    categoria = libro.categoria
        #    if categoria.categoriaId == data['categoria']:
        #        resultado.append(libro.json())
        return{
            'success':True,
            'content': resultado,
            'message':"Exito"
        }, 200