from chat import CRED, CVIOLET, Formatter, Color, CGREEN
from re import findall
from comunication import LLM_comunincation
from sys import argv, exit
from signal import signal, SIGINT

def exit_signal_handler(sig, frame):
    print("\nbye!")
    exit(0)

formatter = Formatter()
signal(SIGINT, exit_signal_handler)
def response_parser(response, data):
    response = response.replace("'", "")
    response = response.replace('"', '')
    functions = findall('\\`\\`\\`([a-zA-Z0-9_ \\-\\.,]*\\([a-zA-Z0-9_ /\\-\\.,\\[\\]]*\\))\\`\\`\\`',response)
    plugins_values = []
    plugins_names = []
    color_codes = {'success': Color(CGREEN), 'error': Color(CRED), 'none': Color(CVIOLET)}
    color = lambda msg, outcome: color_codes[outcome](msg) if outcome in color_codes else color_codes['none'](msg)
    for function in functions:
        split_function = function[:-1].split('(') 
        plugins_names.append(split_function[0])
        result = data[split_function[0]].pop(0)
        response = response.replace('```' + function + '```', f'[{len(plugins_names) - 1}]{color(split_function[0], result["outcome"])}')
        plugins_values.append(result['msg'])
    return response, plugins_values, plugins_names

def print_actions(plugins_names, plugins_values, response):
    if len(plugins_names) == 0:
        return
    plugins_names += ["reprint the message", "query the llm"]
    plugins_values += [response]
    possible_values = "choose an action: " + ' '.join([f"[{i}]{plugins_names[i]}" for i in range(len(plugins_names))]) + " "
    while True:
        n = -1
        while n == -1 or n > len(plugins_values):
            try:
                res = input(possible_values)
                n = int(res)
            except KeyboardInterrupt as _:
                return
            except Exception as _:
                pass
            formatter.clear()
        if n == len(plugins_values):
            return
        print(formatter.get_console_message(plugins_values[n]))


def main(port:int):
    com = LLM_comunincation(port)

    while True:
        msg = input('query the llm. If you want to exit write "exit()" or press ctrl + C: ')
        if 'exit()' in msg:
            exit_signal_handler("","")
        formatter.clear()
        print(formatter.get_user_message(msg))
        print()
        response = com.query_llm(msg, 'fe')
        data = response['data']
        ai_response = response['response']
        string_response, plugins_values, plugins_names = response_parser(ai_response, data)
        print(formatter.get_console_message(string_response))
        print()
        print_actions(plugins_names, plugins_values, string_response)
        
if __name__ == '__main__':
    main(int(argv[1]))


