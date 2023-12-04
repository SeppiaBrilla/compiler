import sys
from comunication import LLM_comunincation

def main():
    port = sys.argv[1]
    com = LLM_comunincation(int(port))
    try:
        parameters = com.get_parameters('compile-and-test')
        program_name = parameters['program_name']
        optimization_level = parameters['optimization']
        lto = parameters['lto']
        com.call_plugin('compile', parameters)
        compile_data = com.get_data('compile')['data']
        
        if 'error' in compile_data:
            com.save_data('compile-and-test', compile_data, 'error')
            return
        parameters['[parameters]'] = parameters['[execution-parameters]'] if '[execution-parameters]' in parameters else []
        print('compiled, now executing',parameters)
        com.call_plugin('execute', parameters)
        execute_data = com.get_data('execute')['data']
        print('execute data', execute_data)
        if 'error' in execute_data:
            com.save_data('compile-and-test', execute_data, 'error')
            return
        stats = f'|{program_name}|{optimization_level}|{"lto" if lto == "true" else ""}|{execute_data["success"]}|'
        com.save_data('compile-and-test', {'success': stats}, 'success')
    except Exception as e:
        com.save_data('compile-and-test', {'error' : str(e)}, 'error')
if __name__ == "__main__":
    main()
