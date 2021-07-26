import json


class Services:
    __services = {
        'yolov3': None
    }

    @staticmethod
    def get(name):
        """
        Get configuration variable
        :param name: the configuration value to get
        """
        return Services.__services[name]

    @staticmethod
    def set(name, value):
        Services.__services[name] = value

    @staticmethod
    def load_from_file(filename):
        with open(filename, "r") as f:
            data = json.load(f)

        for key in data:
            Services.set(key, data[key])
