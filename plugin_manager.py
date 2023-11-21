from plugin import Plugin


class Plugin_manager:
    def __init__(self, plugin_list:list[dict]) -> None:
        self.plugins = {}

        for plugin in plugin_list:
            self.plugins[plugin['name']] = Plugin(plugin['name'], plugin['parameters'], plugin['description'])
            print(f'discovered plugin {plugin["name"]}')
    
    def use_plugin(self, plugin_name:str, args:list[str]):
        return self.plugins[plugin_name](args)

    def __str__(self) -> str:
        return 'available plugins:\n-' + '\n-'.join([str(self.plugins[key]) for key in self.plugins.keys()])
