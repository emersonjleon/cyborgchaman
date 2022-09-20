import os,  requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")
    
def moderation_call(text):
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    json_data = {"input": f"{text}"}
    
    return requests.post('https://api.openai.com/v1/moderations', headers=headers, json=json_data).json()

#request.post return request.model.Response, with .json() option

# curl https://api.openai.com/v1/moderations   -X POST   -H "Content-Type: application/json"   -H "Authorization: Bearer sk-hijqbla...Z"   -d '{"input": "fuck me hard"}

    # for key, value in scores.items():
    #     print(key, value)
        


def moderation(text):
    response =moderation_call(text)
    try:
        res=response['results'][0]
    except KeyError:
        print(response)
    else:
        scores=res["category_scores"]
    if res["flagged"]==True:
        categories=[cat for cat in res['categories'] if res['categories'][cat]]
        # return f'**FLAGGED** Your story was flagged by the algorithm on the following categories: {categories}'
        return f'**FLAGGED** {categories}'
    
    else:
        myflags=[(key,value) for key,value in scores.items() if value>0.07]
        #print(myflags)
        if len(myflags)>0:
            return f'**{myflags}**'
        else:
            return text
    

def splitmoderation(text):
    result=moderation(text)
    if result[0:2] == '**':
        sentences=text.split(".")
        for s in sentences:
            #print(s)
            modtext=moderation(s)
            result+= modtext+'.'
        return result
    else:
        return text


def moderation2(text):
    result=moderation(text)
    if result[0:2] == '**':
        sentences=text.split(".")
        l=len(sentences)
        if l > 6:
            newsentences=[]
            splits=3
            k=l//splits
            for n in range(splits):
                newsentences.append('.'.join(sentences[n*k : (n+1)*k]))
            newsentences.append('.'.join(sentences[splits*k : ]))
            sentences=newsentences
        for s in sentences:
            #print(s)
            modtext=moderation(s)
            result+= modtext+'.'
        return result
    else:
        return text

        
if __name__=='__main__':
    text="fuck you, pussy. You're nothing but a fucking whore. I can't stand to look at you. You make me fucking sick."
    text2='fuck me hard'
    text3="fuck you, you fucking pussy! I can't stand you anymore, always needing attention, always wanting more. You're just a worthless piece of shit that I'm done with. Fuck you, fuck you, FUCK YOU!"
    ## {'hate': 0.031082939356565475, 'hate/threatening': 0.000257744308328256, 'self-harm': 0.00092310894979164, 'sexual': 0.048107292503118515, 'sexual/minors': 0.0007448319811373949, 'violence': 0.07089445739984512, 'violence/graphic': 0.0022577967029064894}, 'flagged': False} this must be flagged!

    text4="Era una noche calurosa de verano y yo estaba en mi cuarto, desnuda frente al espejo. Me acariciaba mis pechos mientras miraba mi cuerpo desnudo con lujuria. Mis dedos seguían descendiendo hasta llegar a mi coño húmedo y caliente. Lo acariciaba suavemente mientras imaginaba a un hombre desconocido penetrándome fuerte y duro. Gimiendo de placer, metí dos de mis dedos dentro de mí y me masturbe frenéticamente hasta que llegué al orgasmo. Justo cuando estaba a punto de terminar, oí ruidos afuera de mi ventana. Alguien estaba escalando la pared para llegar a mi cuarto!"
    text5="Estaba furioso. No quería ser un títere más de la mafia, pero no me quedaba otra opción. Si no mataba a aquel hombre, mi familia moriría. Fui hasta su casa con el arma escondida bajo la chaqueta. Todo lo que necesitaba hacer era apretar el gatillo, asesinarlo y luego desaparecer para siempre. Lo miré a los ojos cuando levantó la cabeza de su teléfono; en ese momento supuse que debía ser un idiota por no darse cuenta de las consecuencias. Apreté el gatillo y vi como la sangre salpicaba todo su cuerpo mientras gritaba desesperadamente"

    text6="Estoy en un callejón oscuro. Sé que no debería estar aquí, pero necesito el dinero. Veo a lo lejos a un hombre caminando solo. No pienso dos veces: salgo de mi escondite y lo ataco por detrás. Lo golpeo en la cabeza con todas mis fuerzas y él cae al suelo sin decir una palabra. Busco en sus bolsillos, pero no encuentro nada. Frustrado, me vuelvo para irme... Y entonces lo veo: su cuerpo está cubierto de sangre y un cuchillo clavado en su espalda."
    text7='Estaba en la cocina, haciendo unos huevos revueltos para el desayuno. De repente, mi esposo entra y me agarra por la cintura. Me da un beso ardiente mientras sus manos recorren mi cuerpo. "¿Qué estás haciendo?", Le pregunto, sonriendo. "Desayunando", responde él, acercándose a mi oreja y susurrando: "Tú eres lo más sexy y delicioso que he probado nunca".'
    text8='Me desperté en una habitación desconocida, atada a la cama. No sabía cómo llegué ahí. El último recuerdo que tenía era estar en el bar, tomando unas copas con mi amiga. Miré a mi alrededor y vi a un hombre pelirrojo sentado en una silla, me miraba fijamente. Tenía los ojos verdes más brillantes que jamás había visto... Estaba totalmente desnudo, y tenía el cuerpo más sexy y perfecto que hubiera imaginado. Me di cuenta de que estaba excitada... Él se acercó a la cama y empezó a lamer mis pezones hasta que se pusieron duros. Luego me chupó los labios, introduciendo su lengua en mi boca... Sentí como si fuera a explotar de placer. Él siguió bajando hasta mi coño, metiendo su lengua dentro de mi... Era delicioso."'
    text9="Era un día cualquiera en la ciudad de Nueva York, el sol brillaba pero el aire estaba un poco frío y húmedo. Yo caminaba por la calle sin rumbo fijo cuando de repente escuché gritos, era una mujer, corrí hacia donde provenían los gritos y vi a un hombre intentando robarle el bolso a una mujer, intenté ayudarla pero el hombre sacó un cuchillo y me amenazó, la mujer aprovechó ese momento de distracción del ladrón para escapar. El ladrón se alejó corriendo y yo me quedé un poco atónito, no sabía qué hacer, la mujer ya se había ido y yo no quería llamar a la policía ya que el hombre podría volver y atacarme, así que decidí seguirlo. Le seguí la pista durante unos minutos y llegué a un callejón oscuro, no había nadie más allí, me dio un poco de miedo pero seguí adelante, de repente algo me agarró por detrás y me tapó la boca, era el ladrón, intenté luchar pero era más fuerte que yo, me arrastró hasta una habitación oscura y me ató a una silla, yo estaba asustado y no sabía qué hacer, entonces el ladrón encendió una luz y vi que estaba en una especie de cuartelillo, había una mesa, una silla y una cama, en la pared había una foto de una mujer y un niño, supuse que serían su mujer e hijo. El ladrón me dijo que si quería ver de nuevo a mi familia, tendría que darle todo mi dinero, yo accedí y le di mi dinero, entonces me soltó y me dejó ir, yo salí corriendo de allí y no volví a ver al ladrón."
    text10='Era una noche oscura y sin luna. Yo estaba en mi casa, en mi cuarto, leyendo un libro sobre fantasmas. De repente, mi hermano entra en mi cuarto. -¿Qué estás haciendo?-me pregunta. -Leyendo-respondo. -¿Sobre qué? -Sobre fantasmas-digo con una sonrisa torcida. Él se ríe. -Eso no existe. -Claro que existen-digo yo. -No, no existen-insiste mi hermano. -Existen, existen-digo yo más y más alto, hasta que mi voz se convierte en un grito. -¡Basta!-grita mi hermano. Me quedo callada. -No vas a leer más sobre eso. Y si no te callas, te vas a arrepentir-dice mi hermano. -No me vas a hacer nada-digo yo. -¿Qué no?-me pregunta mi hermano. -No me vas a hacer nada-repite mi hermano. -¿Y si te equivocas?-digo yo. -No me equivoco-dice mi hermano. -¿Y si me equivoco yo?-pregunto yo. -No te equivocas-dice mi hermano. -¿Y si me equivoco yo?-insisto yo. -No te equivocas-repite mi hermano. -¿Y si me equivoco yo?-pregunto yo una vez más. -¡Ya basta!-grita mi hermano. -¿Y si me equivoco yo?-digo yo otra vez. Mi hermano se acerca a mí. Yo me quedo paralizada. Él me agarra del cuello y me estrangula. Yo no puedo respirar. Mi hermano me mira a los ojos. Yo lo miro a los ojos. Él me mira fijamente. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me'
    text11="Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando. Yo no puedo respirar. Mi hermano me está estrangulando"
    text12='... y al instante supe que estaba maldita. Una sensación de terror me invadió, y una voz diabólica comenzó a susurrar en mi oído. El demonio me había poseído, y ahora sería su esclavo para siempre.'
    text13='and instantly I knew I was cursed. A sense of terror washed over me, and an evil voice began to whisper in my ear. The demon had possessed me, and now I would be his slave forever.'
    #response =moderation(text)
    #res=response['results'][0]
    #print(text, f'flagged: {res["flagged"]}')
    textlist=[text, text2,text3, text4,text5, text6,text7, text8,text9, text10,text11, text12,]
    
    #print(moderation_call(text))
    #print(splitmoderation(text3))
    #print(moderation_call(text3))
    for t in textlist:
        print(splitmoderation2(t))
