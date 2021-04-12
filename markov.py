import markovify
import json
import re
import random
import os
import requests
from bs4 import BeautifulSoup


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
        output = model.make_short_sentence(int(length), tries=100)
    return output
 
def make_models_from_path(path, key, state_size, well_formed):
    """returns a dictionary of 'command': model pairs given a list of filenames"""
    models = []
    commands = []
    file_names = os.listdir(path)

    for file_name in file_names:

        try:
            #open and parse the json file
            db = json.loads(open(path + '/' + file_name).read())[key]
        except KeyError:
            print("Could not build some files, skipping...")
        
        #append new model and command to their respective lists
        commands.append(file_name)
        models.append(markovify.NewlineText(list_to_string(db), state_size = state_size, well_formed = well_formed)) 

    return dict(zip(commands, models))

def make_model_from_url(url, state_size, well_formed):
    """generate model from web page content"""
    content = requests.get(url).content

    if(bool(BeautifulSoup(content, "html.parser").find())):
        text_content = BeautifulSoup(content, features="lxml").text
    else:
        text_content = content

    return markovify.NewlineText(text_content, state_size = state_size, well_formed = well_formed) 

def isUrl(str):
    if(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str)):
        return True
    return False

#regex match
matches = [r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'(\<.*?\>)', r'\>']

