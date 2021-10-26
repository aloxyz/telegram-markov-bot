import os
import requests
import urllib.parse as urlparse
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import markov


_MODELS = None


def help(update: Update, context: CallbackContext):
    """ Help command """
    update.message.reply_text(
        """
    Usage:
    /gen [[model].json | url] (number of max chars)
    Example: /gen gnu.org
    """
    )


def gen(update: Update, context: CallbackContext):
    """generate chain based on url"""
    if context.args:
        content = context.args[0]
        length = 240
    if len(context.args) == 2:
        length = int(context.args[1])

    print(
        f"[{update.message.from_user.username}] content: {content}, length: {int(length)}"
    )

    if urlparse.urlparse(content):
        try:
            output = markov.random_sentence(
                markov.make_model_from_url(content, 1, False), length
            )
        except requests.exceptions.MissingSchema:
            output = markov.random_sentence(
                markov.make_model_from_url("http://" + content, 1, False), length
            )
        except IndexError:
            output = "Invalid arguments"
        except requests.exceptions.SSLError:
            output = "Bad handshake"

    else:
        try:
            output = markov.random_sentence(_MODELS[content], length)
        except IndexError:
            output = "Invalid arguments"

    update.message.reply_text(output)


def main():
    if db_path := os.getenv("DB_PATH"):
        print("[*] Building models...")
        global _MODELS
        _MODELS = markov.make_models_from_path(db_path, "messages", 1, True)
        print(f"[*] Built models {_MODELS.keys()}")

    updater = Updater(os.getenv("BOT_KEY"))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("gen", gen))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
