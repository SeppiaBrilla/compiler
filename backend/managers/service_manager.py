# from backend.models.model import LLM_model
from re import findall
import logging
from typing import Tuple

from managers.plugin_manager import Plugin_manager

class Service_manager:
    def __init__(self, model, plugin_manager:Plugin_manager) -> None:
        self.model = model
        self.plugin_manager = plugin_manager

    def query_model(self, query:str, plugin_name:str) -> Tuple[str, dict[str, list[str]]]:
        logging.log(logging.INFO,f'plugin {plugin_name} has queried the model with the following query:\n{query}')
        response = self.model.query(query)
        response = '_$compile:..$_'
        return response, self.answer_parser(response)

    def call_plugin(self, plugin_name):
        self.plugin_manager.use_plugin(plugin_name )
    

    def answer_parser(self, answer:str) -> dict[str,list[str]]:
        functions = findall('\\_\\$([a-zA-Z0-9_ :\\-\\.,]*)\\$\\_',answer)
        functions_dict = {}
        for function in functions:
            split_function = function.split(':') 
            if split_function[-1] == '':
                del split_function[-1]

            functions_dict[split_function[0]] = split_function[1].split(' ') if len(split_function) > 1 else []
        return functions_dict

   
