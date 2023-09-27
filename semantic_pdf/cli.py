import click
from cleaning import clean_text
from extraction import extract_text_for_sempdfs
from hashing import hash_files
from mydatabase import SemPdf, load_data, write_data
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
            inverted_map[hash_val]: SemPdf = SemPdf(hash_val)

        inverted_map[hash_val].paths.append(path)
    return inverted_map


@click.command()
@click.option(
    "-s", "--skip", is_flag=True, default=False, help="Don't search for new pdfs."
)
def cli(skip):
    if skip:
        print("Loading data from file...")
        sempdfs = load_data()
    else:
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

        print("Writing data to file...")
        write_data(inverted_hashes_map.values())
        sempdfs = inverted_hashes_map.values()

    print("Cleaning text...")
    for sempdf in sempdfs:
        sempdf.cleaned_text = clean_text(sempdf.text)

    write_data(sempdfs)


if __name__ == "__main__":
    cli()
