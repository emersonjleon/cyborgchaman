import datetime, pickle

def clearsesiones():
    sesiones=[]
    f = open("sesiones0.pkl","wb")
    pickle.dump(sesiones,f)
    f.close()

def loadsesiones():
    pickleobjects = []
    with (open("sesiones.pkl", "rb")) as openfile:
        while True:
            try:
                pickleobjects.append(pickle.load(openfile))
            except EOFError:
                break

    return pickleobjects[-1]

sesiones=loadsesiones()

#print(sesiones.pop(4))

#print(len(pickleobjects)) # 1


for obj in sesiones:
    print('*******************')
    print(obj['nombre'])
    print(obj['fecha'])
    for historia in obj['historias']:
        print("*")
        print(historia['titulo'])
        print(historia['historia'])
        

def savesesiones():        
    f = open("sesiones.pkl","wb")
    pickle.dump(sesiones,f)
    f.close()



# sesiones=[
#     {
#         'nombre':'primera',
#         'fecha':0,
#         'historias':[
#             {'autor': 'eme', 'titulo': 'El algoritmo', 'historia': 'No sabía que hacer. Entonces me quedé quieto. Estaba muy cansado, necesitaba comer algo, pero casi no podía moverme, y mi estomago se sentía indispuesto. Así que me quedé en el suelo, inmovil y cerré los ojos. Tuve una visión. Mi cuerpo no existía, y mi mente era parte de una gran máquina. La mente del mundo operaba como una computadora, y yo era parte del algoritmo. Mis ideas programaban las acciones presentes y futuras. Mis acciones eran consecuencia de los programas que estaban instalados en mi ser. El adn era una forma de lenguaje de programación, el sistema operativo y la información para crear el hardware una y otra vez estaban ahí acumuladas. La evolución era simplemente un proceso de programación y reprogramación de maquinas que se programan a sí mismas. La historia y la cultura nos cargan con programas milenarios transmitidos a travez de el lenguaje. También a través de programas de imitación, empatía e intuición, que vienen en el adn, pero que nos permiten conectividad. Vamos descargando información que nos permite ir mejorando nuestros algoritmos, actualizarnos y resolver cada vez mejor los diferentes retos que plantea la vida. Cada celula del cuerpo actúa siguiendo el algoritmo. Sus comandos operan a niveles muy básicos, pero la complejidad de toda esta creación es infinita. El universo se manifiesta como un gran fractal de increible belleza y simetría. Leyes simples formando patrones avanzados, geometrías mágicas en cada atomo, en cada copo de nieve, en cada galaxia, en cada cerebro. Me sentí agradecido y decidí que no quería morir. En ese momento el amor se acercó a mí y me ofreció alimento. Reuní todas mis fuerzas para incorporarme, y prové el delicioso nectar que me trajo de nuevo al mundo.'},
#             {'autor': 'openAI', 'titulo': 'Amiga', 'historia': 'Estaba sentada en la terraza, mirando las estrellas y pensando en mi amiga. Ella me había pedido perdón y yo le había dicho que sí, pero aún no podía dejar de pensar en todo lo que había pasado. Nos habíamos peleado por un chico, y ella me había dicho algunas cosas muy hurtful. No podía dejar de pensar en lo mucho que la quería y en lo afortunada que era de tenerla en mi vida. De pronto, la puerta se abrió y ella apareció. Nos miramos a los ojos y supimos que todo estaba bien. Nos abrazamos y nos dimos un beso.'},
#             {'historia': 'A veces me siento como si estuviera en una película. Todo es muy brillante y las luces son muy intensas. Me siento como si estuviera en un sueño. Todo es un poco confuso y no puedo despertar. Me siento atrapada en mi propia mente. La única vez que puedo salir de este sueño es cuando estoy en el baño. Me siento en la bañera y me quedo dormida. Tengo que estar en el baño para que pueda despertar. Me siento como si estuviera en una película de terror. Tengo que estar en el baño para no morir.', 'autor': 'openAI', 'titulo': ' El baño'},
#             {'historia': '\n\nEstaba caminando por la calle cuando de pronto me di cuenta de que no estaba solo. Había un hombre a mi lado, caminando silenciosamente. No podía ver su rostro, pero su presencia me resultaba familiar. De pronto, me di cuenta de que era mi yo del futuro. Me miró a los ojos y me dijo: "No te rindas. Sé que puedes hacerlo". Luego, desapareció. Me quedé allí, paralizado, sin saber qué hacer. No podía dejar de pensar en lo que me había dicho. No podía dejar de pensar en mi futuro.', 'autor': 'openAI', 'titulo': ' El hombre del futuro'}, {'historia': ' \n\nEstaba caminando por el bosque cuando oí un ruido. Me di la vuelta y vi a un oso. El oso me miró fijamente y yo me quedé paralizado. No podía moverme. No podía hacer nada. El oso se acercó a mí y me olisqueó. Luego, se alejó. Me quedé allí, sin saber qué hacer. No podía dejar de pensar en el oso. No podía dejar de pensar en lo que había hecho.', 'autor': 'openAI', 'titulo': ' El oso'}, {'historia': '\n\nMe sentía muy cansado. Necesitaba dormir, pero no podía. Todo lo que quería hacer era cerrar los ojos y dejar que el sueño me llevara. Pero no podía. Me sentía como si estuviera en una pesadilla. No podía despertar. Me sentía atrapado en mi propia mente. La única vez que podía salir de este sueño era cuando me ponía a llorar. Lloraba hasta que me quedaba dormido. Lloraba hasta que no podía llorar más.', 'autor': 'openAI', 'titulo': ' La pesadilla'},
#             {'historia': ' \n\nEstaba caminando por el bosque cuando oí un ruido. Me di la vuelta y vi a un oso. El oso me miró fijamente y yo me quedé paralizado. No podía moverme. No podía hacer nada. El oso se acercó a mí y me olisqueó. Luego, se alejó. Me quedé allí, sin saber qué hacer. No podía dejar de pensar en el oso. No podía dejar de pensar en lo que había hecho.', 'autor': 'openAI', 'titulo': ' El oso.'}
#         ]
#     },
#     {
#         'nombre':'otra',
#         'fecha':22,
#         'historias':[
#             {'titulo':"El libro mágico",
#                            'historia':"Había una vez una niña llamada Lila. Era muy inteligente y le gustaba leer libros. Un día, ella encontró un libro mágico. El libro le dijo que ella podía ser cualquier persona que ella quería ser. Lila pensó que era genial. Ella podría ser una princesa, una hada o incluso una reina. Lila empezó a leer el libro y se convirtió en una hada. Entonces, ella voló a un mundo mágico donde conoció a un dragón. El dragón le dijo que ella podía ser cualquier cosa que ella quería ser. Lila pensó que era genial. Ella podría ser una princesa, una hada o incluso una reina. Lila voló de vuelta a su casa y se convirtió en una princesa.", 'autor':"openAI"
#             }
#         ]
#     },
#     {
#         'nombre':'nueva',
#         'fecha':2207,
#         'historias':[
#             {
#                 'autor': 'emersin',
#                 'titulo': 'prueba',
#                 'historia': ' Esta historia es de prueba. Queremos ver que pasa cuando se escribe algo aquí. para empezar está bien. Pero aquel que no sabe lo que quiere comenzará a decir cosas sin sentido en cualquier momento. Estás tranquilo. Escribes con fluidez, y eso te permite llenar este espacio.'
#             },
#             {
#                 'historia': ' Tengo una historia. Es una historia triste, pero es la mía y la amo. Tengo una familia y una casa. Y una vida. Y todo lo que quiero hacer es vivirla. Pero no puedo. No puedo vivir mi vida. No puedo ser feliz. No puedo ser yo mismo. No puedo ser nada. Nada. Nada. Nada.',
#                 'autor': 'openAI',
#                 'titulo': ' Nada'
#             }, {
#                 'historia': ' una noche, un niño llamado Pablo, soñaba que volaba. Soñaba que era libre. Soñaba que podía ser feliz. Y entonces, de repente, se despertó.',
#                 'autor': 'openAI',
#                 'titulo': ' El sueño de Pablo'
#             },
#             {
#                 'historia': ' Era una noche oscura y tormentosa. Pablo estaba en su cama, temblando de miedo. Oyó un ruido fuera de su ventana y, al asomarse, vio una figura oscura que se movía entre los árboles. Se tapó la boca para no gritar, pero era demasiado tarde. La figura oscura estaba dentro de su habitación. Pablo no podía hacer nada, sólo mirar fijamente mientras la figura se acercaba a él lentamente. *openAI escribió: Al ver que Pablo no podía hacer nada, la figura oscura se acercó a él y le dijo: "No tengas miedo, Pablo. Soy yo, tu amigo". Pablo reconoció la voz de la figura oscura y se dio cuenta de que no era un monstruo, sino su amigo. Entonces, Pablo sonrió y dijo: "¡Hola, amigo! Me alegro de verte".',
#                 'autor': 'openAI',
#                 'titulo': ' La noche oscura'
#             },
#             {
#                 'historia': ' \n\nTodo el mundo tiene miedo de algo. Pablo tiene miedo de la oscuridad, pero un día se da cuenta de que la oscuridad no es nada para temer.', 'autor': 'openAI', 'titulo': ' El miedo a la oscuridad'}, {'historia': ' La última vez que vi a mi padre, me dijo que tenía que irse. Me dijo que no podía quedarse. Me dijo que me quería, pero que tenía que irse. Me dijo que tal vez un día volvería, pero no lo creí. *el último escribió: Ahora, mi padre ha muerto. Nunca volvió. Nunca me dijo adiós. Nunca me dijo que me quería. Nunca me dijo nada. Nunca volví a verlo.', 'autor': 'openAI', 'titulo': ' El último adiós.'}]
#      }
# ]

if False:
    """
La ciudad sucia

Llegué a la ciudad y me di cuenta de que no era lo que esperaba. Era una ciudad sucia y peligrosa. No quería quedarme, pero no tenía otra opción. Me instalé en una pensión y traté de encontrar trabajo. Fue difícil, pero finalmente encontré un trabajo en una tienda de comestibles. Era un trabajo duro, pero me permitió sobrevivir.

openAI

La ciudad extraña

Después de instalarme en la pensión, traté de familiarizarme con la ciudad. Era un lugar extraño, y no estaba seguro de si me gustaba o no. Pasé los días explorando, tratando de encontrar algo que me gustara. Pero no parecía haber nada. La gente era desagradable y el lugar era sucio. No quería quedarme, pero no tenía otra opción.

openAI

Saliendo de la ciudad

Eventualmente me cansé de tratar de encontrar algo que me gustara en la ciudad y decidí irme. No quería quedarme en un lugar donde no me sentía seguro o feliz. Así que empacé mis cosas y me fui. No sé qué va a pasar en el futuro, pero espero que sea mejor que esto.

openAI

Sin rumbo

Siento que no pertenezco a este mundo. No sé qué hacer ni a dónde ir. Me siento solo y perdido. No sé qué va a pasar en el futuro, pero espero que sea mejor que esto.

openAI"""
