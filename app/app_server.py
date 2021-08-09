import configparser
import logging.config
import os
from api import app_endpoint
import utility

logging.config.fileConfig('config/logging.ini')

logger = logging.getLogger("app_server")

DEFAULT_CONFIG_FILE = 'config/app_server.ini'


def main():
    logger.info('Started')
    config = configparser.ConfigParser()

    if os.path.isfile(DEFAULT_CONFIG_FILE):
        config.read(DEFAULT_CONFIG_FILE)
        hostname = config.get('DEFAULT', 'HOST')
        port = config.get('DEFAULT', 'PORT')
        client_config = config.get('DEFAULT', 'CLIENT_CONFIG')

        if hostname and port and client_config:
            app_endpoint.run_app(hostname, port, client_config)
        else:
            logger.error("Hostname or Port or Config File Not found.")
            utility.appthrows()
    else:
        logger.error("Config File Not found:" + DEFAULT_CONFIG_FILE)
        utility.appthrows()


if __name__ == '__main__':
    main()
