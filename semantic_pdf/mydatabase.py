from dataclasses import dataclass


@dataclass
class SemPdf:
    hash: str
    text: str
    paths: list[str]

    def __init__(self, hash):
        self.paths = []
        self.text = None
        self.hash = hash
