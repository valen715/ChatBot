import tkinter
from tkinter.scrolledtext import ScrolledText
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from flask import Flask, render_template, request
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

bot = ChatBot('HAL3000',
              logic_adapters=[
                  {
                      'import_path': 'chatterbot.logic.BestMatch',
                      'maximum_similarity_threshold': 0.65,
                      'default_response': 'Perdoname, pero no logro entenderte',
                      'response_selection_method': get_random_response,
                  },
              ],
              preprocessors=[
                  'chatterbot.preprocessors.clean_whitespace'
              ],
              read_only=True
              )

trainer = ChatterBotCorpusTrainer(bot)
# trainer.train('chatterbot.corpus.spanish')
docs = ['feedbacker.yml']

for doc in docs:
    trainer.train(f'./corpus/{doc}')


@app.get('/')
def home():
    return render_template('home.html')

@app.get('/entrenamiento')
def entrenamiento():
    return render_template('entrenamiento.html')

@app.post('/entrenar')
def entrenar():
    pregunta = request.values.get('pregunta')
    respuesta = request.values.get('respuesta')
    with open('./corpus/feedbacker.yml','a',encoding='utf-8') as f:
                f.write(f'- - {pregunta}\n')
                f.write(f'  - {respuesta}\n')
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('./corpus/feedbacker.yml')
    print('Respuesta añadida al bot!')
    return render_template('home.html')

@app.get('/get')
def get_bot_response():
    userText = request.args.get('msg')
    if "modo programador 2007" in userText.lower():
        return "clic en GENERAL hacer clic en opcion HABILITAR PESTAÑA PROGRAMADOR"
    elif "modo programador 2010" in userText.lower():
        return 'clic en "ARCHIVO - OPCIONES" clic "PERSONALIZAR CINTA DE OPCIONES" clic en "PESTAÑAS PRINCIPALES" clic en "PROGRAMADOR" hacer clic en boton "ACEPTAR"'
    elif "modo programador 2013" in userText.lower():
        return 'clic en "ARCHIVO - OPCIONES" clic "PERSONALIZAR CINTA DE OPCIONES" clic en "PESTAÑAS PRINCIPALES" clic en "PROGRAMADOR" hacer clic en boton "ACEPTAR"'
    elif "modo programador 2016" in userText.lower():
        return 'clic en ARCHIVO - OPCIONES clic PERSONALIZAR CINTA DE OPCIONES clic en PESTAÑAS PRINCIPALES clic en PROGRAMADOR hacer clic en boton ACEPTAR"'
    return str(bot.get_response(userText.lower()))


if __name__ == '__main__':
    app.run()
