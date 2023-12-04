from re import findall
import sys
from subprocess import Popen, PIPE
from comunication import LLM_comunincation

def main():
    port = sys.argv[1]
    com = LLM_comunincation(int(port))
    try:
        parameters = com.get_parameters('execute')
        program_name = parameters['program_name']
        program_parameters = parameters['[parameters]']
        command = ['perf', 'stat', program_name] + program_parameters
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        _, err = process.communicate()
        if not "Performance counter stats for " in err:
            com.save_data('execute', {'error' : err}, 'error')
            return
        string = err.split(f"Performance counter stats for ")[1]
        instructions = 0
        time = 0
        for line in string.split('\n'):
            if 'instructions' in line and not 'not counted' in line:
                instructions = int(findall('      ([0-9]*)      ',line.replace(',',''))[0])
            if 'time elapsed' in line:
                time = float(findall('      ([0-9 .]*) ',line)[0])
        print(instructions, time)
        com.save_data('execute', {'success' : f'the program execution took {instructions} instructions and the execution time was {time} seconds'}, 'success')
    except Exception as e:
       com.save_data('execute', {'error' : str(e)}, 'error')
   
if __name__ == "__main__":
    main()

