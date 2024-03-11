"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import time

from transformers import GPT2Tokenizer

# Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')  # Assuming GPT-2's tokenizer is similar to GPT-4's


# genai.configure(api_key="AIzaSyAHqw-apjZtd6bcL3LL95yMfgI-dRJKZ6M")
#AIzaSyAKz7WR9dG4ibeOkQIbk4nDidFH9qTtisg
genai.configure(api_key="AIzaSyAKz7WR9dG4ibeOkQIbk4nDidFH9qTtisg")

# Set up the model
generation_config = {
  "temperature": 0.0,
  "top_p": 0.8,
  "top_k": 5,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def inference(text):
    # if len(tokenizer(text))>30000:
    #     print("greater than allowed")
    #     return None
    try:
        response = model.generate_content(text)
    except Exception as e:
        return None
    
    try:
        response.text
    except Exception as e:
        return None
    time.sleep(2)
    return response.text