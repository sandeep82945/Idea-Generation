import json
import os
import pandas as pd

import openai
openai.api_key = ""
import json
import os
import nltk
nltk.download('punkt')
import re

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
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
    max_tokens=300)
    # print the chat completion
    input_text = response['choices'][0]['message']['content']
    return extract_answer(input_text), extract_reviews(input_text), input_text

def get_text_for_conclusion(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    #print(json_file_path)
    if 'sections' in data:
        for element in data['sections']:
            if 'heading' in element and 'text' in element:
                heading = element['heading'].lower()
                if 'future' in heading:
                    if(len(heading)<15):
                        return element['text']
                    else:
                        if(len(element['text'])<10):
                            return None
                        prompt='you are given text of conclusion of research paper.return only the future work text from input text.input text is as follows: '+ element['text']
                        op= response_chat(prompt)[2]
                        return op
                elif 'conclusion' in heading and len(heading) < 12:
                    prompt='you are given text of conclusion of research paper.return only the future work text from input text.input text is as follows: '+ element['text']
                    op= response_chat(prompt)[2]
                    return op


    # If no conclusion heading is found, return None or handle accordingly
    return None

def process_json_files_in_folder(folder_path):
    output_dict = {}
    count=0
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            result = get_text_for_conclusion(json_file_path)
            print(json_file_path)

            if result is not None:
                output_dict[filename] = result
                count+=1
                if(count>300):
                    break


    return output_dict

# Replace 'your_folder_path' with the actual path to your folder containing JSON files
domain='computer'
folder_path=os.path.join("D:\s2-folks\scipdf_parser",domain+"_json")
output_dictionary = process_json_files_in_folder(folder_path)
print(output_dictionary)

for filename, result in output_dictionary.items():
    if result is not None:
        print(f"Text for 'conclusion' in {filename}: {result}")
    else:
        print(f"No 'conclusion' heading found in {filename}.")
df = pd.DataFrame(list(output_dictionary.items()), columns=['JSON ID', 'Future Work'])

# Save the DataFrame to an Excel file
excel_file_path = f'output_data_{domain}.xlsx'
df.to_excel(excel_file_path, index=False)
