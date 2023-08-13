from datetime import datetime
import json
import os


class JsonFileHandler:

    @staticmethod
    def load(file_path):
        data = None
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass
        return data
        
    @staticmethod
    def save(file_path, data):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f)