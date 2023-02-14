################## Mis Clases

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    
    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    myuseremail = db.Column(db.String(120), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())
    tokens_usados = db.Column(db.Integer, nullable=False, default=0)
    
    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    sesion_actual_id=db.Column(db.Integer, nullable=False, default=-111)
    #-111= no sesion created

    def cargar_ultima_sesion(self):
        if self.sesion_actual_id==-111:
            self.nueva_sesion()
        else:
            self.sesionActual=Sesion.query.filter_by(id=self.sesion_actual_id)[0]
        return self.sesionActual
            
    def sesion_actual(self):
        try:
            return self.sesionActual
        except:
            return self.cargar_ultima_sesion()
    def nueva_sesion(self):
         self.sesionActual=Sesion(nombre='**Nueva Sesión**',  user=self)
         #usuario_id=self.id,
         db.session.commit()
         self.sesion_actual_id = self.sesionActual.id
         db.session.commit()
        
            
    is_admin=db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f'<User {self.username} >'


# user_sessions = db.Table('usersessions', 
#     db.Column('sesion_id', db.Integer, db.ForeignKey('sesion.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
# )


    

class Sesion(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    #many-to many (add table above)
    # usuarios = db.relationship('User', secondary=user_sessions,
    #             lazy='subquery', backref=db.backref('sesiones', lazy=True))
    
    #one to many. What is wrong here?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
       nullable=False)
    user = db.relationship('User',
       backref=db.backref('sesiones', lazy=True))
    #usuario_id=db.Column(db.Integer,nullable=True)#my manually created user id.

    is_public=db.Column(db.Boolean, default=False)
    is_shared=db.Column(db.Boolean, default=False)
    #historias (backref)

    def __repr__(self):
        return f'<Sesion {self.nombre} id {self.id}>' 



class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    AIinspiration = db.Column(db.String(300), nullable=True)
    prompt = db.Column(db.Text, nullable=True)
    #flagged = db.Column(db.Text, default='')
    tokens_usados = db.Column(db.Integer, nullable=False, default=0)
    prompt_tokens = db.Column(db.Integer, default=0)
    historia = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    #story=db.Column(JSON, nullable=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesion.id'),
        nullable=False)
    sesion = db.relationship('Sesion',
        backref=db.backref('historias', lazy=True))

    def __repr__(self):
        return '<Historia: %r>' % self.titulo


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, server_default='')
    status = db.Column(db.String(120), nullable=False, server_default='')
    is_confirmed=db.Column(db.Boolean, default=False)
    user_id=db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<Historia: {self.email}>'  


#################################3
