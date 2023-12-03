from managers.configuration_manager import Configuration_manager
from flask import Flask, request, jsonify
from managers.plugin_manager import Plugin_manager
from models.ollama_models.mistral import Mistral_compiler
from managers.service_manager import Service_manager
import logging

app = Flask(__name__)
configuration = Configuration_manager.load_config()
plugin_manager = Plugin_manager(configuration['plugins'], configuration['port'])
model = Mistral_compiler(str(plugin_manager))
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
service_manager = Service_manager(model, plugin_manager)

storage = {}
parameters = {}

@app.route("/query", methods=['POST'])
def query():
    data = request.get_json()
    plugins_data = {}
    if data is None:
        return jsonify({'error': 'query and parse_llm parameters required'}), 400
    response, plugins = service_manager.query_model(data['query'], data['plugin'])
    print(plugins)
    print(response)
    for plugin_name in plugins.keys():
        for i in range(len(plugins[plugin_name])):
            if not plugin_name in plugins_data:
                plugins_data[plugin_name] = []
            plugins_data[plugin_name].append(use_plugin(plugin_name, i, plugins))   

        print(plugins_data[plugin_name])
    interaction = 'user:\n' + data['query'] + '\nAI:\n' + response
    print(interaction)
    service_manager.add_to_history(interaction)
    return jsonify({'response': response, 'data':plugins_data})

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
    storage[plugin_name].append(request.get_json())
    return '', 200
 
@app.route("/parameters/<plugin_name>", methods=['GET'])
def get_parameters(plugin_name):
    return jsonify(parameters[plugin_name])

def use_plugin(plugin_name, plugin_index, plugins):
    parameters[plugin_name] = plugin_manager.parse_plugin(plugin_name, plugins[plugin_name][plugin_index])
    plugin_manager.use_plugin(plugin_name)
    if plugin_name in storage:
        plugin_data = storage[plugin_name][-1]
        on = plugin_manager.on(plugin_name)
        return {'msg':plugin_post_actions(plugin_data, plugin_name, on), 'outcome':plugin_data['outcome']}
        
def plugin_post_actions(plugin_data, plugin_name, post_actions):
    action = post_actions[plugin_data['outcome']][0]
    parameter = post_actions[plugin_data['outcome']][1]
    if action == 'print':
        return plugin_data['data'][parameter]
    elif action == 'query':
        msg = service_manager.query_model(
            f'The function {plugin_name} returned the following error:```{plugin_data["data"][parameter]}```.\n Could you explain it?',
            plugin_name)[0]
        return f'The function {plugin_name} returned the following error:\n```\n{plugin_data["data"][parameter]}```.\n the model possible explaination for it is:\n{msg}'

app.run(debug=True, port=configuration['port'])
