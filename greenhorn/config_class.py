import os
import json
import toml
import pathlib
import configparser


class Config:
    '''
    Stores config file details.
    '''
    supported_formats = ('env', 'ini', 'json', 'toml')

    def __init__(self, use_env: bool = False) -> None:
        '''
        Sets either environment as file format attribute
        or default file format and file path attributes.
        '''
        if use_env == True:
            self.format = 'env'
        else:
            self.format = 'json'
            self.path = f'config.{self.format}'

    def __init__(self, path: str) -> None:
        '''
        Sets custom file format and path attributes.
        '''
        self.path = path
        self.format = pathlib.Path(path).suffix.replace('.', '')
        if self.format not in self.supported_formats:
            raise Exception(f'File format {self.format} is not supported.')

    def load(self) -> None:
        '''
        Sets attributes according to config file details.
        '''
        if self.format == 'env':
            for idx, value in enumerate(os.environ):
                setattr(self, idx, value)
        elif (self.format == 'ini'):
            config = configparser.ConfigParser()
            config.read(self.path)
            data = {section: dict(config.items(section)) for section in config.sections()}
            for idx, value in enumerate(data):
                setattr(self, idx, value)
        else:
            with open(self.path, 'r') as fin:
                if (self.format == 'json'):
                    data = json.load(fin)
                elif (self.format == 'toml'):
                    data = toml.load(fin)
                for name, value in data.items():
                    setattr(self, name, value)

    def reload(self) -> None:
        '''
        Deletes attributes according to config file details.
        '''
        if self.format == 'env':
            for idx in range(os.environ):
                delattr(self, idx)
        elif (self.format == 'ini'):
            config = configparser.ConfigParser()
            config.read(self.path)
            data = {section: dict(config.items(section)) for section in config.sections()}
            for idx in range(data):
                delattr(self, idx)
        else:
            with open(self.path, 'r') as fin:
                if (self.format == 'json'):
                    data = json.load(fin)
                elif (self.format == 'toml'):
                    data = toml.load(fin)
                for name, _ in data.items():
                    delattr(self, name)

    def reload_attr(self, attr_name: str) -> None:
        '''
        Resets specific attribute according to config file details.
        '''
        if self.format == 'env':
            setattr(self, attr_name, os.environ[attr_name])
        elif (self.format == 'ini'):
            config = configparser.ConfigParser()
            config.read(self.path)
            data = {section: dict(config.items(section)) for section in config.sections()}
            setattr(self, attr_name, data[attr_name])
        else:
            with open(self.path, 'r') as fin:
                if (self.format == 'json'):
                    data = json.load(fin)
                elif (self.format == 'toml'):
                    data = toml.load(fin)
                setattr(self, attr_name, data[attr_name])


if __name__ == '__main__':
    config = Config('../pyproject.toml')
    config.load()
    config.reload()
    config.reload_attr('build-system')
