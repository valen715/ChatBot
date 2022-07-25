import tkinter
from tkinter.scrolledtext import ScrolledText
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from flask import Flask, render_template, request
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

bot = ChatBot('Feedbacker')

@app.get('/')
def home():
    return render_template('home.html')

@app.get('/')
def get_random_response():
    text = input()

    if 'si' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Por favor pon "si" o "no"')
        return get_random_response()

while True:
    try:
        texto_usuario = input()
        request = bot.get_response(texto_usuario)

        print(f'¿Es {request} una respuesta coherente a {texto_usuario}')

        if get_random_response() is False:
            print('Por favor pon la respuesta correcta')
            respuesta_correcta = input()
            
            with open('./corpus/feedbacker.yml','a',encoding='utf-8') as f:
                f.write(f'- - {texto_usuario}\n')
                f.write(f'  - {respuesta_correcta}\n')

            trainer = ChatterBotCorpusTrainer(bot)
            trainer.train('./corpus/feedbacker.yml')

            print('Respuesta añadida al bot!')
    except:
        pass

    if __name__ == '__main__':
        app.run()