from configparser import ConfigParser


def get_config(path: str = './program/config/appsettings.ini') -> ConfigParser:
    cfg = ConfigParser()
    cfg.read(path)
    return cfg

def update_config(cfg: ConfigParser, path: str = './program/config/appsettings.ini') -> None:
    with open(path, 'w') as file:
        cfg.write(file)
        file.close()
