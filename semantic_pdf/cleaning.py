import itertools
import ssl
import string

import nltk
from nltk.corpus import stopwords
from utils import config

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")


def clean_text(text):
    """
    Clean the text by converting to lowercase, removing punctuation, numbers, and stopwords.

    Args:
    - text (str): Original text to be cleaned.

    Returns:
    - list: Cleaned text as a list of words.
    """
    # Convert to lowercase and remove punctuation and numbers
    text = text.lower().translate(
        str.maketrans("", "", string.punctuation + string.digits)
    )

    # Split into words
    words = text.split()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))

    # Add math specific stopwords
    alphabet = string.ascii_lowercase
    stop_words.update(set(["".join(i) for i in itertools.product(alphabet, repeat=3)]))
    words = [word for word in words if word not in stop_words]

    return words


def clean_sempdfs(sempdfs):
    for sempdf in sempdfs:
        sempdf.cleaned_text = clean_text(sempdf.text)
    return sempdfs
