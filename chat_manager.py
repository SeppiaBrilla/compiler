from os import get_terminal_size
from sys import stdout

write = stdout.write

class Chat_manager:
    def __init__(self) -> None:
        self.width = get_terminal_size(0)[0]
        self.message_width = (self.width // 2) - 5
    
    def clear(self) -> None:
        write("\033[F")

    def get_user_message(self, msg:str) -> str:
        left_pad = self.width - self.message_width
        left_pad_str = ''.join([' ' for _ in range(left_pad - 2)])
        lines = msg.split('\n')
        true_lines = []
        for line in lines:
            true_lines += self.__split_string(line, self.message_width - 4)
        for i in range(len(true_lines)):
            line_length = len(true_lines[i])
            true_lines[i] = left_pad_str + '| ' + true_lines[i] + ''.join([' ' for _ in range(self.message_width - line_length - 4)]) + ' |'
        border = f'|{"-" * (self.message_width -2)}|'
        true_lines = [left_pad_str + border] + true_lines + [left_pad_str + border]
        return '\n'.join(true_lines)
    
    def __split_string(self, string:str, width:int):
        _words = string.split(' ')
        substrings = ['']
        words = []
        for word in _words:
            if len(word) > width:
                for i in range(0, len(word), width):
                    words.append(word[i:i + width])
            else:
                words.append(word)
        for word in words:
            if len(substrings[-1] + ' ' + word) > width:
                substrings.append(' ')
            substrings[-1] += ' ' + word
        return substrings


    def get_console_message(self, msg:str) -> str:
        right_pad = self.width - self.message_width
        right_pad_str = ''.join([' ' for _ in range(right_pad - 2)])
        lines = msg.split('\n')
        true_lines = []
        for line in lines:
            true_lines += self.__split_string(line, self.message_width - 4)
        for i in range(len(true_lines)):
            line_length = len(true_lines[i])
            true_lines[i] = '| ' + true_lines[i] + ''.join([' ' for _ in range(self.message_width - line_length - 4)]) + ' |' + right_pad_str
        border = f'|{"-" * (self.message_width -2)}|'
        true_lines = [border] + true_lines + [border]
        return '\n'.join(true_lines)

