import os
import json

class Configuration_manager:
    @staticmethod
    def load_config():
        config_file = 'config.json'
        home_config_file = '~/.config/llm_compiler/config.json'
        config = None
        if os.path.exists(home_config_file):
            f = open(home_config_file, 'r')
            config = f.read()
            f.close()
        if os.path.exists(config_file):
            f = open(config_file, 'r')
            config = f.read()
            f.close()
        if config is None:
            raise Exception('no configuration file found')
        return json.loads(config)


