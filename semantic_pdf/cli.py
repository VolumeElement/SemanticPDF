import os

from embedding import extract_text_for_sempdfs
from hashing import hash_files
from mydatabase import SemPdf
from myio import load_data, write_data
from search import search_pdf_files
from utils import constants


def invert_mapping(data_list):
    """
    Invert the list to map hash values to their corresponding paths.

    Args:
    - data_list (list): A list of [path, hash] pairs.

    Returns:
    - dict: A dictionary mapping hashes to lists of paths.
    """
    inverted_map = {}
    for path, hash_val in data_list:
        if hash_val not in inverted_map:
            inverted_map[hash_val]: SemPdf = SemPdf(hash_val)

        inverted_map[hash_val].paths.append(path)
    return inverted_map


print("Loading file list...")
file_list = search_pdf_files()
print("Hashing files...")
file_hashes = hash_files(file_list)
print("Inverting hashes map...")
inverted_hashes_map = invert_mapping(file_hashes)

print("Extracting text from PDFs...")
for _, sempdf in inverted_hashes_map.items():
    print(f"Extracting {sempdf.paths[0]}")
    extract_text_for_sempdfs(sempdf)

print(inverted_hashes_map)
