import os
import yaml
from io import IOBase
from schema import Schema, And, Optional, SchemaError


class ConfigError(Exception):
    pass


def port_range(port):
    return 0 <= port <= 65535


schema = Schema({
    'mqtt': {
        'host': And(str, len),
        'port': And(int, port_range),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len),
        Optional('cafile'): os.path.exists,
        Optional('certfile'): os.path.exists,
        Optional('keyfile'): os.path.exists,
        Optional('topic_prefix'): And(str, len)
    },
    'smartmeter': {
        'device': And(str, len)
    }
})


def load_config(config_file):
    if isinstance(config_file, IOBase):
        config = yaml.safe_load(config_file)
        try:
            config = schema.validate(config)
        except SchemaError as e:
            raise ConfigError(str(e))
    elif config_file is None:
        config = {}
    else:
        raise ConfigError('Unknown type config_file')

    return config
