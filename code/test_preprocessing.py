import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import os
import re

nltk.download('punkt')

def remove_brackets(text):
    pattern = r'\[.*?\]'
    result = re.sub(pattern, '', text)
    return result

# Sample text
text = "This is a [sample] text [with] some [brackets]."

# Remove parts enclosed within square brackets
cleaned_text = remove_brackets(text)

# Print the cleaned text
print(cleaned_text)

def tokenize_and_count(text):
    sent = sent_tokenize(text)
    for s in sent:
        wrd=word_tokenize(s)
        if(len(wrd)<=5):
            sent.remove(s)
    final_txt= ' '.join(sent)
    return final_txt
text=''
result=remove_brackets(text)
data=tokenize_and_count(result)
print(data)

