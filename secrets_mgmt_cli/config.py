import os
import pathlib
import configparser


class ConfigHandler:
    def __init__(self, project_name):
        p = pathlib.Path.home()
        self.home_path = p
        self.config_path = p / ".config" / project_name
        self.config_file_path = self.config_path / "config"

        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file_path):
            self.config.read(self.config_file_path)
            print("-- config file exists --")
            print(self.print_configs())

    def export_configs(self):
        """
        export configs as environment variables
        this doesn't work because of the following reasons:
            https://stackoverflow.com/questions/51886448/python-export-env-variable-in-linux-shell
        """
        for key, val in self.config.defaults().items():
            if key is not None:
                os.environ[key.upper()] = val

    def print_configs(self):
        for key, val in self.config.defaults().items():
            if key is not None:
                print(key.upper(), (20 - int(len(key))) * " ", val)

    def write_config_file(self):
        # rewrite config file
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)

    def create_file_and_dir(self):
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.config_file_path.touch()

    def config_file_input(self, config_dict: dict, section: str = "DEFAULT"):
        """
        example:
        config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '8',}
        """
        self.config[section] = config_dict

    def write_config_file_from_dict(self, config_dict: dict):
        self.config_file_input(config_dict)
        self.write_config_file()
