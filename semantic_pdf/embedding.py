def train_word2vec(sentences, size=100, window=5, min_count=1, workers=4):
    """
    Train a Word2Vec model on the given sentences.

    Args:
    - sentences (list[list[str]]): Text data as list of sentences where each sentence is a list of words.
    - Other arguments are Word2Vec hyperparameters.

    Returns:
    - Word2Vec: Trained Word2Vec model.
    """
    model = Word2Vec(
        sentences, vector_size=size, window=window, min_count=min_count, workers=workers
    )
    return model


def process_sempdfs(sempdfs):
    """
    Iterate through each SemPdf, clean and embed the text.

    Args:
    - sempdfs (list[SemPdf]): List of SemPdf dataclass instances.

    Returns:
    - list[SemPdf]: Processed list of SemPdf dataclass instances.
    """
    cleaned_texts = [clean_text(sempdf.text) for sempdf in sempdfs if sempdf.text]

    # Train Word2Vec model on cleaned text
    model = train_word2vec(cleaned_texts)

    for sempdf in sempdfs:
        if sempdf.text:
            cleaned_text = clean_text(sempdf.text)
            embedded_text = [
                model.wv[word].tolist()
                for word in cleaned_text
                if word in model.wv.index_to_key
            ]
            sempdf.text = (
                embedded_text  # Update the text field with embedded representation
            )

    return sempdfs
