from mynewapp import db, User, Sesion, Historia

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
