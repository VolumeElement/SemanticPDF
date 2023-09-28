import click
import numpy as np
from cleaning import clean_text
from embedding import embed_sempdfs, load_word2vec, save_word2vec, train_word2vec
from extraction import extract_text_for_sempdfs
from hashing import hash_files
from mydatabase import SemPdf, load_data, write_data
from search import search_pdf_files
from sklearn.metrics.pairwise import cosine_similarity
from utils import config, constants


@click.group()
def cli():
    pass


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
        print(path, hash_val)
        if hash_val not in inverted_map:
            inverted_map[hash_val]: SemPdf = SemPdf(hash=hash_val)

        if path not in inverted_map[hash_val].paths:
            inverted_map[hash_val].paths.append(path)
    return inverted_map


@cli.command()
@click.option(
    "-s", "--skip", is_flag=True, default=False, help="Don't search for new pdfs."
)
def init(skip):
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
        sempdfs = inverted_hashes_map.values()

        print("Cleaning text...")
        for sempdf in sempdfs:
            sempdf.cleaned_text = clean_text(sempdf.text)

        write_data(sempdfs)

        print("training word2vec model...")
        model = train_word2vec(sempdfs)
        print("Saving word2vec model...")
        save_word2vec(model)

    model = load_word2vec()

    print("Embedding text...")
    sempdfs = embed_sempdfs(sempdfs, model)
    write_data(sempdfs)


@cli.command()
@click.argument("query", type=str)
@click.option("-n", "--num", type=int, default=3, help="Number of results to return.")
def search(query, num):
    """
    Search for the top N closest articles based on a given string.

    Args:
    - query (str): Query string to search.

    Returns:
    - list[SemPdf]: Top N closest SemPdf dataclass instances.
    """

    import os

    if not os.path.exists(
        os.path.join(config.database_path, constants.INVERTED_HASHES_MAP_FILENAME)
    ):
        print("Please run `init` first.")
        return

    sempdfs = load_data()
    model = load_word2vec()

    # Convert the query into an embedding
    cleaned_query = SemPdf(cleaned_text=clean_text(query))
    query_embedding = embed_sempdfs([cleaned_query], model)[0].embedded_vec

    # If the cleaned query is empty or has words that are not in our Word2Vec model, return an empty list
    if not query_embedding:
        return []

    # Compute an averaged vector for each SemPdf's text
    document_embeddings = [sempdf.embedded_vec for sempdf in sempdfs]

    # Compute cosine similarities
    similarities = cosine_similarity([query_embedding], document_embeddings)[0]

    # Get indices of top N articles
    search_num = min(num, len(similarities))
    top_indices = np.argsort(similarities)[-search_num:][::-1]

    # Return top N articles
    print("Top results:")
    for i in top_indices:
        print(f"{sempdfs[i].paths[0]}: {similarities[i]}")


if __name__ == "__main__":
    cli()
