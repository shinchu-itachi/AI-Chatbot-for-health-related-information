# Flask is a web application framework written in Python, implemented on Werkzeug and Jinja2 template.
# It is a set of functions and predefined classes used to connect with the system software and handle 
# inputs and outputs.

from flask import Flask, render_template, request

# ChatterBot is a library in python which generates responses to user input. It uses a number of 
# machine learning algorithms to produce a variety of responses. It becomes easier for the users 
# to make chatbots using the ChatterBot library with more accurate responses.
from chatterbot import ChatBot


from chatterbot.trainers import ChatterBotCorpusTrainer
import os   

# spaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python.
# spaCy’s CLI provides a range of helpful commands for downloading and training pipelines, 
# converting data and debugging your config, data and installation.
import spacy.cli 
spacy.cli.download("en_core_web_md")

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

app = Flask(__name__)


english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response

if __name__ == "__main__":
    app.run()
