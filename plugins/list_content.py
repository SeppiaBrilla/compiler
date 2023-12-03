import sys
from subprocess import Popen, PIPE
from comunication import LLM_comunincation

def main():
    port = sys.argv[1]
    com = LLM_comunincation(int(port))
    try:
        parameters = com.get_parameters('folder-content')
        folder = parameters['folder']
        process = Popen(['ls',  '-l', folder], stdout=PIPE, stderr=PIPE, text=True)
        res, err = process.communicate()
        if err != "":
            com.save_data('folder-content', {'error' : err}, 'error')
        else:
            com.save_data('folder-content', {'success' : res}, 'success')

    except Exception as e:
        com.save_data('folder-content', {'error' : str(e)}, 'error')
if __name__ == "__main__":
    main()


