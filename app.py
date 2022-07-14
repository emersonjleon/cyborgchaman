import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from cuentos import cuentos#, jsonify


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/cuentos')
def loscuentos():
    return cuentos

@app.route('/cuentos/<string:cnumber>')
def obtenercuento(cnumber):
    elcuento=cuentos[cnumber]
    text=elcuento["name"]+"\n"
    for line in elcuento["content"]:
        text+=line
    return text


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



@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        palabras = request.form["story1"]
        myprompt=generate_prompt(palabras)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
            max_tokens=800
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(palabras):
    return """ OpenAI creará historias usando grupos de palabras principales. 
Ejemplo 1: *Palabras principales: delincuencia, leyes, billetes, subsistir, acecho, sirena, salvado, despojado, pertenencias, Bogotá.
*Historia: La delincuencia Todos los días corro por miedo a que me cojan. Al igual que muchos, lo hago incumpliendo leyes, por conseguir billetes, todo por subsistir. Acecho a las personas de aquí, todos me odian por el trabajo que tengo, no saben lo que siento al cometer este hecho, me atormenta la sirena que a veces me viene persiguiendo. De todas las que me he salvado orando por un santo, el cual me está cobijando y no me ha desamparado. He despojado a muchos de sus pertenencias, las cuales utilizo para llevar de comer a mi familia en mi Bogotá.


Ejemplo 2: *PALABRAS PRINCIPALES: Alegría, contento, fantasía, diversión, colorido, flores.
*Historia:
28 de junio Vi que llevaba una corona de flores amarillas sobre la cabeza, un vestido fuscia, casi transparente, todo escotado y repleto de arandelas; pestañas azules, labios rojos escarchados, aretes de fantasía en forma de lagartija. Agitaba los hombros al ritmo delirante de los tambores. Se protegía del sol con una sombrilla arcoíris y de las miradas conocidas con una capa de base facial más gruesa que su voz. Me escondí en la pastelería Florida, detrás de una vitrina, y desde ahí me di cuenta de que nunca antes, en mis quince años de vida, había visto tan contento a mi papá. 

Ejemplo 3: *palabras principales: 
"""+palabras+"*Historia:"

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
