# create Categoria
# Read all Categoria
from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel

serializer=reqparse.RequestParser()
serializer.add_argument(
    'categoria_descripcion',
    type=str,
    required =True, 
    help='Falta la categoria_descripcion',
    location ='json' # x defecto intenta buscar en todos los campos posibles y si lo encuentra no data error pero si queremos 
    #indicar exactamente por que medio me lo tiene que pasar debemos indicar la location
)

class CategoriaController(Resource):
    def get(self):
        categorias = CategoriaModel.query.all()
        lista = []
        for categoria in categorias:
            lista.append(categoria.json())
        return {
            'success':True,
            'content':lista,
            'message':None
        }
    def post(self):
        data = serializer.parse_args()
        nuevaCategoria = CategoriaModel(data['categoria_descripcion'])
        nuevaCategoria.save()
        return {
            'success': True,
            'content': nuevaCategoria.json(),
            'message':'Categoria creada exitosamente'
        }