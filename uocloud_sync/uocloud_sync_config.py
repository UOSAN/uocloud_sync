import configparser
import os


APP_NAME = 'uocloud_sync'


class UOCloudSyncConfig:
    """
    Read config from file named uocloud_sync.cfg
    """
    def __init__(self):
        # Get parent path of this file
        __location__ = os.path.dirname(os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))))
        self._config = configparser.ConfigParser()
        self._config.read([os.path.join(__location__, f'{APP_NAME}.cfg')])

    def get_client_id(self) -> str:
        try:
            return self._config[APP_NAME]['client_id']
        except KeyError:
            return ''

    def get_client_secret(self) -> str:
        try:
            return self._config[APP_NAME]['client_secret']
        except KeyError:
            return ''
