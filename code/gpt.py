from openai import OpenAI
client = OpenAI(api_key ="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" )
import time

def generate_openai(prompt):
    try: 
        response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a research scientist."},
        {"role": "user", "content": f"{prompt}"}
    ]
    )
        return response.choices[0].message.content
    except:
        pass
    time.sleep(10)
