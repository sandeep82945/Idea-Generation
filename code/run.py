import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')
import yaml
tokenizer = PunktSentenceTokenizer()

from test_preprocessing import preprocess

with open('code/config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

paper_dump_path = config["paper_dump_path"]
input_folder = config["input_folder"]
model_name = config["model_name"]
domain = input_folder.split('/')[-1]


dump_folder = os.path.join(paper_dump_path,model_name, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

#Change this for each models
def generate_ideas(response):
    return response

for filename in os.listdir(input_folder):
    if not filename.endswith('.txt'):
        continue
    
    dump_filename = os.path.join(dump_folder, filename)+'.txt'
    if os.path.exists(dump_filename):
            continue
    
    reponse = ''
    filepath = os.path.join(input_folder,filename)
    with open(filepath, 'r') as f:
         text = f.read()
         text = text.replace('\n', ' ')
         reponse = preprocess(text)
         response = generate_ideas(reponse)
         if response is None:
             continue

    with open(dump_filename, 'w') as f:
        f.write(response)