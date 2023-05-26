###Instrucciones:
# copy a database backup to the file: quickstart.sqlite
# run: python3 addcolumnsql.py
# run: python3 colecciones.py (make sure generar_todo() and update_user_info
# are uncommented)
# check that there is only one mainroot, one public and one colection for each user
###############################
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
    public = Collection(nombre='public', parent_id=1, creator_id=0)
    public.admins.append(me)
    db.session.commit()

    #if False:
def generar_colecciones_por_usuario():
    for user in User.query.all():
        #print(user)
        usercolec=Collection(nombre=f'Historias de {user.username}', parent_id=1, creator_id=0)
        db.session.commit()

        # user.mis_historias_id = usercolec.id
        # print(type(usercolec.id))
        # print(user.mis_historias_id)

        usercolec.admins.append(user)
        usercolec.members.append(user)
        usercolec.can_write='only admins'
        for sesion in user.sesiones:
            for hist in sesion.historias:
                print(hist.titulo)
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
    
def print_collections():    
    for colec in Collection.query.all():
        print(  f'id: {colec.id}   nombre: {colec.nombre}')
        print(f'admins: {[user.username for user in colec.admins]}')
        #print(colec.admins)
        #print(type(colec.historias))
        print(colec.number_of_publications)
        for hist in colec.historias:
            print(hist.titulo)
            # for hist in colec.historias:
            #     print(hist)

def print_user_info():    
    for user in User.query.all():
        """this patch might cause troubles in case two users have the same username.  I will just outcomment it now, but need to be uncommented later"""
        if user.mis_historias_id==None:
            usercolec=Collection.query.filter_by(nombre=f'Historias de {user.username}')[0]
            user.mis_historias_id = usercolec.id
            db.session.commit()
            print(  f'{user.id}:   {user.username}, mis historias id {user.mis_historias_id}')


def update_user_info():    
    """this patch might cause troubles in case two users have the same username. """
    for user in User.query.all():
        if user.mis_historias_id==None:
            usercolec=Collection.query.filter_by(nombre=f'Historias de {user.username}')[0]
            user.mis_historias_id = usercolec.id
            db.session.commit()
            print(  f'{user.id}:   {user.username}, mis historias id {user.mis_historias_id}')
    

if __name__=='__main__':
    db.create_all()

    me=User.query.all()[0]
    
    #generar_todo()
    mainroot=Collection.query.all()[0]
    public=Collection.query.all()[1]

    print_collections()
    print_user_info()    
    #update_user_info()    
     
