from config.base_datos import bd
from sqlalchemy.orm import relationship

class CategoriaModel(bd.Model):
    __tablename__ ="t_categoria"
    categoriaId = bd.Column(name="categoria_id",
        type_=bd.Integer, 
        primary_key=True , 
        autoincrement=True, 
        nullable=False,
        unique=True)
    categoriadescripcion= bd.Column( name="categoria_descripcion", type_=bd.String(45) , nullable=False)
    # esto no crea las relaciones simplemente sirve para al momento de hacer consultas con JOIN's
    libros = relationship('LibroModel', backref='categorialibro', lazy=True)

    def json(self):
        return{
            'categoria_Id': self.categoriaId,
            'categoria_descripcion': self.categoriadescripcion
        }

    def __init__(self,nombre):
        self.categoriadescripcion =nombre
    
    def save(self):
        bd.session.add(self)
        bd.session.commit()
