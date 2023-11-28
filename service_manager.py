from accelerate.utils.megatron_lm import initialize
from chat_manager import Chat_manager
from flask import Flask, request, jsonify
from model import LLM_model


app = Flask(__name__)
service_manager = None

class Service_manager:
    def __init__(self, model: LLM_model) -> None:
        self.parameters = {}
        self.model = model
        self.chat = Chat_manager()

    def start_services(self, port:int, debug:bool=False) -> None:
        app.run(debug=debug, port=port)

    def add_parameters(self, plugin_name:str, **parameters):
        self.parameters[plugin_name] = parameters

    def query_usr(self, query:str, parse_llm:bool) -> str:
        if parse_llm:
            query = self.model.query(query)
        print(self.chat.get_console_message(query))
        response = input()
        print(self.chat.get_user_message(response))
        return response

    def query_model(self, query:str, plugin_name:str) -> str:
        response = self.model.query(query)
        print(self.chat.get_console_message(f"the plugin {plugin_name} queried the model with the query:\n{query}"))
        print(self.chat.get_console_message(f"the model response was:\n {response}"))
        return response


def initialize_service_manager(model:LLM_model):
    global service_manager 
    service_manager = Service_manager(model)

@app.route('/process_json', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Add a new field called 'app'
        data['app'] = 'YourAppName'

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("query_usr", methods=['POST'])
def query_usr():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'query and parse_llm parameters required'}), 400
    response = service_manager.query_usr(data['query'], data['parse_llm'])
    return jsonify({'response': response})
    
