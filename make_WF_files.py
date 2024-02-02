#This code to be run after each annotated Idea domain. Files is done.
#It is for making input txt file without future work creation

import os
import pandas as pd
import json
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
nltk.download('punkt')

tokenizer = PunktSentenceTokenizer()

filename = 'Idea_chemistry.xlsx'

domain = filename.split('.')[0].split('_')[1]

input_file_path = 'pdf_json_2023/chemistry_json'

paper_dump_path = 'data/WF_paper_text'

df = pd.read_excel(os.path.join('data',filename))


def remove_future_work_sentences(paper_id, paper_data_sentences, future_work_sentences, similarity_threshold=0.5, percentage_matched_limit=90.0):
    """
    Removes sentences about future work from the main text of the paper, calculates the percentage 
    of future work sentences that matched with the main text, and prints the matched sentences along with 
    their corresponding matching sentences from the main text.

    :param paper_data_sentences: List of sentences from the paper.
    :param future_work_sentences: List of sentences from the future work section of the paper.
    :param similarity_threshold: Fraction of words that must be common to consider sentences similar.
    :return: List of sentences from the paper excluding similar sentences from future work.
    """
    def sentence_similarity(sent1, sent2):
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())
        common_words = words1.intersection(words2)
        return len(common_words) / max(len(words1), len(words2))

    matched_sentences = []
    filtered_sentences = []

    future_work_sentences = [future_sentence.replace('..','.') for future_sentence in future_work_sentences]

    for future_sentence in future_work_sentences:
        for paper_sentence in paper_data_sentences:
            if sentence_similarity(paper_sentence, future_sentence) >= similarity_threshold:
                matched_sentences.append((future_sentence, paper_sentence))
                break
        else:
            filtered_sentences.append(future_sentence)

    total_future_work_sentences = len(future_work_sentences)
    percentage_matched = (len(matched_sentences) / total_future_work_sentences) * 100 if total_future_work_sentences > 0 else 0

    print(f"{paper_id}: Percentage of future work sentences that matched: {percentage_matched:.2f}%")
    # if matched_sentences:
    #     print("Matched sentence pairs (Future Work Sentence : Paper Sentence):")
    #     for future_sentence, paper_sentence in matched_sentences:
    #         print(f" - {future_sentence} : {paper_sentence}")

    if percentage_matched<percentage_matched_limit:
        print("returning NULL")
        print(paper_id)
        print(future_work_sentences)
        print("-------------------")
        return None

    future_sentences =  [sentence for sentence in paper_data_sentences if sentence not in [fw for fw, _ in matched_sentences]]

    return future_sentences

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

for index, item in df.iterrows():
    json_path = os.path.join(input_file_path, "output_"+item[0].split('_')[1])
    paper_data = read_json(json_path)
    paper_data_sentences = nltk.sent_tokenize(paper_data)

    future_work_text = item[-1].replace('..','.')

    future_work_sentences = nltk.sent_tokenize(future_work_text)
    paper_id = item[0].split('_')[1].split('.')[0]
    # if paper_id != '6cacfc536e183841cc0a8817a0346eeb513bad96':
    #     continue
    

    if len(future_work_sentences) == 0:
            continue
    
    removed_paper_sentences = remove_future_work_sentences(paper_id, paper_data_sentences, future_work_sentences, similarity_threshold=0.8)

    if(removed_paper_sentences == None):
        continue

    WF_text = ' '.join(removed_paper_sentences)
    # WF_text = ' '.join(paper_data_sentences)

    with open(os.path.join(dump_folder, paper_id)+'.txt', 'w') as f:
        f.write(WF_text)

             