from hashing import hash_files
from search import search_pdf_files


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
            inverted_map[hash_val] = []
        inverted_map[hash_val].append(path)
    return inverted_map


file_list = search_pdf_files()
file_hashes = hash_files(file_list)
inverted_hashes_map = invert_mapping(file_hashes)
