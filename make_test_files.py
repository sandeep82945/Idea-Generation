#This code to be run after each annotated Idea domain. Files is done.
#It is for making input txt file without future work creation

import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')
tokenizer = PunktSentenceTokenizer()

domain = 'eco_more2'

input_file_path = 'data/eco2json'

paper_dump_path = 'data/WF_paper_text'

def read_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    paper_text = ''
    if 'abstractText' in data:
        paper_text = paper_text + data['abstractText']

    if 'sections' in data:
        for element in data['sections']:
            if 'heading' in element and 'text' in element:
                heading = element['heading'].lower()
                text =element['text']
                paper_text = paper_text + " " + heading + " "+ text
                paper_text.replace('..','.')

    return paper_text

dump_folder = os.path.join(paper_dump_path, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

for item in os.listdir(input_file_path):
    if not item.endswith('.json'):
        continue
    json_path = os.path.join(input_file_path,item)
    paper_data = read_json(json_path)
    paper_data_sentences = nltk.sent_tokenize(paper_data)
    paper_id = item.split('_')[1]#.split('.')[2]
    WF_text = ' '.join(paper_data_sentences)

    with open(os.path.join(dump_folder, paper_id)+'.txt', 'w') as f:
        f.write(WF_text)
     