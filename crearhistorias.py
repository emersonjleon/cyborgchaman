

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
            
        prompt, nuevahistoria, tokens_usados = openAI_create_story(checked)
        result = {'prompt':prompt, 'historia':nuevahistoria,
                  'autor':"openAI", 'usage':tokens_usados}
        result['titulo']=openAI_generar_titulo(result['historia'])
        result['AIinspiration']=str([story.titulo for story in checked ])
        guardarHistoria(result)
        return render_template("nuevocrearhistorias.html", historias=current_user.sesion_actual().historias, result=result)
    #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    #result = request.args.get("result")
    return render_template("nuevocrearhistorias.html", historias=current_user.sesion_actual().historias)



@app.route("/generarhistoria", methods=("GET", "POST"))
@login_required
def generarhistoria():
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
            
        # prompt, nuevahistoria, tokens_usados = openAI_create_story(checked)
        # result = {'prompt':prompt, 'historia':nuevahistoria,
        #           'autor':"openAI", 'usage':tokens_usados}
        # result['titulo']=openAI_generar_titulo(result['historia'])
        # result['AIinspiration']=str([story.titulo for story in checked ])
        # guardarHistoria(result)
        # return render_template("nuevocrearhistorias.html", historias=current_user.sesion_actual().historias, result=result)
        
        #return redirect(url_for("crearhistoria", result=response.choices[0].text))

    #result = request.args.get("result")
    return render_template("nuevocrearhistorias.html", historias=current_user.sesion_actual().historias)







###################
def generar_prompt_de_historias(historias):
    n=len(historias)+1
    prompt=f"{n} personas escribieron historias."
    for story in historias:
        prompt+= f"\n{story.autor} escribió: "
        prompt+= story.historia
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
        myprompt=generate_prompt(palabras)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=800
        )
        story=response.choices[0].text
        
        result = {'AIinspiration':palabras, 'prompt':myprompt,
                  'historia': story, 'autor':"openAI",
                  'usage':response.usage}
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
                prompt, nuevaparte, usage = openAI_extend_story(story)
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













def openAI_extend_story(story):
    prompt=generar_prompt_alargar_historia(story)
    newstory, usage= openAI_completion(prompt)
    return prompt, newstory, usage

def generar_prompt_alargar_historia(story):
    prompt= """Extender una historia. Tomar una historia empezada y luego continuarla.
Ejemplo 1. Historia inicial: Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez.
Continuación: Mis sensores comienzan a recibir la luz. Se activan los circuitos y en mi tarjeta gráfica aparece un archivo que interpreto como imágenes del planeta. Gracias a archivos detallados identifico plantas, rios y montañas. Entiendo como moverme y exploro a mi alrededor. Hay arena, pero no es un problema para mis piernas, programadas para caminar como humano. No veo personas ni animales a mi alrededor, pero guardo la esperanza de que la vida en la tierra vuelva a reproducirse y ser como antes.
Historia inicial: """
    ending="""
Continuación:"""
    return prompt+story.historia+ending



