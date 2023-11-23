from model import LLM_model
from plugin_manager import Plugin_manager
from chat_manager import Chat_manager
from langchain.docstore.document import Document
from re import findall
def get_query(query:str) -> str:
    return f'''
    This data describes a set of command you can use to fullfill some requests. you can use them by calling the function followed by the charachter ":" and its parameters. 
    The function call must be sourranded by the charachters _$ and $_. If the call contains the value "(None)" it means there are no parameters. 
    Example:
        function = list-folder-content
        correct call = _$list-folder-content:folder$_

    {query}'''

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
        'parameters': 'spike pk -s: program_name'
        'description' 'execute the program called "program_name" and returns the execution statistics'
    }
]
chat_manager = Chat_manager()
model_name = "mistralai/Mistral-7B-v0.1"
# model_name = 'gpt2'
model = LLM_model(model_name)
manager = Plugin_manager(conf)

document = Document(page_content=str(manager))
# query = get_query('Does exists a function that says hello to someone? if so, call it and pretend to already have the answer instead of only the call')
# response = model.query([document], query)
# print(response)

while True:
    msg = input()
    if 'exit()' in msg:
        break
#     # chat_manager.clear()
#     # print(chat_manager.get_user_message(msg))
#     # print(chat_manager.get_console_message(model.query([document], get_query(msg))))
    print(f'user: {msg}')
    response = model.query([document], get_query(msg))
    functions = answer_parser(response)
    for name in functions.keys():
        print(f'the model called the function {name} with parameters {functions[name]}')
        print(f'the result is: {manager.use_plugin(name, functions[name])}')
    print(f'bot: {response}')
