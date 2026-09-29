import json
import os
import pytest


@pytest.fixture(scope="session")
def test_config():
    """Încarcă datele din fișierul test_env.json global."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "test_env.json")

    with open(json_path, "r") as file:
        return json.load(file)


@pytest.fixture(scope="session")
def base_url(test_config):
    return test_config.get("base_url")


@pytest.fixture(scope="session")
def base_url_api(test_config):
    return test_config.get("base_url_api")
