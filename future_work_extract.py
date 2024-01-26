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

def extract_answer(input_text):
    tokens = nltk.word_tokenize(input_text)
    for word in tokens:
        if word.lower() in ['yes', 'no']:
            return word.lower()
    return 'no'

import re
def extract_reviews(input_string):
    pattern = r'Review1:\s*"([^"]*)"\s*[^"]*Review2:\s*"([^"]*)"'
    matches = re.findall(pattern, input_string)

    return matches

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
    retries = 3    
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
            return extract_answer(input_text), extract_reviews(input_text), input_text
        
        except Exception as e:    
            if e: 
                print(e)   
                print('Timeout error, retrying...')
                retries -= 1    
                time.sleep(5) 


def get_text_from_conclusion(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    if 'sections' in data:
        for element in data['sections']:
            if 'heading' in element and 'text' in element:
                heading = element['heading'].lower()
                if 'conclusion' in heading:
                    if(len(element['text'])<10 or len(enc.encode(element['text']))>2048):
                            return None
                    prompt='You are given text of conclusion of a research paper. Extract and Return only the portion of the text that discusses future works. Input text is as follows: '+ element['text']
                    op= response_chat(prompt)[2]
                    return op


def get_text_from_future(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    if 'sections' in data:
        for element in data['sections']:
            if 'heading' in element and 'text' in element:
                heading = element['heading'].lower()
                if 'future' in heading:
                    print(json_file_path)
                    if(len(heading)<15):
                        return element['text']
                    else:
                        if(len(element['text'])<10 or len(enc.encode(element['text']))>2048):
                            return None
                        prompt='You are given text of conclusion of a research paper. Extract and Return only the portion of the text that discusses future works. Input text is as follows: '+ element['text']
                        op= response_chat(prompt)[2]
                        return op
    return None

temp=config['number_of_files']

def process_json_files_in_folder(folder_path, checkpoint_file, output_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as file:
            processed_files = file.read().splitlines()
    else:
        processed_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and filename not in processed_files:
            json_file_path = os.path.join(folder_path, filename)
            result = get_text_from_future(json_file_path) or get_text_from_conclusion(json_file_path)

            if result is not None:
                # Data to be appended
                new_data = pd.DataFrame({'JSON ID': [filename], 'Future Work': [result]})

                # Check if the output file already exists
                if os.path.exists(output_file):
                    # Read existing data
                    existing_data = pd.read_excel(output_file)
                    # Concatenate new data
                    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                    # Write back to the file
                    updated_data.to_excel(output_file, index=False)
                else:
                    # Create a new file
                    new_data.to_excel(output_file, index=False)

                # Update the checkpoint file
                with open(checkpoint_file, 'a') as file:
                    file.write(filename + '\n')

    return
'''
def process_json_files_in_folder(folder_path, checkpoint_file, output_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as file:
            processed_files = file.read().splitlines()
    else:
        processed_files = []

    output_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and filename not in processed_files:
            json_file_path = os.path.join(folder_path, filename)
            result = get_text_from_future(json_file_path) or get_text_from_conclusion(json_file_path)

            if result is not None:
                output_dict[filename] = result
                with open(checkpoint_file, 'a') as file:
                    file.write(filename + '\n')

                # Update the output file regularly
                df = pd.DataFrame(list(output_dict.items()), columns=['JSON ID', 'Future Work'])
                df.to_excel(output_file, index=False)

    return output_dict
'''

# Replace 'your_folder_path' with the actual path to your folder containing JSON files
domain = config['domain']
input_path = config['input_path']


folder_path = os.path.join(input_path, domain + "_json")
checkpoint_file = f'processed_files_{domain}.txt'
output_file = f'output_data_{domain}.xlsx'

output_dictionary = process_json_files_in_folder(folder_path, checkpoint_file, output_file)

# # Print the results
# for filename, result in output_dictionary.items():
#     if result is not None:
#         print(f"Text for 'conclusion' in {filename}: {result}")
#     else:
#         print(f"No 'conclusion' heading found in {filename}.")