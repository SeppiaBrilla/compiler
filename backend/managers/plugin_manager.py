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
        process = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        out, err = process.communicate()
        if err != "":
            return err
        return out
    
    def parse_plugin(self, plugin_name, parameters):
        parameter_names = self.plugins[plugin_name]['parameters'].split(' ')
        return {parameter_names[i]: parameters[i] for i in range(len(parameters))}
            

    def __str__(self) -> str:
        return 'available functions:\n-' + '\n-'.join([self.__get_plugin_str(self.plugins[key]) for key in self.plugins.keys()])

    def __get_plugin_str(self, plugin) -> str:
        return f'''{plugin["description"]}. Usage =
    {plugin["name"]}:{plugin["parameters"] if len(plugin["parameters"]) > 0 else "(NONE)"}
'''
