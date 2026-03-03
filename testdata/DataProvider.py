import json

data_file = open('test_data.json')
global_data = json.load(data_file)


class DataProvider:
    def __init__(self) -> None:
        self.data = global_data

    def get_api_key(self) -> str:
        return self.data.get("api-key")
