import os
from pickle import dump, load

from gensim.models import Word2Vec
from mydatabase import SemPdf
from utils import config, constants

MODEL_PATH = os.path.join(config.database_path, constants.WORD2VEC_MODEL_FILENAME)


def train_word2vec(sempdfs: list[SemPdf], size=100, window=5, min_count=1, workers=4):
    """
    Train a Word2Vec model on the given sentences.

    Args:
    - sentences (list[list[str]]): Text data as list of sentences where each sentence is a list of words.
    - Other arguments are Word2Vec hyperparameters.

    Returns:
    - Word2Vec: Trained Word2Vec model.
    """
    cleaned_texts = [sempdf.cleaned_text for sempdf in sempdfs if sempdf.cleaned_text]

    model = Word2Vec(
        cleaned_texts,
        vector_size=size,
        window=window,
        min_count=min_count,
        workers=workers,
    )
    return model


def save_word2vec(model):
    """
    Save a Word2Vec model to disk.

    Args:
    - model (Word2Vec): Trained Word2Vec model.
    """
    with open(MODEL_PATH, "wb") as f:
        dump(model, f)


def load_word2vec():
    """
    Load a Word2Vec model from disk.

    Returns:
    - Word2Vec: Trained Word2Vec model.
    """
    with open(MODEL_PATH, "rb") as f:
        model = load(f)
    return model


def embed_sempdfs(sempdfs):
    """
    Iterate through each SemPdf, clean and embed the text.

    Args:
    - sempdfs (list[SemPdf]): List of SemPdf dataclass instances.

    Returns:
    - list[SemPdf]: Processed list of SemPdf dataclass instances.
    """

    for sempdf in sempdfs:
        if sempdf.cleaned_text:
            embedded_text = [
                model.wv[word].tolist()
                for word in sempdf.cleaned_text
                if word in model.wv.index_to_key
            ]
            sempdf.embedded_text = embedded_text

    return sempdfs
