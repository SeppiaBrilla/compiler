from os import get_terminal_size
from sys import stdout

write = stdout.write

class Chat_manager:
    def run(self):
        width = get_terminal_size(0)[0]
        message_width = (width // 2) - 10

        while True:
            msg = input()
            write("\033[F")
            print(self.print_user_message(msg, message_width, width))
            response = self.get_response(msg)
            print(self.print_console_message(response, message_width, width))

    def print_user_message(self, msg, message_width, total_width):
        left_pad = total_width - message_width
        left_pad_str = ''.join([' ' for _ in range(left_pad)])
        lines = msg.split('\n')
        true_lines = []
        for line in lines:
            true_lines += self.split_string(line, message_width)
        for i in range(len(true_lines)):
            line_length = len(true_lines[i])
            true_lines[i] = left_pad_str + true_lines[i] + ''.join(' ' for _ in range(line_length))
        return '\n'.join(true_lines)
    
    def split_string(self, string, width):
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

    def get_response(self, msg):
        return ' '.join(['msg' for _ in range(len(msg.split(' ')))])

    def print_console_message(self, msg, message_width, total_widht):
        right_pad = total_widht - message_width
        right_pad_str = ''.join([' ' for _ in range(right_pad)])
        lines = msg.split('\n')
        true_lines = []
        for line in lines:
            true_lines += self.split_string(line, message_width)
        for i in range(len(true_lines)):
            line_length = len(true_lines[i])
            true_lines[i] = true_lines[i] + ''.join(' ' for _ in range(line_length)) + right_pad_str
        return '\n'.join(true_lines)

