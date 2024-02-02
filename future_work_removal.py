import pandas as pd
import os
import yaml
import json
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

from future_work_RE_extractor import future_work_extraction_algorithm


with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

file_names = ['output_data_comp22.xlsx']

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
                paper_text = paper_text + heading + text

    return paper_text

def extract_future_work_text_from_response(text):
    sentences = []

    pattern = r'The future work.*?:\s*(.*)'

    # Find the match using re.DOTALL to make '.' match newlines
    match = re.search(pattern, text, re.DOTALL)
    # Print the matched text
    if match:
        extracted_text = match.group(1)
        extracted_text = extracted_text.replace('\"',"")
        sentences += sent_tokenize(extracted_text)
    else:
        print("No matching text found.")

    return sentences

def remove_future_work_sentences(paper_data_sentences, future_work_sentences, similarity_threshold=0.5, percentage_matched_limit=90.0):
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

    for future_sentence in future_work_sentences:
        for paper_sentence in paper_data_sentences:
            if sentence_similarity(paper_sentence, future_sentence) >= similarity_threshold:
                matched_sentences.append((future_sentence, paper_sentence))
                break
        else:
            filtered_sentences.append(future_sentence)

    total_future_work_sentences = len(future_work_sentences)
    percentage_matched = (len(matched_sentences) / total_future_work_sentences) * 100 if total_future_work_sentences > 0 else 0

    print(f"Percentage of future work sentences that matched: {percentage_matched:.2f}%")
    # if matched_sentences:
    #     print("Matched sentence pairs (Future Work Sentence : Paper Sentence):")
    #     for future_sentence, paper_sentence in matched_sentences:
    #         print(f" - {future_sentence} : {paper_sentence}")

    if percentage_matched<percentage_matched_limit:
        print("returning NULL")
        return None

    future_sentences =  [sentence for sentence in paper_data_sentences if sentence not in [fw for fw, _ in matched_sentences]]

    return future_sentences

for file in file_names:
    dic = {}
    domain = file.split('_')[-1].split('.')[0]
    economics_data = pd.read_excel(file)
    for index, rows in economics_data.iterrows():
        paper_id = rows[0]
        future_work = rows[1]
        input_file_path = os.path.join(config['input_path'], domain+'_json',paper_id)  #verify path 
        paper_data = read_json(input_file_path)
        future_work_sentences = extract_future_work_text_from_response(future_work)
        paper_data_sentences = nltk.sent_tokenize(paper_data)
        if len(future_work_sentences) == 0:
            continue

        removed_paper_sentences = remove_future_work_sentences(paper_data_sentences, future_work_sentences, similarity_threshold=0.8)

        if removed_paper_sentences is None:
            continue
        
        dic[paper_id] = {'paper_id': paper_id, 'full_text': paper_data, 'full_text_WF': ' '.join(removed_paper_sentences), 'Future_work': ' '.join(future_work_sentences)}

    data = []
    for paper_id, attributes in dic.items():
        data.append({
            **attributes
        })

    df = pd.DataFrame(data)

    excel_file_path = f'Idea_{domain}.xlsx'
    df.to_excel(excel_file_path, index=False)

    # print(df['Future_work'])
        # print(df.head)

    
    # json_object = json.dumps(dic, indent = 8) 

    # output_path = f'Idea_{domain}.json'

    # with open(output_path, 'w') as json_file:
    #     json.dumps(dic, json_file, indent=4)

