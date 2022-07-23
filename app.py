import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import datetime, pickle


from cuentos import cuentos#, jsonify
from sesiones import sesiones as sesiones
    

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route('/cuentos')
def loscuentos():
    #return cuentos
    #return str(historias)
    #return str(type(sesiones))
    return sesiones



@app.route("/sesiones", methods=("GET", "POST","DELETE"))
def editar_sesiones():
    #guardar sesion
    if request.method == "POST":
        nuevasesion={}
        nuevasesion['nombre'] = request.form["sesionname"]
        nuevasesion['fecha'] = datetime.date
        nuevasesion['historias']=historias
        sesiones.append(nuevasesion)

        # create json object from dictionary
        #jsonfile = json.dumps(sesiones)
        # open file for writing, "w" 
        #f = open("sesiones.json","w")
        # write json object to file
        #f.write(jsonfile)
        # close file
        #f.close()

        # write the python object (dict) to pickle file
        f = open("sesiones.pkl","wb")
        pickle.dump(sesiones,f)
        f.close()

        return render_template("sesiones.html", historias=historias, sesiones=sesiones)
    if request.method == "DELETE":
        pass
    return render_template("sesiones.html", historias=historias, sesiones=sesiones)

###################
###Generate index page
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

    

@app.route("/index")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    #return str(links)
    return render_template("index.html", links=links)
###########






@app.route('/presentation')
def presentation():
    return render_template("presentation.html", result=None)

########################################

@app.route('/cuentos/<string:cnumber>')
def obtenercuento(cnumber):
    elcuento=cuentos[cnumber]
    text=elcuento["name"]+"\n"
    for line in elcuento["content"]:
        text+=line
    return text




@app.route('/palabrasprincipales/<string:cnumber>')
def palabrasprincipales(cnumber):
    elcuento=cuentos[cnumber]
    text=elcuento["name"]+"\n"
    for line in elcuento["content"]:
        text+=line
    myprompt=f"Determine las palabras principales que describen la tematica del siguiente cuento:{text}. PALABRAS PRINCIPALES:"
    response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=50
        )
    elcuento["palabras principales"]=response.choices[0].text
    return text + "* PALABRAS PRINCIPALES:"+response.choices[0].text





###################################
historias=[]
##mejorar esto con sesiones...............
#[{'autor': 'emersin', 'titulo': 'Locura', 'historia': ' El mundo se deshace ante mis ojos. No hay palabras que puedan describir esta sensación. Veo luces y voy hacia ellas.'}, {'autor': 'mamá', 'titulo': 'Me agarraste dormida', 'historia': ' La puerta me despertó. Dije: voy al baño, y no he entrado. Creo que sigo dormida, pero me quedé contando historias.'}, {'historia': '\n\nA veces me siento como si estuviera en una película. Todo es muy brillante y las luces son muy intensas. Me siento como si estuviera en un sueño. Todo es un poco confuso y no puedo despertar. Me siento atrapada en mi propia mente. La única vez que puedo salir de este sueño es cuando estoy en el baño. Me siento en la bañera y me quedo dormida. Tengo que estar en el baño para que pueda despertar. Me siento como si estuviera en una película de terror. Tengo que estar en el baño para no morir.', 'autor': 'openAI', 'titulo': ' El baño'}]


@app.route('/')
@app.route("/ingresarhistoria", methods=("GET", "POST"))
def ingresarhistoria():
    if request.method == "POST":
        nuevahistoria={}
        nuevahistoria['autor'] = request.form["autor"].capitalize()
        nuevahistoria['titulo'] = request.form["titulo"]
        nuevahistoria['historia'] = request.form["historia"]
        historias.append(nuevahistoria)
        #result = request.args.get("result")
    
        return render_template("leerhistorias.html", leer=nuevahistoria, historias=historias)
    return render_template("ingresarhistoria.html")





@app.route("/leerhistorias", methods=("GET", "POST"))
def leerhistorias():
    return render_template("leerhistorias.html",historias=historias)
    




@app.route("/crearhistoria", methods=("GET", "POST"))
def crearhistoria():
    if request.method == "POST":
        nuevahistoria=openAI_create_story(historias)
        result = {'historia':nuevahistoria, 'autor':"openAI"}
        result['titulo']=openAI_generar_titulo(result['historia'])
        historias.append(result)
        return render_template("crearhistoria.html", historias=historias, result=result)
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
        max_tokens=length
    )
    return response.choices[0].text


def openAI_create_story(historias):
    if len(historias)<3:
        hist=historias+historias0
    prompt=generar_prompt_de_historias(historias)
    return openAI_completion(prompt)



    
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

@app.route("/crearhistoriadepalabras", methods=("GET", "POST"))
def crearhistoriadepalabras():
    if request.method == "POST":
        palabras = request.form["story1"]
        myprompt=generate_prompt(palabras)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=800
        )
        return render_template("crearhistoriadepalabras.html", result=response.choices[0].text)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("crearhistoriadepalabras.html", result=result)



def generate_prompt(palabras):
    """Prompt usado en 'crearhistoriadepalabras', donde con unas palabras se genera una historia"""
    return """ OpenAI creará historias usando grupos de palabras principales. 
Ejemplo 1: *Palabras principales: delincuencia, leyes, billetes, subsistir, acecho, sirena, salvado, despojado, pertenencias, Bogotá.
*Historia: La delincuencia Todos los días corro por miedo a que me cojan. Al igual que muchos, lo hago incumpliendo leyes, por conseguir billetes, todo por subsistir. Acecho a las personas de aquí, todos me odian por el trabajo que tengo, no saben lo que siento al cometer este hecho, me atormenta la sirena que a veces me viene persiguiendo. De todas las que me he salvado orando por un santo, el cual me está cobijando y no me ha desamparado. He despojado a muchos de sus pertenencias, las cuales utilizo para llevar de comer a mi familia en mi Bogotá.


Ejemplo 2: *PALABRAS PRINCIPALES: Alegría, contento, fantasía, diversión, colorido, flores.
*Historia:
28 de junio Vi que llevaba una corona de flores amarillas sobre la cabeza, un vestido fuscia, casi transparente, todo escotado y repleto de arandelas; pestañas azules, labios rojos escarchados, aretes de fantasía en forma de lagartija. Agitaba los hombros al ritmo delirante de los tambores. Se protegía del sol con una sombrilla arcoíris y de las miradas conocidas con una capa de base facial más gruesa que su voz. Me escondí en la pastelería Florida, detrás de una vitrina, y desde ahí me di cuenta de que nunca antes, en mis quince años de vida, había visto tan contento a mi papá. 

Ejemplo 3: *palabras principales: 
"""+palabras+"*Historia:"







#petname##########################

@app.route("/petname", methods=("GET", "POST"))
def petname():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_petname(animal),
            temperature=0.6,
        )
        return render_template("petname.html", result=response.choices[0].text)

    result = request.args.get("result")
    return render_template("petname.html", result=result)


def generate_petname(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

###################################

@app.route('/nuevahistoria/<string:cnumber>')
def nuevahistoria(cnumber):
    elcuento=cuentos[cnumber]
    text=elcuento["name"]+"\n"
    for line in elcuento["content"]:
        text+=line
        palabasprincipales=elcuento['palabras principales']
        myprompt=f"Cree una SEGUNDA historia de 150 palabras que se relacione con las siguientes palabras principales:{palabrasprincipales}.  NUEVA HISTORIA:"
    response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=500
        )
    elcuento["nuevahistoria"]=response.choices[0].text
    return myprompt+elcuento["nuevahistoria"]


####deprecated?
def create_story(prompt,lines=12):
    myprompt=prompt
    story=''
    for i in range(lines):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt+story,
            temperature=0.6,
        )
        newline=response.choices[0].text
        story+=newline
    return story
