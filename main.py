from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response, get_random_response

bot = ChatBot('HAL3000',
    logic_adapters=[
        {
            'import_path':'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.65,
            'default_response':'Perdoname, pero no logro entenderte',
            'response_selection_method': get_random_response,
        },
        # 'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter'
    ],
    # response_selection_method=get_random_response,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    read_only=True



)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.spanish')
docs = ['feedbacker.yml']
for doc in docs:
    trainer.train(f'./corpus/{doc}')


while True:
    texto_usuario = input('Tú: ')
    respuesta = bot.get_response(texto_usuario)
    print(f'Bot: {respuesta}')