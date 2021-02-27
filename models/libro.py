from config.base_datos import bd
#si queremos usar alguna datatype especifico de una base de datos en la base
#particular , debemos de importar el dialecto para que solamente funcione
#en esa base de datos
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship

class LibroModel(bd.Model):
    __tablename__ ="t_libro"
    libroId = bd.Column(name="libro_id",
        type_=bd.Integer, 
        primary_key=True , 
        autoincrement=True, 
        nullable=False,
        unique=True)
    libroNombre= bd.Column( name="libro_npombre", type_=bd.String(45))
    libroCantidad= bd.Column( name="libro_cant", type_=bd.Integer)
    # Year solo funciona en dialecto MYSQL
    libroEdicion= bd.Column( name="libro_edicion", type_=mysql.YEAR()) #bd.YEAR
    autor = bd.Column(bd.ForeignKey('t_autor.autor_id'), 
                    name="autor_id", type_=bd.Integer, nullable=False)
    categoria = bd.Column(bd.ForeignKey('t_categoria.categoria_id'), 
                    name="categoria_id", type_=bd.Integer, nullable=False)
    sedes = relationship('SedeLibroModel', backref='libroSede')
    
    def __init__(self, nombre , cantidad ,edicion ,autor , categoria):
        self.libroNombre =nombre
        self.libroCantidad =cantidad
        self.libroEdicion =edicion
        self.autor=autor
        self.categoria= categoria
    
    def save(self):
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return{
            'libro_id': self.libroId,
            'libro_nombre':self.libroNombre,
            'libro_cant' : self.libroCantidad,
            'libro_edicion':self.libroEdicion,
            'autor_id':self.autor,
            'categoria_id':self.categoria
        }
    