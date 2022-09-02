# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    
    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())
    
    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    #sesiones = db.relationship('Sesion', secondary=user_sessions, lazy='subquery',
    #    backref=db.backref('usuarios', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

user_sessions = db.Table('tags',
    db.Column('sesion_id', db.Integer, db.ForeignKey('sesion.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Sesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)


    def __repr__(self):
        return f'<Sesion {self.name} >' 



class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    sesion_id = db.Column(db.Integer, db.ForeignKey('sesion.id'),
        nullable=False)
    sesion = db.relationship('Sesion',
        backref=db.backref('historias', lazy=True))

    def __repr__(self):
        return '<Historia: %r>' % self.title


