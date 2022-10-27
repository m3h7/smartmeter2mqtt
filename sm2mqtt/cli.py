#!/usr/bin/env python3

import os
import sys
import argparse
import logging
from time import sleep
from .config import load_config, ConfigError
from .sm2mqtt import Smartmeter2Mqtt
from . import __version__

LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'


def main():
    argp = argparse.ArgumentParser(description='MQTT to InfluxDB')
    argp.add_argument('-c', '--config', help='path to configuration file (YAML format)', required=True)
    argp.add_argument('-D', '--debug', help='print debug messages', action='store_true')
    argp.add_argument('-o', '--output', help='output log messages to file')
    argp.add_argument('-t', '--test', help='test parse config', action='store_true')
    args = argp.parse_args()

    log_file = None
    if args.output:
        log_file = args.output

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format=LOG_FORMAT, filename=log_file)

    try:
        config = load_config(open(args.config, 'r'))

        if args.test:
            print("The configuration file seems ok")
            return

        try:
            s2m = Smartmeter2Mqtt(config)
            s2m.run()
        except KeyboardInterrupt:
            return
        except Exception as e:
            raise

    except Exception as e:
        if args.debug or os.getenv('DEBUG', False):
            raise e
        if isinstance(e, ConfigError):
            print('Config error:')
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
