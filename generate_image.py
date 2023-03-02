
#openai api completions.create -m curie:ft-tercer-piso-danza-2022-12-13-20-09-38 -p ""

import os,  requests
import openai
from dotenv import load_dotenv, find_dotenv
from flask import url_for
from werkzeug.utils import secure_filename
import os
#from mynewapp import app

import requests

def generate_image_name(historia):
    # try:
    #     image_link=historia.image_link
    # except:
    image_name=secure_filename(f'{historia.id}_{historia.sesion.user}_{historia.titulo}_000.jpg')
    return image_name

def store_image(image_url,image_name):
    img_data = requests.get(image_url).content
    filename0=f'./static/uploads/cyborg_images/{image_name}'


    filename=f'./cyborgchaman/static/uploads/cyborg_images/{image_name}'
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        with open(filename, 'wb') as handler:
            handler.write(img_data)
    except FileNotFoundError:
        with open(filename0, 'wb') as handler:
            handler.write(img_data)

            
    location=url_for('static', filename=f'uploads/cyborg_images/{image_name}')
    print(location)
    return filename0


load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image_from_prompt(myprompt):
    response = openai.Image.create(
        prompt=myprompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    print(image_url)
    #store_image(image_url, image_location)
    return response, image_url


def generate_image_from_story(historia):
    newprompt=image_prompt_from_story(historia.historia)
    image, temp_url=generate_image_from_prompt(newprompt+", matte painting trending on artstation")
    #image, temp_url=generate_image_from_prompt(historia.historia+", matte painting trending on artstation")
    image_name=generate_image_name(historia)
    location=store_image(temp_url,image_name)
    historia.image_link=location
    print(location)





def image_prompt_from_story(story,  length=700, temp=0.9):
    callprompt=f"""create a nice text prompt for a Dall-E image generation, to depict acuratelly and artisticly the following stories. 
Story: La niña caminaba por la playa, adorando los rayos de luna que bañaban el horizonte mientras se mezclaban con las olas. Oía a lo lejos una canción que atrapó su corazón, y fue empujada hacia delante por sus propias fuerzas desconocidas. De repente, en medio de la niebla vio a un chico hermoso sentado sobre un tocón de árbol; él brillaba como si estuviera hecho de estrellas e irradiaba felicidad y deseo. La miró directamente a los ojos y ella sintió como si su alma hubiera sido liberta para perseguir sus sueñosotenido audacia para volar libremente entre el destino y el amor prohibido.
Prompt: A girl walking on the beach under the full moon finds a boy in the fog sitting on a tree
Story: I was at the grocery store when I saw the most interesting thing: an avocado with a cat inside. I had to buy it, of course, and when I got it home I showed it to my roommates. They were as fascinated as I was, and we all agreed that it was one of the coolest things we'd ever seen.
Prompt:  A grocery store with a surreal article: an avocado with a furry surprise inside
Story: {story}
Prompt:"""
    response = openai.Completion.create(
        #model="curie:ft-tercer-piso-danza-2022-12-13-20-09-38",
        model="text-davinci-003",
        prompt=callprompt,
        temperature=temp,
        max_tokens=length,
        presence_penalty=0.95,
        frequency_penalty=0.9,
    )
    return response.choices[0].text

if __name__=='__main__':
    #historia=finetuning_completion("El cyborg chamán nos cuenta  una historia. Historia:",  length=700, temp=0.9)
    
    #print(historia.choices[0].text)

    story0="Comence a sentirme mejor cuando me llegó el aroma. Cebolla con tomate... Mi esposa estaba preparando un almuerzo delicioso. Todo estaba listo, pero la sorpresa fue el postre. Que maravilla. Chocolate y arequipe, helado y salsa inglesa. Mi cuchara no podía parar, pero el placer se disfruta mas despacio. Baje el ritmo y permití una explosión de sabores en mi boca. Gracias al cielo por permitirnos saborearlo en vida."
    story1="Puse las cartas en la mesa. Apareció el loco, el mundo y el ermitaño. *** Siento como si el mundo estuviera cambiando a mi alrededor. El loco representa la libertad, el ermitaño es la introspección y el mundo es todo lo externo. Siento que debo tomar un camino, pero no sé cuál es el correcto. ¿Será el camino de la libertad o el camino de la introspección? No lo sé, pero siento que debo decidir pronto."
    story="Desde niño, shamán supo que era diferente. Sus ojos eran de un color imposible, y sus manos siempre estaban frías. No le importaba, porque podía ver cosas que otros no podían. Los espíritus le hablaban, y él les hacía caso. Cuando creció, se convirtió en el guía de su tribu. Ayudaba a la gente a comunicarse con los espíritus, y les enseñaba a protegerse de las fuerzas oscuras del mundo. Pero un día, un extraño llegó a la tribu. Traía consigo tecnología mágica, y ofreció al shaman cyborgs para todos los que quisieran tenerlos. El shaman supo inmediatamente que aquello era malo, pero no pudo evitar que muchos de su tribu se sometieran a la operación. Ahora, con sus nuevos poderes, el shaman debe luchar contra las fuerzas del mal para proteger a su tribu… y al mundo entero."
    newprompt=image_prompt_from_story(story)
    
    print(newprompt)

    image, url=generate_image(newprompt+", matte painting trending on artstation")
    print(url)
    print(image)
