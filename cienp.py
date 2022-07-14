import os

import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = "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"





def generate_prompt(story1, story2):
    return f"Cinco colombianos escriben historias. * 1: {story1} * 2: {story2} * Niño 3: {story3} *"


story1="Se oyen fuertes disparos en la calle 13 de la capital, cristales caen fuertemente al suelo, gritos suplican sin aliento paz y justicia, llantos con anhelo de esperanza, y yo desde mi cuarto medio aturdida del escándalo solo quiero entender el teorema de Pitágoras."


story2 = "Habíamos vuelto al colegio después de las cuarentenas. En clase de Competencias Ciudadanas la profesora preguntó si alguien sabía qué significaba
el color rojo en la bandera de la ciudad. Después de un momento de silencio, desde el fondo del salón, una voz destemplada respondió: Hambre."

story3 = "Tengo grabada en mi memoria tu radiante sonrisa la primera vez que nos
subimos al TransMiCable, cómo tus dedos señalaban los barrios donde
jugabas de niña, mientras te reías y le hablabas a los otros pasajeros de lo
hermosa que se ve la ciudad desde arriba; eras tan alegre y nostálgica, tu
felicidad siempre fue contagiosa y hasta el hombre callado que iba con
nosotros comenzó a reír. Ahora que te has ido, solo me queda recordarte
en cada calle, avenida y carrera, en cada subida a Monserrate y en cada
caminata por la Séptima. Te amaré siempre, mamá."

def create_story(prompt,lines=15):
    myprompt=prompt
    for i in range(lines):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=myprompt,
            temperature=0.6,
        )
        newline=response.choices[0].text
        print(newline)
        myprompt+=newline

create_story(generate_prompt(story1,story2), 15  )




