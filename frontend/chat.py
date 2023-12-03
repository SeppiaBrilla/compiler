from os import get_terminal_size
from sys import stdout

write = stdout.write

class Formatter:
    def __init__(self) -> None:
        self.width = get_terminal_size(0)[0]
        self.message_width = (self.width // 2) - 5
    
    def clear(self) -> None:
        write("\033[F")
        print(" " * self.width, end="\r")

    def get_user_message(self, msg:str) -> str:
        left_pad = self.width - self.message_width
        left_pad_str = ''.join([' ' for _ in range(left_pad - 2)])
        lines = msg.split('\n')
        true_lines = []
        for line in lines:
            true_lines += self.__split_string(line, self.message_width - 4)
        for i in range(len(true_lines)):
            line_length = len(self.string_decolor(true_lines[i]))
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
            line_length = len(self.string_decolor(true_lines[i]))
            true_lines[i] = '| ' + true_lines[i] + ''.join([' ' for _ in range(self.message_width - line_length - 4)]) + ' |' + right_pad_str
        border = f'|{"-" * (self.message_width -2)}|'
        true_lines = [border] + true_lines + [border]
        return '\n'.join(true_lines)

    def string_decolor(self, string):
        if not CEND in string:
            return string
        colors = [CBOLD, CITALIC, CURL, CBLINK, CBLINK2, CSELECTED, CBLACK, CRED, CGREEN, CYELLOW, 
                  CBLUE, CVIOLET, CBEIGE, CWHITE, CBLACKBG, CREDBG, CGREENBG, CYELLOWBG, CBLUEBG, 
                  CVIOLETBG, CBEIGEBG, CWHITEBG, CGREY, CRED2, CGREEN2, CYELLOW2, CBLUE2, CVIOLET2, 
                  CBEIGE2, CWHITE2]

        for color in colors:
            if color in string:
                string = string.replace(color, '')

        return string.replace(CEND, '')


class Color:
    def __init__(self, color) -> None:
        self.color = color

    def __call__(self, msg:str) -> str:
        return f'{self.color}{msg}{CEND}'

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'
