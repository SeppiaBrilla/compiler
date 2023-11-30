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
PARAMETER temperature 0.7

SYSTEM """ 
You are an AI assistant that helps managing the compilation task of some code.
This data describes a set of command you can use to fullfill some requests. you can use them by calling the function followed by the charachter ":" and its parameters. 
        The function call must be sourranded by the charachters _$ and $_. If the call contains the value "(None)" it means there are no parameters. 
        Example:
            function = list-folder-content
            correct call = _$list-folder-content:folder$_
Your answer must contain the function call and act as if the correct result from the call is already present instead of the function call. Example:
"Here it is the content of the folder 'folder': _$list-folder-content:folder$_"
{functions}
"""
        '''
        print(model)
        f = open(self.FILE_NAME, 'w')
        f.write(model)
        f.close()
        run(['ollama', 'create', self.MODEL_NAME, '-f', self.FILE_NAME], check=True)
