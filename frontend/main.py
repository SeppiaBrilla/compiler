from managers.chat_manager import Chat_manager
from compilerConnect import LLM_comunincation
from sys import argv


chat_manager = Chat_manager()


def main(port:int):
    com = LLM_comunincation(port)

    while True:
        msg = input('query the llm: ')
        if 'exit()' in msg:
            break
        chat_manager.clear()
        print(chat_manager.get_user_message(msg))
        print()
        response = com.query_llm(msg, 'fe')
        print(chat_manager.get_console_message(response))
        print()

if __name__ == '__main__':
    main(int(argv[1]))
