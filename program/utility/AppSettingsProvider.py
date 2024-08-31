from configparser import ConfigParser

class AppSettingsProvider():
    settings: ConfigParser
    __path: str
    
    def __init__(self, path: str = './program/config/appsettings.ini') -> None:
        self.__path = path
        self.settings = self.get_config()

    def get_config(self) -> ConfigParser:
        cfg = ConfigParser()
        cfg.read(self.__path)
        return cfg

    def update_config(self) -> None:
        with open(self.__path, 'w') as file:
            self.settings.write(file)
            file.close()
