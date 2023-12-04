import sys
from subprocess import Popen, PIPE
from comunication import LLM_comunincation

def main():
    port = sys.argv[1]
    com = LLM_comunincation(int(port))
    try:
        parameters = com.get_parameters('compile')
        program_name = parameters['program_name']
        file_names = parameters['[file_names]']
        optimization_level = parameters['optimization']
        lto = parameters['lto']
        command = ['gcc', f'-{optimization_level}'] 
        if lto == 'true':
            command += ['-flto']

        command += [ '-o', program_name] + file_names
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        _, err = process.communicate()
        print(command)
        if err == '':
            com.save_data('compile', {'success' : 'compiled successfully'}, 'success')
        else:
            com.save_data('compile', {'error' : err}, 'error')
    except Exception as e:
        com.save_data('compile', {'error' : str(e)}, 'error')
if __name__ == "__main__":
    main()
