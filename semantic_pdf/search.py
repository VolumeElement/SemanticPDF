import os

from utils import config


def search_pdf_files():
    """
    Search for all PDF files in the specified directory in the Config object.

    Args:
    - config (Config): A Config object containing the directory to search.

    Returns:
    - list: A list of paths to the found PDF files.
    """
    pdf_files = []

    # Check if the specified directory exists
    if not os.path.exists(config.pdf_search_path):
        print(f"Error: Directory {config.pdf_search_path} does not exist.")
        return []

    # Walk through the directory
    for dirpath, _, filenames in os.walk(config.pdf_search_path):
        for filename in filenames:
            if filename.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(dirpath, filename))

    return pdf_files
