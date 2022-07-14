import os

import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = "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"





def generate_prompt(story1, story2):
    return f"Cuatro niños escriben historias. * Niño 1: {story1} .*Niño 2: {story2}. * Niño 3: "


story1="Me levante por la mañana y busque a mi amigo Ramón. Estabamos en le parque. De repente me encontre una rata y me asusto. Ramón la mató pero quedo muy triste, pues antes de morir lo miraba con unos ojos de ternura. la vida es delicada y el dijo que queria ir a otra parte"
story2 = "Un día mi mamá me invito al parque y luego yo la acompañe a visitar a mi abuela. Cuando pasamos frente a la panaderia, le pedi Ella me dijo que no tenía que llorar tanto, y me dió un abrazo. Donde mi abuela nos dieron cafe y tambien galletas. " 


def create_story(prompt,lines=12):
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




