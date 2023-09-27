import json
import os

from utils import config


def load_data(filename):
    with open(os.path.join(config.database_path, filename), "r") as f:
        data = json.load(f)


def write_data(filename, data):
    with open(os.path.join(config.database_path, filename), "w") as f:
        json.dump(data, f)
