import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import os

nltk.download('punkt')

def tokenize_and_count(folder_path):
    total_tokens = 0
    count=[]
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            f=0
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            sent = sent_tokenize(text)
            for s in sent:
                wrd=word_tokenize(s)
                if(len(wrd)<=4):
                    sent.remove(s)
                else:
                    f+=len(wrd)
            #for s in sent:
                #print(s)
            count.append(f)
            if(f>20000):
                print(f)
                print(filename)
    count.sort()
    print(len(count))
    s=0      
    for i in count:
        s+=i
    return s/len(count)

folder_path=os.path.join("D:\dsa","final\chemistry22")
num_tokens = tokenize_and_count(folder_path)
print(num_tokens)

