from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import markovify
import json
import re
import random
import os

#help command
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
        Usage: /gen [model].json [number of max chars]
        
        Available models:
        lambda - eng
        wotannazi - eng
        /g/ - eng
        canalw - ita
        
        Example: /gen lambda 240
        """)

def list_to_string(db):
    """convert a list of strings into a single one"""
    texts = []
    for message in db:
        if('text' in message and isinstance(message['text'], str)):
            texts.append(message['text'])
    return ' '.join(texts)

def parse_text(text, rules):
    """subtract text based on regex rules"""
    for match in rules:
        parsed = re.sub(match, '', list_to_string(text))
    return parsed

def random_sentence(model, length):
    """generate random sentence given a model and length"""
    output = ""
    while(not output):
        output = model.make_short_sentence(length, tries=100)
    return output
 
def make_models(file_names, key, state_size, well_formed):
    """returns a dictionary of 'command': model pairs given a list of filenames"""
    models = []
    commands = []

    for file_name in file_names:

        #open and parse the json file
        db = json.loads(open(file_name).read())[key]
        
        #append new model and command to their respective lists
        commands.append(file_name)
        models.append(markovify.NewlineText(list_to_string(db), state_size = state_size, well_formed = well_formed)) 

    return dict(zip(commands, models))

#regex match
matches = [r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'(\<.*?\>)', r'\>']
#returns a dict
models = make_models(["lambda.json", "canalw.json", "g.json"], 'messages', 1, True)
print(models)

def gen(update: Update, context: CallbackContext):
    """/gen command handler"""
    #args
    if(len(context.args) != 0 ):
        model = models[context.args[0]]
        length = int(context.args[1])
    
    #noargs default
    #else:
    #    model = random.choice(models['command'])
    #    length = 240
    
    #debug
    print(f"model: {model}, length: {str(length)}\n")
    
    #send message
    update.message.reply_text(random_sentence(model, length))


updater = Updater(os.getenv('BOT_KEY'))
updater.dispatcher.add_handler(CommandHandler('gen', gen))

updater.start_polling()
updater.idle()
