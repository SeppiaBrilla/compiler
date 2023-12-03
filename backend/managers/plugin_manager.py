from subprocess import Popen, PIPE
import logging

class Plugin_manager:
    def __init__(self, plugin_list:list[dict], port:int) -> None:
        self.plugins = {}
        self.port = port

        for plugin in plugin_list:
            self.plugins[plugin['name']] = plugin
            logging.debug(f'discovered plugin {plugin["name"]}')
    
    def use_plugin(self, plugin_name:str):
        command = [self.plugins[plugin_name]['plugin_location'], str(self.port)]
        if "interpreter" in self.plugins[plugin_name]:
            command = [self.plugins[plugin_name]["interpreter"]] + command
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        out, err = process.communicate()

        print(out, err)
        if err != "":
            return err
        return out
    
    def parse_plugin(self, plugin_name, parameters):
        parameter_names = self.plugins[plugin_name]['parameters'].split(' ')
        print(parameters, parameter_names)
        return {parameter_names[i]: parameters[i] for i in range(len(parameters))}
            
    def on(self, plugin_name):
        on = self.plugins[plugin_name]['on'].copy()
        for key in on.keys():
            on[key] = on[key].split(' ')

        return on

    def __str__(self) -> str:
        return 'available functions:\n-' + '\n-'.join([self.__get_plugin_str(self.plugins[key]) for key in self.plugins.keys()])

    def __get_plugin_str(self, plugin) -> str:
        return f'''{plugin["name"]}:
    description: {plugin["description"]}. 
    Usage example: ```{plugin["name"]}({','.join(plugin["parameters"].split(' ')) if len(plugin["parameters"]) > 0 else ""})```
'''
