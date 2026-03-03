import configparser

gloabal_config = configparser.ConfigParser()
gloabal_config.sections()
gloabal_config.read('test_config.ini')


class ConfigProvider:
    def __init__(self) -> None:
        self.config = gloabal_config

    def get_api_url(self) -> str:
        return self.config['api'].get('base_url')

    def get_ui_url(self) -> str:
        return self.config['ui'].get('base_url')

    def get_ui_waiting_time(self) -> int:
        return self.config['ui'].get('waiting_time')
