import json
import os


def load_test_data():
    """Resolves the absolute path to the data directory and loads the JSON test data file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    json_path = os.path.join(project_root, "data", "test_data.json")

    with open(json_path, "r", encoding="utf-8") as data_file:
        return json.load(data_file)
