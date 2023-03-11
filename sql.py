from app import db, User, Sesion, Historia

s=Sesion(nombre='Hello Python!')
db.create_all()
Historia(titulo='Python is pretty cool', autor='me', sesion=s, texto='new')
Sesion.query.all() #[]
db.session.add(s)

# db.session.rollback()
db.session.add(s)
Sesion.query.all() #[<Sesion Hello Python! >]
Historia.query.all() #[<Historia: 'Python is pretty cool'>]
h=Historia.query.all()[0] 
h.texto # 'new'
h.sesion # <Sesion Hello Python! >
h.sesion.historias
[<Historia: 'Python is pretty cool'>]
# db.session.commit(s)

#######################################
>>> from mynewapp import db, User, Sesion, Historia
>>> User.query.all()
[<User 'emerson'>]
>>> Sesion.query.all()
[<Sesion **Nueva Sesión** >]
>>> Historia.query.all()
[<Historia: 'la primera'>]
>>> h=Historia.query.all()[0]
>>> h.story
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Historia' object has no attribute 'story'
>>> h.historia
' adslk'
>>> h.fecha
datetime.datetime(2022, 9, 4, 0, 0)
>>> h.titulo
'la primera'
>>> h.AIinspiration
>>> h.ldsk
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Historia' object has no attribute 'ldsk'
>>> h.sesion
<Sesion **Nueva Sesión** >
>>> s=h.sesion
>>> s.usuario
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Sesion' object has no attribute 'usuario'
>>> s.usuarios
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Sesion' object has no attribute 'usuarios'
>>> s.usuario_id 
1 #esta funciona, pero to tiene backref
>>> me=User.query.all()
>>> me.ultima_sesion_db
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute 'ultima_sesion_db'
>>> me.is_admin
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute 'is_admin'
>>> me.is_admin=True
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute 'is_admin'
>>> me.is_admin=True
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'list' object has no attribute 'is_admin'
>>> me
[<User 'emerson'>]
>>> me=me[0]
>>> me.is_admin
False
>>> me.is_admin=True
>>> db.session.commit()
