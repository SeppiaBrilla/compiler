from re import findall
import logging
from typing import Tuple

from managers.plugin_manager import Plugin_manager

class Service_manager:
    def __init__(self, model, plugin_manager:Plugin_manager) -> None:
        self.model = model
        self.plugin_manager = plugin_manager
        self.history = []

    def query_model(self, query:str, plugin_name:str) -> Tuple[str, dict[str, list[str]]]:
        logging.log(logging.INFO,f'plugin {plugin_name} has queried the model with the following query:\n{query}')
        history = '/n'.join(self.history)
        query = history + '/n' + query
        response = self.model.query(query)
        return response, self.answer_parser(response)

    def call_plugin(self, plugin_name):
        self.plugin_manager.use_plugin(plugin_name )
    
    def add_to_history(self, history_message:str):
        self.history.append(history_message)

    def answer_parser(self, answer:str) -> dict[str,list[str]]:
        answer = answer.replace("'", "")
        answer = answer.replace('"', '')
        functions = findall('\\`\\`\\`([a-zA-Z0-9_ \\-\\.,]*\\([a-zA-Z0-9_ /\\-\\.,\\[\\]]*\\))\\`\\`\\`',answer)
        functions_dict = {}
        for function in functions:
            split_function = function[:-1].split('(') 
            if split_function[-1] == '':
                del split_function[-1]
            if not split_function[0] in functions_dict:
                functions_dict[split_function[0]] = []
            
            array = {}
            print('splitting parameters:', split_function[1], '[' in split_function[1])
            if '[' in split_function[1]:
                arrays = findall('(\\[[a-zA-Z0-9_ /\\-\\.,]*\\])', split_function[1])
                base = "ARRAY_VALUE"
                print(arrays)
                for i in range(len(arrays)):
                    values = arrays[i][1:-1].split(',')
                    print('array values:',values)
                    array[base + str(i)] = values
                    split_function[1] = split_function[1].replace(arrays[i], base + str(i), 1)
                
            functions_dict[split_function[0]].append(split_function[1].split(',') if len(split_function) > 1 else [])
            for i in range(len(functions_dict[split_function[0]][-1])):
                if functions_dict[split_function[0]][-1][i] in array.keys():
                    functions_dict[split_function[0]][-1][i] = array[functions_dict[split_function[0]][-1][i]]
        return functions_dict

   
