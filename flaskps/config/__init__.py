from os import getenv
from importlib import import_module


def get_config():
    """Función para recuperar la configuración dependiendo del entorno"""
    try:
        # Entorno por defecto si no se especifica otro, development
        mode = getenv('FLASK_ENV', 'development')
        module = __name__ + "." + mode
        config = import_module(module)
        config.ENV = mode
        config.SQLALCHEMY_TRACK_MODIFICATIONS = False
        return config
    except ModuleNotFoundError:
        print(f"Configuration {module} is missing")
        exit(1)


Config = get_config()
