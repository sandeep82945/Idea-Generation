import json
import os
import pandas as pd
import time
import openai
import json
import os
import nltk
nltk.download('punkt')
import re
import tiktoken
import yaml

# Load the configuration from the YAML file
with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

openai.api_key = config["open_ai_key"]

domain = config['domain']
folder_path = os.path.join('data/WF_paper_text', domain)

enc = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")

def response_completion(prompt):
    response = openai.Completion.create(
    model="gpt-3.5-turbo-1106",
    temperature=0,
    max_tokens=300,
    top_p=0.9,
    frequency_penalty=0,
    presence_penalty=0
    )
    # print the chat completion
    input_text = response.choices[0].text
    
    return extract_answer(input_text), input_text

def response_chat(prompt):
    retries = 10    
    while retries > 0: 
        try: 
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=500, request_timeout=15)
            input_text = response['choices'][0]['message']['content']
            return input_text
        
        except Exception as e:    
            if e: 
                print(e)   
                print('Timeout error, retrying...')
                retries -= 1    
                time.sleep(5) 



def get_text_from_paper(text_file_path):
    with open(text_file_path) as f:
        return f.read()


    
prompt = '''
I am providing you research paper text. Extract the sentences/portion of text , where future research direction is mentioned:

Output should Quote the Paper text:

'''
paper_dump_path = 'verification_data'
dump_folder = os.path.join(paper_dump_path, domain)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)
    
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        paper_id = filename.split('.')[0]
        paper_text = get_text_from_paper(os.path.join(folder_path,filename))
        full_prompt = prompt + paper_text
        response = response_chat(prompt + paper_text)
        with open(os.path.join(dump_folder, paper_id)+'.txt', 'w') as f:
            f.write(response)
        exit(0)


# Replace 'your_folder_path' with the actual path to your folder containing JSON files



# # Print the results
# for filename, result in output_dictionary.items():
#     if result is not None:
#         print(f"Text for 'conclusion' in {filename}: {result}")
#     else:
#         print(f"No 'conclusion' heading found in {filename}.")