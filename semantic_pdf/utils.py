from dataclasses import dataclass

import yaml


@dataclass
class Config:
    pdf_search_path: str
    database_path: str

    def __init__(self):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.pdf_search_path = config["pdf_search_path"]
        self.database_path = config["database_path"]


config = Config()


@dataclass
class Constants:
    BUF_SIZE: int = 65536
    INVERTED_HASHES_MAP_FILENAME: str = "inverted_hashes_map.json"
    WORD2VEC_MODEL_FILENAME: str = "word2vec.model"


constants = Constants()
