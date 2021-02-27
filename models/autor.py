from config.base_datos import bd

class AutorModel(bd.Model):
    #para cambiar el nombre de la tabla a crearse 
    __tablename__ ="t_autor"
    autorId= bd.Column(
        name="autor_id",
        type_=bd.Integer, 
        primary_key=True , 
        autoincrement=True, 
        nullable=False,
        unique=True)
    autorNombre= bd.Column(
        name="autor_nombre",
        type_=bd.String(45))
    #si no indicamos un backref flask lo generara aleatoriamente y sera mas complicado
    #averiguar su nombre el backref sirve para usarse en el modelo hijo(para que nos devuelva los datos del padre)
    #https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship
    # lazy => define cuando SQLALchemy va a cargar la data de la base de datos
    # 'select' / True => es el valor por defecto, significa que SQLALchemy cargará los datos segun sea necesario 
    # 'join'/ False => le dice a SQLALChemy que cargue la relacion en la misma consulta usan un JOIN 
    # 'subquery' => trabaja como un JOIN pero en su lugar de hacerlo en una misma consulta lo hara en una subconsulta
    # 'dynamic' => es especial si se tiene muchos elementos y se desea aplicar filtros adicionales. SQLAlchemy devolvera otro objeto de consulta que se puede customizar antes de cargar los elementos de la bd. Al hacer esto tener en cuenta que el proceso de lectura de la bd puede ser mayor y x ende tener un mayor tiempo de espera
    libros=  bd.relationship('LibroModel', backref='autorLibro', lazy=True)# en el caso de fk se apunta al nombre de la tabla , mientras que en 
    #los relationship se apunta al nombre del modelo
    #en el caso de los relationship normal no puede estar creado la tabla aun 
        
    def __init__(self, nombreAutor):
        self.autorNombre = nombreAutor
    
    def __str__(self):
        return '{}:{}'.format(self.autorId , self.autorNombre)

    def save(self):
        #el metodo session devuelve la sesion actual y evita que se cree una nueva 
        #session y asi ralentizar la conexcion a mi bdist_dumb
        #el metodo add sirve para agregar toda mi instancia (mi nuevo autor) a un formato 
        #que sea valido para la bd
        bd.session.add(self)
        # el commit sirve para que los cambios realizados a la bd se hagan efectivo , esto 
        #esto generalmente se usa con transacciones
        bd.session.commit()

    def json(self):
        return{
            'autorId': self.autorId,
            'autorNombre': self.autorNombre
        }
    def delete(self):
        # con el delete se hace la eliminacion TEMPORAL DE LA BASE DE DATOS
        bd.session.delete(self)
        bd.session.commit()