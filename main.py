from query_model import Query_model, get_queryModel
from plugin_manager import Plugin_manager
from chat_manager import Chat_manager
from langchain.docstore.document import Document
from re import findall
import logging

def answer_parser(answer:str) -> dict[str,list[str]]:
    functions = findall('\\_\\$([a-zA-Z0-9_ :\\-\\.,]*)\\$\\_',answer)
    functions_dict = {}
    for function in functions:
        split_function = function.split(':') 
        if split_function[-1] == '':
            del split_function[-1]

        functions_dict[split_function[0]] = split_function[1].split(' ') if len(split_function) > 1 else []
    return functions_dict
conf = [
    {
        'name': 'list-folder-content',
        'parameters': 'ls:folder',
        'description':'lists all the file in a given folder'
    },
    {
        'name': 'say hello',
        'parameters': 'echo hello!:',
        'description':'say hello to you'
    },
    {   
        'name': 'compile',
        'parameters':'python3 compile_risc.py: program_name file_name',
        'description':'compile a the file called "file_name" into a program called "program_name"'
    },
    {   
        'name':'execute',
        'parameters': 'spike pk -s: program_name',
        'description': 'execute the program called "program_name" and returns the execution statistics'
    }
]
chat_manager = Chat_manager()
# model_name = "mistralai/Mistral-7B-v0.1"
model_name = 'gpt2'
model = get_queryModel(model_name)
manager = Plugin_manager(conf)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
document = Document(page_content=str(manager))
if isinstance(model, Query_model):
    model.add_documents(document)

while True:
    msg = input('query the llm: ')
    if 'exit()' in msg:
        break
    chat_manager.clear()
    print(chat_manager.get_user_message(msg))
    response = model.query(msg)
    functions = answer_parser(response)
    for name in functions.keys():
        logging.debug(f'the model called the function {name} with parameters {functions[name]}')
        logging.debug(f'the result is: {manager.use_plugin(name, functions[name])}')
    print(chat_manager.get_console_message(response))
