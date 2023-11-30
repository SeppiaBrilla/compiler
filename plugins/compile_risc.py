import sys
import subprocess
from compilerConnect import LLM_comunincation

def main():
    
    port = sys.argv[0]
    com = LLM_comunincation(int(port))
    parameters = com.get_parameters('compile')
    com.save_data('compile',  parameters)
    print('from compile!', parameters)
    # subprocess.run(['riscv64-unknown-elf-gcc', '-O3', '-o', program_name, file_name])

if __name__ == "__main__":
    main()


