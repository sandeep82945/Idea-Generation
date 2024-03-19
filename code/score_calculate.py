import os
domain = 'economics'
model_name = 'GPT-4'
import pandas as pd
import torch
from typing import List

from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained('roberta-large-mnli')
model = AutoModelForSequenceClassification.from_pretrained('roberta-large-mnli')

def text_to_list(text):
    # Split the text into individual lines
    topics = text.strip().split("\n")
    # Remove any empty strings resulting from splitting
    topics = [topic.strip() for topic in topics if topic.strip()]
    return topics

def infer_score_average(hypotheses: List[str], predicate: str) -> float:
    """
    Computes the average entailment score between a predicate and a list of hypotheses.

    Args:
        hypotheses (List[str]): A list of hypothesis sentences.
        predicate (str): The predicate sentence.

    Returns:
        float: The average entailment score.
    """
    # Load the tokenizer and model

    scores = []
    for hypothesis in hypotheses:
        # Encode the predicate and hypothesis
        inputs = tokenizer(predicate, hypothesis, return_tensors='pt', padding=True, truncation=True)

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Softmax to get probabilities
        probs = torch.softmax(outputs.logits, dim=-1)

        # Assuming "entailment" is the first class (index 0), adjust if necessary based on the model
        entailment_prob = probs[:,0].item()
        scores.append(entailment_prob)

    # Calculate average score
    average_score = sum(scores) / len(scores) if scores else 0
    return average_score


if domain == 'chemistry':
    all_score = 0
    predicates = []
    hypothesiss = []
    path = 'data/Response/' + model_name
    files = ['chemistry', 'chem_more']
    length = 0
    for file in files:
        if file == 'chemistry':
            true_csv = pd.read_excel('data/Idea_'+file+'.xlsx')
        else:
            true_csv = pd.read_excel('data/Idea_chemistryMORE'+'.xlsx')
        ids = true_csv['paper_id']
        future_work = true_csv['Future_work']
        result_dict = {ids[i].split('.')[0].replace('output_',''): future_work[i] for i in range(min(len(ids), len(future_work)))}

        text_paths  = os.listdir(os.path.join(path,file))
        for text_path in text_paths:
            if not text_path.endswith('.txt'):
                continue
            with open(os.path.join(os.path.join(path,file),text_path),'r') as f:
                print(text_path)
                text = f.read()
                hypothesis = text_to_list(text)
                if text_path.replace(".txt",'') in result_dict.keys():
                    predicate = result_dict[text_path.replace(".txt",'')]
                    score = infer_score_average(hypothesis,predicate)
                    all_score +=score
                    length+=1

    print(all_score/length)



if domain == 'computer':
    all_score = 0
    predicates = []
    hypothesiss = []
    path = 'data/Response/' + model_name
    files = ['comp_more','computer']
    length = 0
    for file in files:
        if file == 'computer':
            true_csv = pd.read_excel('data/Idea_'+file+'.xlsx')
        else:
            true_csv = pd.read_excel('data/Idea_computerMORE'+'.xlsx')
        ids = true_csv['paper_id']
        future_work = true_csv['Future_work']
        result_dict = {str(ids[i]): future_work[i] for i in range(min(len(ids), len(future_work)))}

        text_paths  = os.listdir(os.path.join(path,file))
        for text_path in text_paths:
            if not text_path.endswith('.txt'):
                continue
            with open(os.path.join(os.path.join(path,file),text_path),'r') as f:
                print(text_path)
                text = f.read()
                hypothesis = text_to_list(text)
                if text_path.replace(".txt",'') in result_dict.keys():
                    predicate = result_dict[text_path.replace(".txt",'')]
                    score = infer_score_average(hypothesis,predicate)
                    all_score +=score
                    length+=1

    print(all_score/length)


if domain == 'economics':
    all_score = 0
    predicates = []
    hypothesiss = []
    path = 'data/Response/' + model_name
    files = ['eco_more','economics']
    length = 0
    for file in files:
        if file == 'economics':
            true_csv = pd.read_excel('data/Idea_'+file+'.xlsx')
        else:
            true_csv = pd.read_excel('data/Idea_economicsMORE'+'.xlsx')
        ids = true_csv['paper_id']
        future_work = true_csv['Future_work']
        result_dict = {str(ids[i]): future_work[i] for i in range(min(len(ids), len(future_work)))}

        text_paths  = os.listdir(os.path.join(path,file))
        for text_path in text_paths:
            if not text_path.endswith('.txt'):
                continue
            with open(os.path.join(os.path.join(path,file),text_path),'r') as f:
                print(text_path)
                text = f.read()
                hypothesis = text_to_list(text)
                if text_path.replace(".txt",'') in result_dict.keys():
                    predicate = result_dict[text_path.replace(".txt",'')]
                    score = infer_score_average(hypothesis,predicate)
                    all_score +=score
                    length+=1

    print(all_score/length)