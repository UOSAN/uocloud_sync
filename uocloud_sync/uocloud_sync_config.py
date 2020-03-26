import configparser


APP_NAME = 'uocloud_sync'


class UOCloudSyncConfig:
    """
    Read config from file named uocloud_sync.cfg
    """
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read([f'{APP_NAME}.cfg'])

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
