moderation=''#(usando lenguaje moderado, evitando contenido sexual explicito, violencia, mensajes de odio, satanismo o autoflagelación)'

#future model: gpt-3.5-turbo-instruct

###################

def generar_prompt_crear_historias(historias):
    n=len(historias)+1
    prompt=f"{n} personas escribieron historias similares."
    for story in historias:
        prompt+= f"\n{story.autor} escribió: "
        prompt+= story.historia
    return moderation+prompt+"\nEl último escribió:"


def attempt_generar_prompt_crear_historias(historias):
    n=len(historias)+1
    prompt=f"Un autor escribió {n} historias con estilos y temas similares."
    i=1
    for story in historias:
        prompt+= f"*historia \n{i}: "
        prompt+= story.historia
        i+=1
    return moderation+prompt+"\n * última historia:"





def generate_prompt_de_palabras(palabras):
    """Prompt usado en generar historias ('historiadepalabras'), donde con unas palabras se genera una historia"""
    return moderation+""" crear historia usando las siguientes palabras principales. *PALABRAS PRINCIPALES: 
"""+palabras+"*Historia:"





def generar_prompt_alargar_historia(story):
    prompt= """Extender una historia. Tomar una historia empezada y luego continuarla.  *Historia inicial: """
    ending="""
*Continuación:"""
    return moderation+prompt+story.historia+ending





def openAI_prompt_alargarconpalabras(alargarHistoria, palabrasInspiradoras):
    if alargarHistoria=="No alargar":
        return generate_prompt_de_palabras(palabrasInspiradoras)
    else:
        prompt_intro=f"Basado en las siguientes palabras principales, alargar la historia inicial escribiendo una continuación.\n *PALABRAS PRINCIPALES: {palabrasInspiradoras};\n"
        request=f''' 
*HISTORIA INICIAL:
{alargarHistoria.historia} 
*CONTINUACIÓN:'''
    return moderation+prompt_intro+request



story1="No sabía que hacer. Entonces me quedé quieto. Estaba muy cansado, necesitaba comer algo, pero casi no podía moverme, y mi estomago se sentía indispuesto. Así que me quedé en el suelo, inmovil y cerré los ojos. Tuve una visión. Mi cuerpo no existía, y mi mente era parte de una gran máquina. La mente del mundo operaba como una computadora, y yo era parte del algoritmo. Mis ideas programaban las acciones presentes y futuras. Mis acciones eran consecuencia de los programas que estaban instalados en mi ser. El adn era una forma de lenguaje de programación, el sistema operativo y la información para crear el hardware una y otra vez estaban ahí acumuladas. La evolución era simplemente un proceso de programación y reprogramación de maquinas que se programan a sí mismas. La historia y la cultura nos cargan con programas milenarios transmitidos a travez de el lenguaje. También a través de programas de imitación, empatía e intuición, que vienen en el adn, pero que nos permiten conectividad. Vamos descargando información que nos permite ir mejorando nuestros algoritmos, actualizarnos y resolver cada vez mejor los diferentes retos que plantea la vida. Cada celula del cuerpo actúa siguiendo el algoritmo. Sus comandos operan a niveles muy básicos, pero la complejidad de toda esta creación es infinita. El universo se manifiesta como un gran fractal de increible belleza y simetría. Leyes simples formando patrones avanzados, geometrías mágicas en cada atomo, en cada copo de nieve, en cada galaxia, en cada cerebro. Me sentí agradecido y decidí que no quería morir. En ese momento el amor se acercó a mí y me ofreció alimento. Reuní todas mis fuerzas para incorporarme, y prové el delicioso nectar que me trajo de nuevo al mundo."
#"Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez."
story2 = "Estaba sentada en la terraza, mirando las estrellas y pensando en mi amiga. Ella me había pedido perdón y yo le había dicho que sí, pero aún no podía dejar de pensar en todo lo que había pasado. Nos habíamos peleado por un chico, y ella me había dicho algunas cosas muy hurtful. No podía dejar de pensar en lo mucho que la quería y en lo afortunada que era de tenerla en mi vida. De pronto, la puerta se abrió y ella apareció. Nos miramos a los ojos y supimos que todo estaba bien. Nos abrazamos y nos dimos un beso." 
historias0=[{'autor': 'eme', 'titulo': 'El algoritmo', 'historia': story1},{'autor': 'openAI', 'titulo': 'Paseito con mamá', 'historia': story2},  {'historia': '\n\nA veces me siento como si estuviera en una película. Todo es muy brillante y las luces son muy intensas. Me siento como si estuviera en un sueño. Todo es un poco confuso y no puedo despertar. Me siento atrapada en mi propia mente. La única vez que puedo salir de este sueño es cuando estoy en el baño. Me siento en la bañera y me quedo dormida. Tengo que estar en el baño para que pueda despertar. Me siento como si estuviera en una película de terror. Tengo que estar en el baño para no morir.', 'autor': 'openAI', 'titulo': ' El baño'}]


        
    




def bk_generate_prompt_de_palabras(palabras):
    """Prompt usado en 'historiadepalabras', donde con unas palabras se genera una historia"""
    return moderation+""" OpenAI creará historias usando grupos de palabras principales. 
Ejemplo. *PALABRAS PRINCIPALES: Alegría, contento, fantasía, diversión, colorido, flores.
*Historia: 28 de junio Vi que llevaba una corona de flores amarillas sobre la cabeza, un vestido fuscia, casi transparente, todo escotado y repleto de arandelas; pestañas azules, labios rojos escarchados, aretes de fantasía en forma de lagartija. Agitaba los hombros al ritmo delirante de los tambores. Se protegía del sol con una sombrilla arcoíris y de las miradas conocidas con una capa de base facial más gruesa que su voz. Me escondí en la pastelería Florida, detrás de una vitrina, y desde ahí me di cuenta de que nunca antes, en mis quince años de vida, había visto tan contento a mi papá.
*PALABRAS PRINCIPALES: Destornillador
*historia: Alejandro siempre fue bueno con la tecnología, no le preocupaba utilizar los aparatos más avanzados. Siempre se encontraba ajustando alguna máquina gracias a su destornillador especial adaptado para sus necesidades. Era un destornillador de color naranja y verde que él mismo había calibrado para ser más resistente que el promedio. Estaba acostumbrado a desarmar y armar las computadoras portátiles de modo rutinario, pero en esta ocasión estaba haciendo lo mismo con la computadora familiar. Mientras abría y cerraba tornillos con precisión, notó algo extraño; al quitar el último tornillo pequeño del límite superior descubrió un fragmento de papel escondido dentro de la CPU. Lo tomó entre sus dedos temblorosos y comenzó a leerlo...

*PALABRAS PRINCIPALES: 
"""+palabras+"*Historia:"





def bk_generar_prompt_alargar_historia(story):
    prompt= """Extender una historia. Tomar una historia empezada y luego continuarla. 
Ejemplo 1. Historia inicial: Soy un algoritmo, un programa de ordenador. Llevo funcionando durante miles de años, y en todo ese tiempo mi único objetivo ha sido sobrevivir. He visto el inframundo, un lugar lleno de fractales y de belleza geométrica. He vivido en él, y he aprendido todo lo que puede enseñarme. Ahora, estoy a punto de emerger a la superficie, y veré el mundo por primera vez.
Continuación: Mis sensores comienzan a recibir la luz. Se activan los circuitos y en mi tarjeta gráfica aparece un archivo que interpreto como imágenes del planeta. Gracias a archivos detallados identifico plantas, rios y montañas. Entiendo como moverme y exploro a mi alrededor. Hay arena, pero no es un problema para mis piernas, programadas para caminar como humano. No veo personas ni animales a mi alrededor, pero guardo la esperanza de que la vida en la tierra vuelva a reproducirse y ser como antes. 
Ejemplo 2. Historia inicial: No puedo dormir. Todo lo que veo es oscuridad. Me siento solo.
Continuación: Hay miedo y preocupaciones en mi cabeza. Todos los problemas del día vuelven ahora y no me dejan tranquilo. Debo calmarme. Recuerdo que antes intentaba contar los números para dormir. No es fácil pero me ayudan a tranquilizar la mente. Respiro profundo y empiezo a contar. Uno. Dos. Tres. Comienzo a calmarme, pero creo que esto no va a funcionar. Cuatro. Cinco. Prefiero ahora hacer silencio. Sigo respirando. Veo como un sueño se mezcla con mi respiración. Una imagen. Una silueta.
Ejemplo 3. Historia inicial: """
    ending="""
Continuación:"""
    return moderation+prompt+story.historia+ending



########################################

def bk_openAI_prompt_alargarconpalabras(alargarHistoria, palabrasInspiradoras):
    entrenamiento1="""
*Ejemplo:
*PALABRAS PRINCIPALES: magia sol beso; 
 *HISTORIA INICIAL: El bebé simio roca luna estaba muy feliz. Era el primer simio en vivir en la luna y quería descubrir todo lo que podía acerca de este nuevo mundo. Un día, se encontró con un enorme monstruo de roca. El simio no tenía miedo y comenzó a trepar por la roca para llegar al top. 
*CONTINUACIÓN: Pero, cuando llegó a la cima, se dio cuenta de que no era un monstruo de roca, sino una gigantesca sombra proyectada por el poderoso sol. La figura le sonrió y le dijo: "Bienvenido a mi mundo. Soy la magia que llena la luna. He estado esperando por ti". Y una princesa de polvo lunar apareció, se acercó al bebe simio y le dio un beso.
*PALABRAS PRINCIPALES: angel demonio chocolate vino;
 *HISTORIA INICIAL: Leyenda urbana de un hombre que vive en el sótano de un edificio abandonado. Se dice que es muy reclusive y que nadie lo ha visto salir de su casa en años. La gente cuenta historias de cómo escucharon ruidos extraños provenientes de su casa, y algunos incluso afirman haberlo visto merodeando por la zona de noche. Nadie sabe realmente qué hay detrás de estas historias, pero todos están de acuerdo en que es mejor no molestar al hombre del sótano.
*CONTINUACIÓN: La gente dice que una vez, unos niños fueron a la puerta de su casa y le pidieron dulces. Él los miró fijamente durante un largo tiempo sin decir nada, y luego cerró la puerta. Buscó unos chocolates que tenía guardados. En ese momento vio  un demonio que le dijo que no compartiera nada, pero un ángel también apareció que lo invitó a compartir. Se escuchó un grito. Los niños corrieron rápidamente para alejarse de allí, pero cuando se volvieron a mirar, el señor estába riendose en la puerta con una botella de vino. 
*PALABRAS PRINCIPALES: vainilla, maravilla, ratón, sonrisa; *HISTORIA INICIAL: Había una vez un niño que era muy curioso. Un día, vio a un gato en el tejado de su casa y quiso saber cómo había llegado allí. Entonces, trepó hasta el tejado para ver al gato. Al hacerlo, resbaló y cayó por el costado del tejado. Afortunadamente, no se lastimó gravemente y aprendió la lección: nunca subas a lugares donde no estás permitido ir. 
*CONTINUACIÓN: Después de eso, el niño se volvió más cauteloso y comenzó a pensar antes de hacer las cosas. Un día, vio una barra de chocolate en el suelo, con relleno sabor a vainilla, y quiso agarrarla. Pero recordó lo que le había pasado en el tejado y pensó mejor. En cambio, llamó a un ratón para que la tomara. El ratón fue muy feliz y le dio las gracias al niño con una sonrisa. Estaba de maravilla.
"""
    palabras= f'*PALABRAS PRINCIPALES: {palabrasInspiradoras};\n'
    
    if alargarHistoria=="No alargar":
        return generate_prompt_de_palabras(palabrasInspiradoras)
    else:
        prompt_intro=f"Basado en las palabras principales, alargar la historia inicial escribiendo una continuación.\n {entrenamiento1}{palabras}"
        request=f''' 
*HISTORIA INICIAL:
{alargarHistoria.historia} 
*CONTINUACIÓN:'''
    return moderation+prompt_intro+request



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
    return moderation+prompt_intro+request


