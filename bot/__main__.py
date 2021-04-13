from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import markovify
import os
import requests
from bs4 import BeautifulSoup
from markov import *
import urllib.parse as urlparse

if(os.getenv('DB_PATH')):
    print("[*] Building models...")
    models = make_models_from_path(os.getenv('DB_PATH'), 'messages', 1, True)
    print(f"[*] Built models {models.keys()}")

#help command
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
    """
    Usage:
    /gen [[model].json | url] (number of max chars)
    Example: /gen gnu.org
    """)

def gen(update: Update, context: CallbackContext):
    """generate chain based on url"""
    if(context.args):
        content = context.args[0]
        length = 240
    if(len(context.args) == 2):
        length = int(context.args[1])

    print(f"[{update.message.from_user.username}] content: {content}, length: {int(length)}")

    if(urlparse.urlparse(content)):
        try:
            output = random_sentence(make_model_from_url(content, 1, False), length)
        except requests.exceptions.MissingSchema:
            output = random_sentence(make_model_from_url("http://" + content, 1, False), length)
        except IndexError:
            output = "Invalid arguments"
        except requests.exceptions.SSLError:
            output = "Bad handshake"
            
    else:
        try:
            output = random_sentence(models[content], length)
        except IndexError:
            output = "Invalid arguments"
    
    update.message.reply_text(output)



updater = Updater(os.getenv('BOT_KEY'))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('gen', gen))
#updater.dispatcher.add_handler(CommandHandler('gen_url', gen_url))
updater.start_polling()
updater.idle()
