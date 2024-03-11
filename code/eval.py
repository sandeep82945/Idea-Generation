import nltk
nltk.download('stopwords')

model = 'gemini'
domain = 'physics'
import pandas as pd
future_work_df = pd.read_excel('data/idea_physics.xlsx')


import torch
if torch.backends.mps.is_available():
    print("yes")
    device = torch.device('mps')

from summ_eval.bert_score_metric import BertScoreMetric
bert_score=BertScoreMetric()

from summ_eval.blanc_metric import BlancMetric
blanc_score=BlancMetric()

# from summ_eval.mover_score_metric import  MoverScoreMetric
# mover_score= MoverScoreMetric()

from summ_eval.sentence_movers_metric import SentenceMoversMetric
sentence_mover_score=SentenceMoversMetric()

from summ_eval.summa_qa_metric import  SummaQAMetric
summa_qa_score= SummaQAMetric()

# from summ_eval.supert_metric import SupertMetric
# supert_score =SupertMetric()

from summ_eval.meteor_metric import  MeteorMetric
meteor_score =  MeteorMetric()

# from summ_eval.s3_metric import S3Metric
# s3_metric =S3Metric()

# from summ_eval.syntactic_metric import  SyntacticMetric
# syntactic_score =SyntacticMetric()

from summ_eval.cider_metric import CiderMetric
cider_score = CiderMetric()

from summ_eval.chrfpp_metric import  ChrfppMetric
chrfpp_score= ChrfppMetric()

def Evaluate_R(summaries, references,type:str="rouge"):

  #summaries- A list of summaries
  #references- A list of predicted summaries

  if(type=="rouge"):
    score_dict = rouge.evaluate_batch(summaries, references)

  if(type=="bert_score"):
    score_dict=bert_score.evaluate_batch(summaries,references)

  if(type=="blanc_score"):
    score_dict=blanc_score.evaluate_batch(summaries,references)

  if(type=="mover_score"):
    score_dict=mover_score.evaluate_batch(summaries,references)

  if(type=="sentence_mover_score"):
    score_dict=sentence_mover_score.evaluate_batch(summaries,references)

  if(type=="summa_qa_score"):
    score_dict=summa_qa_score.evaluate_batch(summaries,references)

  if(type=="supert_score"):
    score_dict=supert_score.evaluate_batch(summaries,references)

  if(type=="meteor_score"):
    score_dict=meteor_score.evaluate_batch(summaries,references)

  if(type=="s3_metric"):
    score_dict=s3_metric.evaluate_batch(summaries,references)

  if(type=="syntactic_score"):
    score_dict=syntactic_score.evaluate_batch(summaries,references)

  if(type=="cider_score"):
    score_dict=cider_score.evaluate_batch(summaries,references)

  if(type=="chrfpp_score"):
    score_dict=chrfpp_score.evaluate_batch(summaries,references)

  if(type=="blue_score_4"):
    # score_dict=blue_score_4.evaluate_batch(summaries,references)
    score_dict = BleuMetric(n=4).compute_bleu(summaries, references)

  if(type=="blue_score_3"):
    # score_dict=blue_score_3.evaluate_batch(summaries,references)
    score_dict = BleuMetric(n=3).compute_bleu(summaries, references)

  if(type=="blue_score_2"):
    # score_dict=blue_score_2.evaluate_batch(summaries,references)
    score_dict = BleuMetric(n=2).compute_bleu(summaries, references)

  if(type=="blue_score_1"):
    # score_dict=blue_score_1.evaluate_batch(summaries,references)
    score_dict = BleuMetric(n=1).compute_bleu(summaries, references)
  return score_dict

import pandas as pd
import os
folder_path = os.path.join('data/Response/',model, domain)

import re
# def extract_responses(text):
#     re.
paper_id = future_work_df['paper_id'].tolist()
Future_work = future_work_df['Future_work'].tolist()
future_dict = dict(zip(paper_id, Future_work))

summaries = []
references = []
for file_name in os.listdir(folder_path):
    if( not file_name.endswith('.txt')):
        continue
    with open(os.path.join(folder_path, file_name), 'r') as f:
        text = f.read()
        new_filename = 'output_'+file_name.split('.')[0] + '.pdf.json'
        if not new_filename in future_dict.keys():
          print(new_filename)
          continue
        summaries.append(text)
        future = future_dict[new_filename]
        references.append(future)

print("Scores are: ")
score_lists = ["bert_score","cider_score"]
for value in score_lists:
  print("The result of :", value)
  print(Evaluate_R(summaries, references,value))
