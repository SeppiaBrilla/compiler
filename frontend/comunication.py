import requests
import json

class LLM_comunincation:
    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }
    def __init__(self, port:int):
        self.port = port

    def query_llm(self, query:str, plugin_name:str):
        body = json.dumps({
            'query':query,
            'plugin':plugin_name
        })
        response = requests.post(f'http://localhost:{self.port}/query', data=body, headers=self.headers)
        response = response.json()
        return response

    def get_data(self, plugin_name:str, element:int = -1):
        return requests.get(f'http://localhost:{self.port}/storage/{plugin_name}/{element}').json()

    def call_plugin(self, plugin_name:str, parameters:dict):
        body = json.dumps({'parameters': parameters})
        requests.post(f'http://localhost:{self.port}/call_plugin/{plugin_name}', data=body, headers=self.headers)
        return self.get_data(plugin_name).json()

    def save_data(self, plugin_name, data):
        body = json.dumps({'data': data})
        requests.post(f'http://localhost:{self.port}/save_data/{plugin_name}', data=body, headers=self.headers)

    def get_parameters(self, plugin_name):
        return requests.get(f'http://localhost:{self.port}/parameters/{plugin_name}').json()


