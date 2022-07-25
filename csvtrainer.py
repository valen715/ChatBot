from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import csv

bot = ChatBot('CSVTrainer')

with open('ExcelHelp.csv','r') as f:
    reader = csv.reader(f)

    for fila in reader:
        with open('./corpus/csvtrainer.yml','a',encoding='utf-8') as f:
            f.write(f'- - {fila[0]}\n')
            f.write(f'  - {fila[1]}\n')


    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('./corpus/csvtrainer.yml')
    print('Respuesta añadida al bot!')