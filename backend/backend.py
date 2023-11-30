from managers.configuration_manager import Configuration_manager
from flask import Flask, request, jsonify
from managers.plugin_manager import Plugin_manager
from models.query_model import Query_model
from models.ollama_models.mistral import Mistral_compiler
from langchain.docstore.document import Document
from managers.service_manager import Service_manager
import logging

app = Flask(__name__)
# model_name = "mistralai/Mistral-7B-v0.1"
model_name = 'gpt2'
configuration = Configuration_manager.load_config()
plugin_manager = Plugin_manager(configuration['plugins'], configuration['port'])
model = Query_model(model_name)
document = Document(page_content=str(plugin_manager))
model.add_documents(document)
model = Mistral_compiler(str(plugin_manager))
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
service_manager = Service_manager(model, plugin_manager)

storage = {}
parameters = {}

@app.route("/query", methods=['POST'])
def query():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'query and parse_llm parameters required'}), 400
    response, plugins = service_manager.query_model(data['query'], data['plugin'])
    for plugin_name in plugins.keys():
        parameters[plugin_name] = plugin_manager.parse_plugin(plugin_name, plugins[plugin_name])
        # service_manager.call_plugin(plugin_name)
    print(plugins)        
    return jsonify({'response': response})

@app.route("/storage/<plugin_name>/<element>", methods=['GET'])
def get_data(plugin_name, element):
    element = int(element)
    if element >= len(storage[plugin_name]) or len(storage[plugin_name]) == 0:
        return jsonify([])
    return jsonify(storage[plugin_name][element])

@app.route("/call_plugin/<plugin_name>", methods=['POST'])
def call_plugin(plugin_name):
    parameters = request.get_json()['parameters']
    parameters[plugin_name] = parameters
    service_manager.call_plugin(plugin_name)
    return '', 200

@app.route("/save_data/<plugin_name>", methods=['POST'])
def save_data(plugin_name):
    if not plugin_name in storage:
        storage[plugin_name] = []
    storage[plugin_name].append(request.get_json()['data'])
    return '', 200
 
@app.route("/parameters/<plugin_name>", methods=['GET'])
def get_parameters(plugin_name):
    return jsonify(parameters[plugin_name])
    
app.run(debug=True, port=configuration['port'])
