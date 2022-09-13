# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)
#####
# need: pip install email_validator, Flask-User and others from cyborgchaman

import os
import openai
from flask import Flask, redirect, render_template, request, url_for, render_template_string
import pickle
from datetime import datetime, date
from dotenv import load_dotenv, find_dotenv
#import pymysql



#from flaskusers import create_app
from flask_user import login_required, UserManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from flask_babelex import Babel


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    #mysqlkey = os.getenv("MYSQL_KEY")
    
    SECRET_KEY = "secretkey I dont get why os key is not working here"
    #os.getenv("MYFLASK_KEY")

    
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app.sqlite'  # File-based SQL
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    # SQLALCHEMY_DATABASE_URI =f'mysql+pymysql://elcyborgchaman:mysql0Secret@elcyborgchaman.mysql.pythonanywhere-services.com/elcyborgchaman$default'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "El Cyborg Chamán"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    #USER_EMAIL_SENDER_EMAIL = 'emersonleon@gmail.com'      # email
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form



load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
#myflaskkey=os.getenv("MYFLASK_KEY")
#print(myflaskkey)
    
""" Flask application factory """
    
# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

#app.config.from_pyfile('mysettings.cfg')
# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)



# #### migrate to add new columns:
# from flask_migrate import Migrate

# migrate2 = Migrate(app, db)



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
    
#################################3



# Create all database tables
db.create_all()


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)
#userbabel=user_manager.babel
babel = Babel(app)
babel.BABEL_DEFAULT_LOCALE='es'
babel.init_app(app)

# this line is inside user_manager
#self.babel = app.extensions.get('babel', None)




# The Home page is accessible to anyone
@app.route('/')
def home():
    return render_template('home.html')



#load pickle

def pickleLoad(filename):
    pickleobject = []
    with (open(filename, "rb")) as openfile:
        while True:
            try:
                pickleobject.append(pickle.load(openfile))
            except EOFError:
                break
    return pickleobject[-1]


sesiones=pickleLoad('sesiones.pkl')
historias=pickleLoad('historias.pkl')

#####


######## Usar sql aquí, y usuarios para cada sesión


    
## incluye db y pickle
def guardarHistoria(newstory):
    newstory['datetime'] = datetime.now()
    newstory['fecha'] = date.today()
    historias.append(newstory)
    #sesion_actual=cargar_ultima_sesion(current_user)
    h=Historia(titulo=newstory['titulo'],
               autor=newstory['autor'],
               historia=newstory['historia'],
               fecha = newstory['datetime'],
               AIinspiration = newstory['AIinspiration'],
               sesion=current_user.sesion_actual())
    if h.AIinspiration=="manual":
        h.AIinspiration=""
    else:
        h.prompt=newstory['prompt']
        h.tokens_usados=newstory['usage']["total_tokens"]
        h.prompt_tokens=newstory['usage']["prompt_tokens"]    
        current_user.tokens_usados += h.tokens_usados
        
    db.session.add(h)
    db.session.commit()
    f = open("historias.pkl","wb")
    pickle.dump(historias,f)
    f.close()

################################################################


#pickle
def guardarSesionActual(name='*unsaved '):
    global historias
    nuevasesion={}
    nuevasesion['fecha'] = datetime.now()
    if name == '*unsaved ':
        name+=str(nuevasesion['fecha'])
    else:
        nuevasesion['nombre'] = name
    nuevasesion['historias']=historias
    sesiones.append(nuevasesion)

    # write the python object (dict) to pickle file
    f = open("sesiones.pkl","wb")
    pickle.dump(sesiones,f)
    f.close()

#sql
def guardarSesion(sesion,nombre):
    #if sesion.nombre == '**Nueva Sesión**':
    sesion.nombre = nombre
    db.session.commit()
    

#pickle
def borrarHistorias():
    global historias
    historias=[]

    f = open("historias.pkl","wb")
    pickle.dump(historias,f)
    f.close()

    




@app.route("/missesiones", methods=("GET", "POST"))
@login_required    # User must be authenticated
def mis_sesiones():
    global historias

    if request.method == "POST":
        myaction = request.form["myaction"]
        ##################
        if myaction == "guardarhistorias":  
            sesionname = request.form["sesionname"]
            guardarSesionActual(sesionname) #pickle
            #db SQLAlchemy
            guardarSesion(current_user.sesion_actual(), nombre=sesionname)
            #return values
            ses=current_user.sesiones
            his=current_user.sesion_actual().historias
            return render_template("sesiones.html", historias=his, sesiones=ses)

            
        ###############
        elif myaction == "nuevasesion": 
            borrarHistorias() #pickle
            current_user.nueva_sesion()
            #return values
            ses=current_user.sesiones
            his=current_user.sesion_actual().historias
            return render_template("sesiones.html", historias=his, sesiones=ses)

        ############## Va para editar_sesiones.html mover esto!
        elif myaction == "borrarsesionguardada":  
            borrarsesion = request.form["deletesesion"]
            for i in range(len(sesiones)):
                if sesiones[i]['nombre']==borrarsesion:
                    deleted=sesiones.pop(i)
                    nota=f'Se eliminó la sesión {borrarsesion}'
                    f = open("sesiones.pkl","wb")
                    pickle.dump(sesiones,f)
                    f.close()
                    break
                else:
                
                    nota='No se encontró ninguna sesión con ese nombre'
            return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)
        #######################
        elif myaction == "cargarsesionold":  
            cargarsesion = request.form["cargarsesion"]
            #pickle
            for i in range(len(sesiones)):
                if sesiones[i]['nombre']==cargarsesion:
                    historias=sesiones[i]['historias']
                    nota= f'se cargó la sesión { sesiones[i]["nombre"] }'
                    break
                else:
                    nota='No se encontró ninguna sesión con ese nombre'
                #sql
            current_user.sesionActual=Sesion.query.filter_by(user_id=current_user.id).filter_by(nombre=cargarsesion).first()
            current_user.sesion_actual_id=current_user.sesionActual.id
            db.session.commit()
            ##############################
        elif myaction == "cargarsesion":  
            cargarsesion_id = request.form["cargarsesion"]
            current_user.sesionActual=Sesion.query.filter_by(user_id=current_user.id).filter_by(id=cargarsesion_id).first()
            current_user.sesion_actual_id=current_user.sesionActual.id
            db.session.commit()
        
            #return values
            ses=current_user.sesiones
            his=current_user.sesion_actual().historias
            return render_template("sesiones.html", historias=his, sesiones=ses)

            return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)

    ses=current_user.sesiones
    his=current_user.sesion_actual().historias
    return render_template("sesiones.html", historias=his, sesiones=ses)






@app.route("/editarsesiones", methods=("GET", "POST"))
@login_required    # User must be authenticated
def editar_sesiones():
    if request.method == "POST":
        myaction = request.form["myaction"]

        ############## hacer directamente en sql
        if myaction == "borrarsesionguardada":  
            borrarsesion = request.form["deletesesion"]
            for i in range(len(sesiones)):
                if sesiones[i]['nombre']==borrarsesion:
                    deleted=sesiones.pop(i)
                    nota=f'Se eliminó la sesión {borrarsesion}'
                    f = open("sesiones.pkl","wb")
                    pickle.dump(sesiones,f)
                    f.close()
                    break
                else:
                
                    nota='No se encontró ninguna sesión con ese nombre'
            return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)

    ses=current_user.sesiones
    his=current_user.sesion_actual().historias
    return render_template("editar_sesiones.html", historias=his, sesiones=ses)











#######################
#Administrador

#### define un decorador@admin_required
@app.route('/adm/usuarios')
@login_required    # User must be authenticated
def mostrar_usuarios():
    if current_user.is_admin:
        return render_template('adm_usuarios.html', usuarios=User.query.all())
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


@app.route('/adm/sesiones')
@login_required    # User must be authenticated
def mostrar_sesiones():
    if current_user.is_admin:
        return render_template('adm_sesiones.html', sesiones=Sesion.query.all())
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


@app.route('/adm/historias')
@login_required    # User must be authenticated
def mostrar_historias():
    if current_user.is_admin:
        return render_template('adm_historias.html', historias=Historia.query.all())
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


@app.route('/adm/emails')
@login_required    # User must be authenticated
def mostrar_emails():
    if current_user.is_admin:
        return render_template('adm_emails.html', emails=Email.query.all())
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")

    

@app.route('/adm/user/<string:username>')
@login_required    # User must be authenticated
def mostrar_usuario(username):
    if current_user.is_admin:
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('adm_username.html', user=user)
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


@app.route('/adm/sesion/<string:sesionid>')
@login_required    # User must be authenticated
def mostrar_sesion(sesionid):
    if current_user.is_admin:
        sesion = Sesion.query.filter_by(id=int(sesionid)-13500).first_or_404()
        return render_template('adm_sesionid.html', sesion=sesion)
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


@app.route('/adm/story/<string:storyid>')
@login_required    # User must be authenticated
def mostrar_historia(storyid):
    if current_user.is_admin:
        historia = Historia.query.filter_by(id=int(storyid)-23500).first_or_404()
        return render_template('adm_storyid.html', post=historia)
    else:
        return render_template_string("""{% extends "base.html" %}
        {% block content %}
        El usuario no está autorizado para ver esta página...
        {% endblock %}""")


    ###############################################












@app.route("/ingresarhistoria", methods=("GET", "POST"))
@login_required
def ingresarhistoria():
    if request.method == "POST":
        nuevahistoria={}
        nuevahistoria['autor'] = request.form["autor"]
        nuevahistoria['titulo'] = request.form["titulo"]
        nuevahistoria['historia'] = request.form["historia"]
        nuevahistoria['AIinspiration'] = "manual"
        
        guardarHistoria(nuevahistoria)
        #result = request.args.get("result")
    
        return render_template("ingresarhistoria.html",
                               result=nuevahistoria)
    return render_template("ingresarhistoria.html")





@app.route("/leerhistorias", methods=("GET", "POST"))
@login_required
def leerhistorias():
    return render_template("leerhistorias.html", historias=current_user.sesion_actual().historias)
    



#############
@app.route("/requestemail", methods=("GET", "POST"))
@login_required
def tokensemailrequest():
    if request.method == "POST":
        emailrecibido= request.form["email"]
        new_email=Email(email=emailrecibido, status="to be confirmed",
              user_id=current_user.id)
        db.session.add(new_email)
        db.session.commit()

        # current_user.myuseremail=f'TBC id[{new_email.id}:]'+ emailrecibido
        return render_template("emailrecibido.html", new_email=new_email)
    return render_template("tokensemailrequest.html")


def confirm_email(user, email):
    """desde python, from mynewapp import db, User, Email, confirm_email"""
    user.email_confirmed_at=datetime.utcnow
    email.is_confirmed=True
    email.status="confirmed"
    current_user.myuseremail= email.email

########

TOKENS_LIMIT=6000
TOKENS_EMAIL_REQUEST=5000

def openAI_completion(prompt, user, length=700, temp=0.8):
    if user.tokens_usados>TOKENS_LIMIT and user.myuseremail=='':
        return "tokens limit", 0
    else:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=temp,
            max_tokens=length,
            presence_penalty=1.2,
            frequency_penalty=0.7,
            user=current_user.__repr__()
        )
        
    return response.choices[0].text, response.usage



    

#############################################

    
@app.route("/generarhistoria", methods=("GET", "POST"))
@login_required
def generarhistoria():
    if request.method == "POST":
        #alargar
        alargar_id = request.form["alargarhistoria"]
        if alargar_id == "No alargar":
            alargarHistoria = "No alargar"
        else:
            alargarHistoria=Historia.query.filter_by(id=int(alargar_id)).first_or_404()
        #palabras
        palabrasInspiradoras = request.form["palabrasInspiradoras"]
       
        historiassql=current_user.sesion_actual().historias
        # historiasMarcadas=[h for h in historiassql if
        #                    request.form[h.id]=="True"]
        historiasMarcadas=[]

        printtext="<br>print "
        #printtext += f"<br>{alargarHistoria.titulo}"
        #printtext += f"<br>{[h.titulo for h in historiassql]}"
        for historia in historiassql:
            try:
                # only valid for checked items.
                h_id=request.form[str(historia.id)]
            except KeyError:
                printtext += f"<br>{historia.id}<br>"
                #unchecked.append(historia)
            else:
                # execute if no exception
                historiasMarcadas.append(historia)
          
        prompt, nuevahistoria, tokens = openAI_generar_historia(alargarHistoria, palabrasInspiradoras, historiasMarcadas, current_user)
        if nuevahistoria=='tokens limit':
            return render_template("tokensemailrequest.html", tokens_limit=TOKENS_LIMIT)
        else:
            result = {'prompt':prompt, 'historia':nuevahistoria,
                      'autor':"openAI", 'usage':tokens}
            if alargarHistoria=="No alargar":
                result['titulo']=openAI_generar_titulo(result['historia'])
            else:
                if alargarHistoria.autor[-6:]=='openAI':
                    result['autor'] = alargarHistoria.autor
                    result['titulo']=alargarHistoria.titulo
                else:
                    result['autor']=alargarHistoria.autor+' + openAI'
                if alargarHistoria.autor[-1]=='+':
                    result['titulo']=alargarHistoria.titulo
                else:
                    result['titulo']=alargarHistoria.titulo+'+'
            result['AIinspiration']=openAI_AIinspiration(alargarHistoria, palabrasInspiradoras, historiasMarcadas)
            guardarHistoria(result)
            if current_user.myuseremail=='' and current_user.tokens_usados>TOKENS_EMAIL_REQUEST:
                return render_template("tokensemailrequest.html", tokens_limit=TOKENS_LIMIT, result=result)
            else:
                return render_template("generarhistoria.html", historias=current_user.sesion_actual().historias, result=result)
        # return openAI_AIinspiration(alargarHistoria, palabrasInspiradoras, historiasMarcadas)#+printtext
    #render_template("generarhistoria.html", historias=current_user.sesion_actual().historias, result=result)
        

    #result = request.args.get("result")
    return render_template("generarhistoria.html", historias=current_user.sesion_actual().historias)


def openAI_generar_historia(alargar, palabras, historias, user):
    #prompt=openAI_final_prompt(alargar, palabras, historias)
    prompt=openAI_prompt_alargarconpalabras(alargar, palabras)
    story, usage= openAI_completion(prompt, user)
    return prompt, story, usage 






####################################################
#prompts generar historias

def openAI_AIinspiration(alargarHistoria, palabrasInspiradoras, historiasMarcadas):
    #AIinspiration
    if alargarHistoria == "No alargar":
        alargartext=""
    else:
        alargartext='extensión '#de la historia "{alargarHistoria.titulo}". '
    if len(historiasMarcadas)>0:
        historiasjoin='", "'.join([post.titulo for post in historiasMarcadas])
        historiastext= f' se tuvieron en cuenta las historias "{historiastext}")'
    else:
        historiastext=""
    return f'{alargartext}inspirada en las palabras: {palabrasInspiradoras};{historiastext}'



def openAI_final_prompt(alargarHistoria, palabrasInspiradoras, historiasMarcadas):
    number=1
    y=" y "
    historiasanteriores=""
    palabras=""
    if len(historiasMarcadas)>0:
        hayanteriores="las historias anteriores"
        nostories=False
        for h in historiasMarcadas:
            historiasanteriores+= f'*HISTORIA {number}: {h.historia}\n'
            number+=1
    else:
        nostories=True
        y=""
        hayanteriores=""

    if len(palabrasInspiradoras)>0:
        haypalabras="las palabras principales,"
        palabras+= f'*PALABRAS PRINCIPALES: {palabrasInspiradoras};\n'
        nowords=False
    else:
        nowords=True
        y=""
    if nowords and nostories:
        prompt_intro=""
    else:
        prompt_intro=f"{historiasanteriores}{palabras}\n Basado en {hayanteriores}{y}{haypalabras}"
    if alargarHistoria == "No alargar":
        request=f" openAI creará una nueva historia.\n*HISTORIA FINAL: "
    else:
        request=f''' extender la siguiente historia, tomar la HISTORIA INICIAL y luego continuarla.
*HISTORIA INICIAL:
{alargarHistoria.historia} 
*CONTINUACION:'''
    return prompt_intro+request


def openAI_prompt_alargarconpalabras(alargarHistoria, palabrasInspiradoras):
    entrenamiento1="""
*Ejemplo:
*PALABRAS PRINCIPALES: magia sol beso; 
 *HISTORIA INICIAL: El bebé simio roca luna estaba muy feliz. Era el primer simio en vivir en la luna y quería descubrir todo lo que podía acerca de este nuevo mundo. Un día, se encontró con un enorme monstruo de roca. El simio no tenía miedo y comenzó a trepar por la roca para llegar al top. 
*CONTINUACION: Pero, cuando llegó a la cima, se dio cuenta de que no era un monstruo de roca, sino una gigantesca sombra proyectada por el poderoso sol. La figura le sonrió y le dijo: "Bienvenido a mi mundo. Soy la magia que llena la luna. He estado esperando por ti". Y una princesa de polvo lunar apareció, se acercó al bebe simio y le dio un beso.
"""
    palabras= f'*PALABRAS PRINCIPALES: {palabrasInspiradoras};\n'
    
    if alargarHistoria=="No alargar":
        return generate_prompt_de_palabras(palabrasInspiradoras)
    else:
        prompt_intro=f"Basado en las palabras principales, alargar la historia inicial escribiendo una continuación.\n {entrenamiento1}{palabras}"
        request=f''' 
*HISTORIA INICIAL:
{alargarHistoria.historia} 
*CONTINUACION:'''
    return prompt_intro+request




    






###################################################
@app.route("/crearhistoria", methods=("GET", "POST"))
@login_required
def crearhistoria():
    if request.method == "POST":
        checked=[]
        #unchecked=[]
        historiassql=current_user.sesion_actual().historias
        for historia in historiassql:
            try:
                # only valid for checked items.
                tit=request.form[historia.titulo]

            except KeyError:
                pass
                #unchecked.append(historia)
            else:
                # execute if no exception
                checked.append(historia)
            
        prompt, nuevahistoria, tokens_usados = openAI_create_story(checked,current_user)
        if nuevahistoria=='tokens limit':
            return render_template("tokensemailrequest.html", tokens_limit=TOKENS_LIMIT)
        else:
            result = {'prompt':prompt, 'historia':nuevahistoria,
                  'autor':"openAI", 'usage':tokens_usados}
            result['titulo']=openAI_generar_titulo(result['historia'])
            result['AIinspiration']=str([story.titulo for story in checked ])
            guardarHistoria(result)
            return render_template("crearhistoria.html", historias=current_user.sesion_actual().historias, result=result, checked=checked)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    #result = request.args.get("result")
    return render_template("crearhistoria.html", historias=current_user.sesion_actual().historias)



def openAI_create_story(historias, user):
    if len(historias)<2:
        hist=historias+historias0
    prompt=generar_prompt_de_historias(historias)
    story, usage= openAI_completion(prompt, user)
    return prompt, story, usage 






###################
def generar_prompt_de_historias(historias):
    n=len(historias)+1
    prompt=f"{n} personas escribieron historias."
    for story in historias:
        prompt+= f"\n{story.autor} escribió: "
        prompt+= story.historia
    return prompt+"\nEl último escribió:"




    






    
story1="No sabía que hacer. Entonces me quedé quieto. Estaba muy cansado, necesitaba comer algo, pero casi no podía moverme, y mi estomago se sentía indispuesto. Así que me quedé en el suelo, inmovil y cerré los ojos. Tuve una visión. Mi cuerpo no existía, y mi mente era parte de una gran máquina. La mente del mundo operaba como una computadora, y yo era parte del algoritmo. Mis ideas programaban las acciones presentes y futuras. Mis acciones eran consecuencia de los programas que estaban instalados en mi ser. El adn era una forma de lenguaje de programación, el sistema operativo y la información para crear el hardware una y otra vez estaban ahí acumuladas. La evolución era simplemente un proceso de programación y reprogramación de maquinas que se programan a sí mismas. La historia y la cultura nos cargan con programas milenarios transmitidos a travez de el lenguaje. También a través de programas de imitación, empatía e intuición, que vienen en el adn, pero que nos permiten conectividad. Vamos descargando información que nos permite ir mejorando nuestros algoritmos, actualizarnos y resolver cada vez mejor los diferentes retos que plantea la vida. Cada celula del cuerpo actúa siguiendo el algoritmo. Sus comandos operan a niveles muy básicos, pero la complejidad de toda esta creación es infinita. El universo se manifiesta como un gran fractal de increible belleza y simetría. Leyes simples formando patrones avanzados, geometrías mágicas en cada atomo, en cada copo de nieve, en cada galaxia, en cada cerebro. Me sentí agradecido y decidí que no quería morir. En ese momento el amor se acercó a mí y me ofreció alimento. Reuní todas mis fuerzas para incorporarme, y prové el delicioso nectar que me trajo de nuevo al mundo."
#"Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez."
story2 = "Estaba sentada en la terraza, mirando las estrellas y pensando en mi amiga. Ella me había pedido perdón y yo le había dicho que sí, pero aún no podía dejar de pensar en todo lo que había pasado. Nos habíamos peleado por un chico, y ella me había dicho algunas cosas muy hurtful. No podía dejar de pensar en lo mucho que la quería y en lo afortunada que era de tenerla en mi vida. De pronto, la puerta se abrió y ella apareció. Nos miramos a los ojos y supimos que todo estaba bien. Nos abrazamos y nos dimos un beso." 
historias0=[{'autor': 'eme', 'titulo': 'El algoritmo', 'historia': story1},{'autor': 'openAI', 'titulo': 'Paseito con mamá', 'historia': story2},  {'historia': '\n\nA veces me siento como si estuviera en una película. Todo es muy brillante y las luces son muy intensas. Me siento como si estuviera en un sueño. Todo es un poco confuso y no puedo despertar. Me siento atrapada en mi propia mente. La única vez que puedo salir de este sueño es cuando estoy en el baño. Me siento en la bañera y me quedo dormida. Tengo que estar en el baño para que pueda despertar. Me siento como si estuviera en una película de terror. Tengo que estar en el baño para no morir.', 'autor': 'openAI', 'titulo': ' El baño'}]







##################################3
def openAI_generar_titulo(historia):
    """Usando openAI generamos el título de una historia"""
    titleprompt=f"""Determine el título de las  siguientes historias. *cuento: Un domingo soleado, cuya fecha no recuerdo, me
alisté para trabajar. Mi madre me dio la bendición
y me dirigí hacia la misa de doce en la iglesia
del 20 de Julio. Al llegar observé que la iglesia
estaba repleta y comencé a rezar. Pedí por un
día a la mano de Dios y que este me protegiera.
De repente comenzó la misa. El padre salió y
empezaron las alabanzas. Casi al instante, mi jefe
me llamó para que me afanara por empezar mi
labor. Mirando a la figura de Cristo, pedí perdón,
le apunté a mi cliente y disparé. Título del cuento: Por el pan de cada día
*cuento:{historia}. Título del cuento:"""
    title = openai.Completion.create(
        model="text-davinci-002",
        prompt=titleprompt,
        temperature=0.6,
        max_tokens=20
    )
    return title.choices[0].text



##################################

@app.route("/historiadepalabras", methods=("GET", "POST"))
@login_required
def historiadepalabras():
    if request.method == "POST":
        palabras = request.form["story1"]
        myprompt=generate_prompt_de_palabras(palabras)
        ## cambiado recientemente
        story, usage= openAI_completion(myprompt, current_user)
        if story=='tokens limit':
            return render_template("tokensemailrequest.html", tokens_limit=TOKENS_LIMIT)
        else:

            # response = openai.Completion.create(
            #     model="text-davinci-002",
            #     prompt=myprompt,
            #     temperature=0.6,
            #     max_tokens=800
            # )
            # story=response.choices[0].text
        
            result = {'AIinspiration':palabras, 'prompt':myprompt,
                      'historia': story, 'autor':"openAI",
                      'usage':usage}
            result['titulo']=openAI_generar_titulo(result['historia'])
            guardarHistoria(result)
            return render_template("historiadepalabras.html", result=result)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("historiadepalabras.html", result=result)


#Ejemplo 1: *Palabras principales: delincuencia, leyes, billetes, subsistir, acecho, sirena, salvado, despojado, pertenencias, Bogotá.
#*Historia: La delincuencia Todos los días corro por miedo a que me cojan. Al igual que muchos, lo hago incumpliendo leyes, por conseguir billetes, todo por subsistir. Acecho a las personas de aquí, todos me odian por el trabajo que tengo, no saben lo que siento al cometer este hecho, me atormenta la sirena que a veces me viene persiguiendo. De todas las que me he salvado orando por un santo, el cual me está cobijando y no me ha desamparado. He despojado a muchos de sus pertenencias, las cuales utilizo para llevar de comer a mi familia en mi Bogotá.


def generate_prompt_de_palabras(palabras):
    """Prompt usado en 'historiadepalabras', donde con unas palabras se genera una historia"""
    return """ OpenAI creará historias usando grupos de palabras principales. 
Ejemplo 1: *PALABRAS PRINCIPALES: homosexualidad, rechazo, dolor, muerte.
*historia: Barrio Danubio, día viernes. Termino de retocar mi maquillaje y vestido, doy vuelta frente al espejo... Por primera vez me gusta lo que veo. ¡Soy feliz! Saliendo de mi casa me encuentro al chico que siempre me ha gustado, sin pensarlo dos veces le confieso mi amor; su respuesta hizo que sintiera algo en mi estómago... Pero no son las mariposas soñadas, sino su cuchillo perforándome mientras grita palabras de asco. No entiendo el motivo; después de unos segundos comprendo: es porque soy hombre.
Ejemplo 2: *PALABRAS PRINCIPALES: 
"""+palabras+"*Historia:"

    

#########alargarhistoria##############
@app.route("/alargarhistoria", methods=("GET", "POST"))
@login_required
def alargarhistoria():
    if request.method == "POST":
        titulo=request.form['alargarhistoria']
        historiassql=current_user.sesion_actual().historias
        for story in historiassql:
            if story.titulo==titulo:
                prompt, nuevaparte, usage = openAI_extend_story(story, current_user)
                if nuevaparte=='tokens limit':
                    return render_template("tokensemailrequest.html", tokens_limit=TOKENS_LIMIT)
                else:
                    if story.autor[-6:]=='openAI':
                        newautor=story.autor
                    else:
                        newautor=story.autor+' + openAI'
                    historiaalargada=story.historia+""" *** """+nuevaparte
                    result = {'prompt':prompt,
                          'historia':historiaalargada,
                          'autor':newautor, 'usage':usage}
                    result['titulo']=story.titulo+'+'
                    result['AIinspiration'] = "alargar historia" 
                    guardarHistoria(result)
                    return render_template("alargarhistoria.html", historias=current_user.sesion_actual().historias, result=result)
            else:
                pass
        note="no se encontró la historia buscada "+titulo
        return render_template("alargarhistoria.html", historias=current_user.sesion_actual().historias, note=note)
    return render_template("alargarhistoria.html", historias=current_user.sesion_actual().historias)













def openAI_extend_story(story, user):
    prompt=generar_prompt_alargar_historia(story)
    newstory, usage= openAI_completion(prompt, user)
    return prompt, newstory, usage

def generar_prompt_alargar_historia(story):
    prompt= """Extender una historia. Tomar una historia empezada y luego continuarla.
Ejemplo 1. Historia inicial: Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez.
Continuación: Mis sensores comienzan a recibir la luz. Se activan los circuitos y en mi tarjeta gráfica aparece un archivo que interpreto como imágenes del planeta. Gracias a archivos detallados identifico plantas, rios y montañas. Entiendo como moverme y exploro a mi alrededor. Hay arena, pero no es un problema para mis piernas, programadas para caminar como humano. No veo personas ni animales a mi alrededor, pero guardo la esperanza de que la vida en la tierra vuelva a reproducirse y ser como antes.
Historia inicial: """
    ending="""
Continuación:"""
    return prompt+story.historia+ending




if __name__=='__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
