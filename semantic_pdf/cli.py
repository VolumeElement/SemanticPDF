import json
import os

import click
import numpy as np
from cleaning import clean_sempdfs, clean_text
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
    "-r", "--reinit", is_flag=True, default=False, help="Reinitialize the database."
)
@click.option(
    "-s", "--stats", is_flag=True, default=False, help="Print database statistics."
)
def database(reinit, stats):
    if reinit:
        init(reinit)
        return

    if stats:
        sempdfs = load_data()
        if not sempdfs:
            print("No data found.")
            return

        _stats = {
            "Number of Documents": len(sempdfs),
            "Number of Unique Hashes": len(set([sempdf.hash for sempdf in sempdfs])),
            "Number of Unique Paths": len(
                set([path for sempdf in sempdfs for path in sempdf.paths])
            ),
            "Number of Duplicates": len(
                [sempdf for sempdf in sempdfs if len(sempdf.paths) > 1]
            ),
        }

        print(json.dumps(_stats, indent=4))


def init(reinit=False):
    """Initialize the database.

    Args:
    - reinit (bool): Whether to reinitialize the database."""

    # Load sempdfs if it exists
    _init = True
    sempdfs = []
    if not reinit and os.path.exists(
        os.path.join(config.database_path, constants.INVERTED_HASHES_MAP_FILENAME)
    ):
        _init = False

        print("Loading data from file...")
        sempdfs = load_data()

    # Search for pdf's
    print("Loading file list...")
    file_list = search_pdf_files()
    print("Hashing files...")
    file_hashes = hash_files(file_list)
    print("Inverting hashes map...")
    inverted_hashes_map = invert_mapping(file_hashes)

    # update sempdfs paths
    paths_updated = False
    for sempdf in sempdfs:
        if sempdf.paths != inverted_hashes_map[sempdf.hash].paths:
            paths_updated = True
            sempdf.paths = inverted_hashes_map[sempdf.hash].paths
    if paths_updated:
        print("Updating paths...")
        write_data(sempdfs)

    # Update sempdfs text
    delta_sempdfs = []
    negative_delta_sempdfs = []

    if _init:
        # If we are initializing, then all sempdfs are new
        delta_sempdfs = inverted_hashes_map.values()
    else:
        # What hashes are new?
        for hash_val, sempdf in inverted_hashes_map.items():
            if hash_val not in [sempdf.hash for sempdf in sempdfs]:
                delta_sempdfs.append(sempdf)

        # What hashes are no longer available?
        for sempdf in sempdfs:
            if sempdf.hash not in inverted_hashes_map:
                negative_delta_sempdfs.append(sempdf)

    if len(delta_sempdfs) + len(negative_delta_sempdfs) == 0:
        print("No new files found.")
        return

    if delta_sempdfs:
        print("Extracting text from PDFs...")
        delta_sempdfs = extract_text_for_sempdfs(delta_sempdfs)

        print("Cleaning text...")
        delta_sempdfs = clean_sempdfs(delta_sempdfs)
        sempdfs.extend(delta_sempdfs)

    if negative_delta_sempdfs:
        print("Removing old hashes...")
        # Remove hashes that are no longer available
        for sempdf in negative_delta_sempdfs:
            sempdfs.remove(sempdf)

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
@click.option(
    "-s", "--skip", is_flag=True, default=False, help="Don't search for new pdfs."
)
@click.option(
    "-r", "--reinit", is_flag=True, default=False, help="Reinitialize the database."
)
def search(query, num, skip, reinit):
    """
    Search for the top N closest articles based on a given string.

    Args:
    - query (str): Query string to search.

    Returns:
    - list[SemPdf]: Top N closest SemPdf dataclass instances.
    """

    if not skip:
        init(reinit)
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
