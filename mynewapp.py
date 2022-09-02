# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)
#####
# need: pip install email_validator, Flask-User and others from cyborgchaman

import os
import openai
from flask import Flask, redirect, render_template, request, url_for
import pickle
from datetime import datetime, date
from dotenv import load_dotenv, find_dotenv



#from flaskusers import create_app
from flask_user import login_required, UserManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app2.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Flask-User QuickStart App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    #USER_EMAIL_SENDER_EMAIL = 'emersonleon@gmail.com'      # email
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form


""" Flask application factory """
    
# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

babel = Babel(app)
babel.BABEL_DEFAULT_LOCALE='es'

#app.config.from_pyfile('mysettings.cfg')
# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)





################## Mis Clases

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
    manualemail = db.Column(db.String(120), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())
    
    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    

    def __repr__(self):
        return '<User %r>' % self.username


user_sessions = db.Table('usersessions', 
    db.Column('sesion_id', db.Integer, db.ForeignKey('sesion.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


    

class Sesion(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    # usuarios = db.relationship('Usuarios', secondary=user_sessions,
    #             lazy='subquery', backref=db.backref('sesiones', lazy=True))


    def __repr__(self):
        return f'<Sesion {self.nombre} >' 



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
        return '<Historia: %r>' % self.titulo


#################################3




# Create all database tables
db.create_all()


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

# The Home page is accessible to anyone
@app.route('/')
def home():
    return render_template('home.html')



@app.route('/usuario/<string: username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

###############################################

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

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



def borrarHistorias():
    global historias
    historias=[]

    f = open("historias.pkl","wb")
    pickle.dump(historias,f)
    f.close()


def guardarHistoria(story):
    story['datetime'] = datetime.now()
    story['fecha'] = date.today()
    historias.append(story)
    f = open("historias.pkl","wb")
    pickle.dump(historias,f)
    f.close()





@app.route("/miperfil", methods=("GET", "POST"))
@login_required    # User must be authenticated
def editar_sesiones():
    global historias

    if request.method == "POST":
        myaction = request.form["myaction"]
        ##################
        if myaction == "guardarhistorias":  #nueva sesion
            sesionname = request.form["sesionname"]
            guardarSesionActual(sesionname)

            return render_template("sesiones.html", historias=historias, sesiones=sesiones)
        ###############
        elif myaction == "borrarhistorias":  #caution
            borrarHistorias()
            return render_template("sesiones.html", historias=historias, sesiones=sesiones)
        ##############
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
        elif myaction == "cargarsesion":  
            cargarsesion = request.form["cargarsesion"]
            for i in range(len(sesiones)):
                if sesiones[i]['nombre']==cargarsesion:
                    historias=sesiones[i]['historias']
                    nota= f'se cargó la sesión { sesiones[i]["nombre"] }'
                    break
                else:
                    nota='No se encontró ninguna sesión con ese nombre'
            return render_template("sesiones.html", historias=historias, sesiones=sesiones, nota=nota)


    return render_template("sesiones.html", historias=historias, sesiones=sesiones)



@app.route("/ingresarhistoria", methods=("GET", "POST"))
def ingresarhistoria():
    if request.method == "POST":
        nuevahistoria={}
        nuevahistoria['autor'] = request.form["autor"]
        nuevahistoria['titulo'] = request.form["titulo"]
        nuevahistoria['historia'] = request.form["historia"]
        
        guardarHistoria(nuevahistoria)
        #result = request.args.get("result")
    
        return render_template("ingresarhistoria.html",
                               result=nuevahistoria)
    return render_template("ingresarhistoria.html")





@app.route("/leerhistorias", methods=("GET", "POST"))
def leerhistorias():
    return render_template("leerhistorias.html",historias=historias)
    




@app.route("/crearhistoria", methods=("GET", "POST"))
def crearhistoria():
    if request.method == "POST":
        checked=[]
        #unchecked=[]
        for historia in historias:
            try:
                # only valid for checked items.
                tit=request.form[historia['titulo']]

            except KeyError:
                pass
                #unchecked.append(historia)
            else:
                # execute if no exception
                checked.append(historia)
            
        prompt, nuevahistoria, usage = openAI_create_story(checked)
        result = {'prompt':prompt, 'historia':nuevahistoria,
                  'autor':"openAI", 'usage':usage}
        result['titulo']=openAI_generar_titulo(result['historia'])
        result['AIinspiration']=[story['titulo'] for story in checked ]
        guardarHistoria(result)
        return render_template("crearhistoria.html", historias=historias, result=result, checked=checked)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    #result = request.args.get("result")
    return render_template("crearhistoria.html", historias=historias)



###################
def generar_prompt_de_historias(historias):
    n=len(historias)+1
    prompt=f"{n} personas escribieron historias."
    for story in historias:
        prompt+= f"\n{story['autor']} escribió: "
        prompt+= story['historia']
    return prompt+"\nEl último escribió:"



def openAI_completion(prompt, length=700, temp=0.8):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temp,
        max_tokens=length,
        presence_penalty=1.2,
        frequency_penalty=0.7,
    )
    return response.choices[0].text, response.usage


def openAI_create_story(historias):
    if len(historias)<2:
        hist=historias+historias0
    prompt=generar_prompt_de_historias(historias)
    story, usage= openAI_completion(prompt)
    return prompt, story, usage 



    
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
*cuento: Domingo al amanecer, surge la duda de siempre.
¿Será que lloverá? Antes de empezar a poner
los ganchos a las prendas, mi madre dice: «Ve
afuera a ver cómo está el cielo». Al rato vuelvo:
«Está haciendo sol». Continúo alistándome
para ir a ciclovía. El día parece estar perfecto,
hace bastante sol y el viento pega tan fuerte que
refresca. Me integro a la ciclovía. Voy avanzando,
la iluminación decae progresivamente, nubes
negras se apoderan del cielo. Aquí estoy, bajo el
puente vehicular de la Boyacá con 68, llamando a
mi madre para que entre la ropa. Título del cuento: Llover o no llover
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
def historiadepalabras():
    if request.method == "POST":
        palabras = request.form["story1"]
        myprompt=generate_prompt(palabras)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=800
        )
        story=response.choices[0].text
        
        result = {'AIinspiration':palabras, 'prompt':myprompt, 'historia': story, 'autor':"openAI", 'usage':response.usage}
        result['titulo']=openAI_generar_titulo(result['historia'])
        guardarHistoria(result)
        return render_template("historiadepalabras.html", result=result)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("historiadepalabras.html", result=result)


#Ejemplo 1: *Palabras principales: delincuencia, leyes, billetes, subsistir, acecho, sirena, salvado, despojado, pertenencias, Bogotá.
#*Historia: La delincuencia Todos los días corro por miedo a que me cojan. Al igual que muchos, lo hago incumpliendo leyes, por conseguir billetes, todo por subsistir. Acecho a las personas de aquí, todos me odian por el trabajo que tengo, no saben lo que siento al cometer este hecho, me atormenta la sirena que a veces me viene persiguiendo. De todas las que me he salvado orando por un santo, el cual me está cobijando y no me ha desamparado. He despojado a muchos de sus pertenencias, las cuales utilizo para llevar de comer a mi familia en mi Bogotá.


def generate_prompt(palabras):
    """Prompt usado en 'historiadepalabras', donde con unas palabras se genera una historia"""
    return """ OpenAI creará historias usando grupos de palabras principales. 
Ejemplo 1: *PALABRAS PRINCIPALES: homosexualidad, rechazo, dolor, muerte.
*historia: Barrio Danubio, día viernes. Termino de retocar mi maquillaje y vestido, doy vuelta frente al espejo... Por primera vez me gusta lo que veo. ¡Soy feliz! Saliendo de mi casa me encuentro al chico que siempre me ha gustado, sin pensarlo dos veces le confieso mi amor; su respuesta hizo que sintiera algo en mi estómago... Pero no son las mariposas soñadas, sino su cuchillo perforándome mientras grita palabras de asco. No entiendo el motivo; después de unos segundos comprendo: es porque soy hombre.
Ejemplo 2: *PALABRAS PRINCIPALES: Alegría, contento, fantasía, diversión, colorido, flores.
*Historia: 28 de junio Vi que llevaba una corona de flores amarillas sobre la cabeza, un vestido fuscia, casi transparente, todo escotado y repleto de arandelas; pestañas azules, labios rojos escarchados, aretes de fantasía en forma de lagartija. Agitaba los hombros al ritmo delirante de los tambores. Se protegía del sol con una sombrilla arcoíris y de las miradas conocidas con una capa de base facial más gruesa que su voz. Me escondí en la pastelería Florida, detrás de una vitrina, y desde ahí me di cuenta de que nunca antes, en mis quince años de vida, había visto tan contento a mi papá. 
Ejemplo 3: *PALABRAS PRINCIPALES: 
"""+palabras+"*Historia:"

    

#########alargarhistoria##############
@app.route("/alargarhistoria", methods=("GET", "POST"))
def alargarhistoria():
    if request.method == "POST":
        titulo=request.form['alargarhistoria']
        for story in historias:
            if story['titulo']==titulo:
                prompt, nuevaparte, usage = openAI_extend_story(story)
                if story['autor'][-6:]=='openAI':
                    newautor=story['autor']
                else:
                    newautor=story['autor']+' + openAI'
                historiaalargada=story['historia']+""" *** """+nuevaparte
                result = {'prompt':prompt,
                          'historia':historiaalargada,
                          'autor':newautor, 'usage':usage}
                result['titulo']=story['titulo']+'+'
                result['AIinspiration'] = "alargar historia" 
                guardarHistoria(result)
                return render_template("alargarhistoria.html", historias=historias, result=result)
            else:
                pass
        note="no se encontró la historia buscada "+titulo
        return render_template("alargarhistoria.html", historias=historias, note=note)
    return render_template("alargarhistoria.html", historias=historias)

def openAI_extend_story(story):
    prompt=generar_prompt_alargar_historia(story)
    newstory, usage= openAI_completion(prompt)
    return prompt, newstory, usage

def generar_prompt_alargar_historia(story):
    prompt= """Extender una historia. Tomar una historia empezada y luego continuarla.
Ejemplo 1. Historia inicial: Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez.
Continuación: Mis sensores comienzan a recibir la luz. Se activan los circuitos y en mi tarjeta gráfica aparece un archivo que interpreto como imágenes del planeta. Gracias a archivos detallados identifico plantas, rios y montañas. Entiendo como moverme y exploro a mi alrededor. Hay arena, pero no es un problema para mis piernas, programadas para caminar como humano. No veo personas ni animales a mi alrededor, pero guardo la esperanza de que la vida en la tierra vuelva a reproducirse y ser como antes.
Ejemplo 2. Historia inicial: No puedo dormir. Todo lo que veo es oscuridad. Me siento solo.
Continuación: Hay miedo y preocupaciones en mi cabeza. Todos los problemas del día vuelven ahora y no me dejan tranquilo. Debo calmarme. Recuerdo que antes intentaba contar los números para dormir. No es fácil pero me ayudan a calmar la mente. Respiro profundo y empiezo a contar. Uno. Dos. Tres. Comienzo a calmarme, pero creo que esto no va a funcionar. Cuatro. Cinco. Prefiero ahora hacer silencio. Sigo respirando. Veo como un sueño se mezcla con mi respiración. Una imagen. Una silueta.
Ejemplo 3. Historia inicial: En un lugar de La Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor.  Era, en fin, una de esas figuras que pasan desapercibidas a no ser por su caballo, el cual era de un tordillo bayo, flaco como su amo, y tan mal corvejón, que aunque anduviese a cuatro patas, no parecía más que un palo arrimado al caballo. 
Continuación: Tenía la crin y la coleta, que eran su principal ornato, tan largas, que aunque el mozo las recogiese todas en una mano, le colgaban por la rodilla. Rocinante, así llamado por su amo, en otro tiempo era llamado el Mazamorrero, y antes el Rucio, nombre que todavía se le daba cariñosamente, porque fuera de él no había caballo que pudiese compararse con él en nada. Era, en efecto, un animal tan miserable, que hasta el mismo don Quijote le tenía lástima. Don Quijote se llamaba el hidalgo, y no era muy rico, pero era muy honrado y tenía una buena posición social. Vivía en una pequeña aldea llamada Tobar, en la provincia de La Mancha, y era muy conocido y respetado por todos los que le rodeaban. Don Quijote tenía una mente muy ingeniosa, pero estaba obsesionado con los caballeros andantes y las historias de caballería.
Historia inicial: """
    ending="""
Continuación:"""
    return prompt+story['historia']+ending




if __name__=='__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
