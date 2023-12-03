import sys
from subprocess import Popen, PIPE
from comunication import LLM_comunincation
from time import time

def main():
    port = sys.argv[1]
    com = LLM_comunincation(int(port))
    try:
        parameters = com.get_parameters('execute')
        program_name = parameters['program_name']
        program_parameters = parameters['[parameters]']
        command = [program_name] + program_parameters
        start = time()
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        res, err = process.communicate()
        execution_time = time() - start
        if err != "":
            com.save_data('execute', {'error' : err}, 'error')
        else:
            com.save_data('execute', {'success' : f'the program output was:\n{res}.\nThe exection took {execution_time}s'}, 'success')

    except Exception as e:
        com.save_data('execute', {'error' : str(e)}, 'error')
if __name__ == "__main__":
    main()

