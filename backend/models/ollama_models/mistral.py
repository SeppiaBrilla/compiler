from models.model import LLM_model
import requests
from subprocess import run
import json

class Mistral_compiler(LLM_model):
    MODEL_NAME = 'Mistral-compiler'
    FILE_NAME = './MistralModelFile'
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    def __init__(self, functions) -> None:
        if not self.__is_model_present():
            self.__create_model(functions)
        
    def query(self, query):
        body =  json.dumps({
              "model": self.MODEL_NAME,
              "prompt": query,
              "stream": False
        })
        response = requests.post('http://localhost:11434/api/generate', data=body)
        return response.json()['response']

    def __is_model_present(self):
        try:
            elements = requests.get('http://localhost:11434/api/tags').json()

            return self.MODEL_NAME in elements
        except:
            return False
    
    def __create_model(self, functions):
        model = f'''
FROM mistral
PARAMETER temperature 0.5

SYSTEM """ 
You are an AI assistant that helps compiling code.
You have a set of fuctions you can call to assist you on the job. You can call them as stated below:
            function = example
            correct call = ```example(parameters)```
If there is a function that can be used use it instead of giving your idea.
Your answer must contain the function call and act as if the correct result from the call is already present instead of the function call. Example:
"Here it is the result of the function example on the parameter: ```example(parameter)```". 
Every parameter is always mandatory. The empty array can be noted as: []. Each value inside the array must be separated by commas. Example:
```example2([value1,value2,value3])```
{functions}
"""
        '''
        f = open(self.FILE_NAME, 'w')
        f.write(model)
        f.close()
        run(['ollama', 'create', self.MODEL_NAME, '-f', self.FILE_NAME], check=True)
