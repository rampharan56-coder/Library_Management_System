import json
import os


class JSONStorage:
    def __init__(self, data_dir="data"):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_path = os.path.join(project_root, data_dir)
        os.makedirs(self.base_path, exist_ok=True)

    def get_file_path(self, filename):
        return os.path.join(self.base_path, filename)

    def load(self, filename, default_data=None):
        if default_data is None:
            default_data = []

        file_path = self.get_file_path(filename)
        if not os.path.exists(file_path):
            self.save(filename, default_data)
            return default_data

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content == "":
                    return default_data
                return json.loads(content)
        except Exception:
            return default_data

    def save(self, filename, data):
        file_path = self.get_file_path(filename)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
