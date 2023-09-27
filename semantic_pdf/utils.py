from dataclasses import dataclass

import yaml


@dataclass
class Config:
    pdf_search_path: str

    def __init__(self):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.pdf_search_path = config["pdf_search_path"]


config = Config()
