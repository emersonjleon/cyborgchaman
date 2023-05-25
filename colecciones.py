import sqlalchemy
import sqlalchemy.ext.declarative
import datetime
from app import app, db, User, Sesion, Historia, Collection, histcolec


#primera colección y una historia
def generar_coleccion_mainroot():
    mainroot = Collection(nombre='mainroot', parent_id=-1, creator_id=0)
    mainroot.admins.append(me)
    db.session.commit()
    

#if mainroot.nombre=='mainroot':
def generar_coleccion_public():
    public = Collection(nombre='public', parent_id=mainroot.id, creator_id=0)
    public.admins.append(me)
    db.session.commit()

    #if False:
def generar_colecciones_por_usuario():
    for user in User.query.all():
        print(user)
        usercolec=Collection(nombre=f'Historias de {user.username} {user.id}', parent_id=mainroot.id, creator_id=0)
        usercolec.admins.append(me)
        usercolec.members.append(user)
        usercolec.can_write='only members'
        for sesion in user.sesiones:
            for hist in sesion.historias:
                usercolec.historias.append(hist)
        db.session.commit()

def generar_todo():
    generar_coleccion_mainroot()
    mainroot=Collection.query.all()[0]
    generar_coleccion_public()
    public=Collection.query.all()[1]

    generar_colecciones_por_usuario()


    #hist=Historia.query.all()[-1]
    #public.historias.append(hist)
    db.session.commit()
    

        # for user in User.query.all():
        #     print(user)
    
    

if __name__=='__main__':
    db.create_all()

    me=User.query.all()[0]
    
    #generar_todo()
    mainroot=Collection.query.all()[0]
    public=Collection.query.all()[1]

    
    
    for colec in Collection.query.all():
        print(f'nombre: {colec.nombre}')
        print(f'admins: {[user.username for user in colec.admins]}')
        #print(colec.admins)
        print(type(colec.historias))
        print(colec.number_of_publications)
        
        # for hist in colec.historias:
        #     print(hist)


    
        #return Collection.query.filter_by_name'Historias de {user.username} {user.id}'
