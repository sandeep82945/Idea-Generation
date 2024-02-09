import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')

tokenizer = PunktSentenceTokenizer()

foldername= 'data/WF_paper_text/computer'

paper_dump_path = 'data/Response'


domain = foldername.split('/')[-1]

dump_folder = os.path.join(paper_dump_path, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

def preprocess(text):
     return text

def generate_ideas(response):
    return response

for filename in os.listdir(foldername):
    if not filename.endswith('.txt'):
        continue
    reponse = ''
    filepath = os.path.join(foldername,filename)
    with open(filepath, 'r') as f:
         text = f.read()
         text = text.replace('\n', ' ')
         reponse = preprocess(text)
         response = generate_ideas(reponse)
         if response is None:
             continue
    with open(os.path.join(dump_folder, filename)+'.txt', 'w') as f:
        f.write(response)