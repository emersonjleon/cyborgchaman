import os

import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = os.getenv("OPENAI_API_KEY")#key needed here

def generate_prompt(historias):
    n=len(historias)+1
    prompt=f"{n} personas escribieron historias."
    for story in historias:
        prompt+= f" *{story['autor']} escribió: "
        prompt+= story['historia']
    return prompt+" *el último escribió:"



def openAI_completion(prompt, length=500, temp=0.6):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temp,
        max_tokens=length
    )
    return response.choices[0].text


def create_story(historias):
    if len(historias)==0:
        historias=historias0
    prompt=generate_prompt(historias)
    return openAI_completion(prompt)




    
story1="Me levante por la mañana y busque a mi amigo Ramón. Estabamos en le parque. De repente me encontre una rata y me asusto. Ramón la mató pero quedo muy triste, pues antes de morir lo miraba con unos ojos de ternura. la vida es delicada y el dijo que queria ir a otra parte"
story2 = "Un día mi mamá me invito al parque y luego yo la acompañe a visitar a mi abuela. Cuando pasamos frente a la panaderia, le pedi Ella me dijo que no tenía que llorar tanto, y me dió un abrazo. Donde mi abuela nos dieron cafe y tambien galletas. " 
historias0=[{'autor': 'nn', 'titulo': 'Ramon y la rata', 'historia': story1},{'autor': 'nn', 'titulo': 'Paseito con mamá', 'historia': story2}, {'autor': 'mamá', 'titulo': 'Me agarraste dormida', 'historia': ' La puerta me despertó. Dije: voy al baño, y no he entrado. Creo que sigo dormida, pero me quedé contando historias.'}, {'historia': '\n\nA veces me siento como si estuviera en una película. Todo es muy brillante y las luces son muy intensas. Me siento como si estuviera en un sueño. Todo es un poco confuso y no puedo despertar. Me siento atrapada en mi propia mente. La única vez que puedo salir de este sueño es cuando estoy en el baño. Me siento en la bañera y me quedo dormida. Tengo que estar en el baño para que pueda despertar. Me siento como si estuviera en una película de terror. Tengo que estar en el baño para no morir.', 'autor': 'openAI', 'titulo': ' El baño'}]








if __name__=='__main__':    
    create_story(historias0)




