import boto3
import json
bedrock = boto3.client(service_name='bedrock-runtime')
modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'
import time

def inference(text):   
    body = json.dumps({
        "prompt": text,
        "max_tokens_to_sample": 512,
        "temperature": 0.0,
        "top_p": 0.9,
    })

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')