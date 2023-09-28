import json
import os
from dataclasses import asdict, dataclass

from utils import config, constants


@dataclass
class SemPdf:
    hash: str
    text: str
    cleaned_text: list[str]
    paths: list[str]
    embedded_vec: list[float]

    def __init__(
        self,
        hash=None,
        text=None,
        paths=None,
        cleaned_text=None,
        embedded_vec=None,
    ):
        self.paths = paths if paths is not None else []
        self.text = text
        self.hash = hash
        self.cleaned_text = cleaned_text if cleaned_text is not None else []
        self.embedded_vec = embedded_vec if embedded_vec is not None else []


def load_data():
    """
    Load a list of SemPdf dataclass instances from a JSON file.
    Returns:
    - list[SemPdf]: List of SemPdf dataclass instances.
    """

    with open(
        os.path.join(config.database_path, constants.INVERTED_HASHES_MAP_FILENAME), "r"
    ) as file:
        data = json.load(file)

    # Convert list of dictionaries to list of dataclass instances
    sem_pdfs = [SemPdf(**item) for item in data]

    return sem_pdfs


def write_data(sem_pdfs: list[SemPdf]):
    data = [asdict(sem_pdf) for sem_pdf in sem_pdfs]

    # Serialize list of dictionaries to JSON and save to a file
    with open(
        os.path.join(config.database_path, constants.INVERTED_HASHES_MAP_FILENAME), "w"
    ) as file:
        json.dump(data, file, indent=4)
