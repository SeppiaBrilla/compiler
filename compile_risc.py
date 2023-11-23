import sys
import subprocess

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 compile_risc.py program_name file_name")
        return
    
    program_name = sys.argv[1]
    file_name = sys.argv[2]
    subprocess.run(['riscv64-unknown-elf-gcc', '-O3', '-o', program_name, file_name])

if __name__ == "__main__":
    main()
