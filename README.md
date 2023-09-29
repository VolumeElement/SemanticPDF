# SemPDF Search Engine README 

SemPDF is a tool for searching through a collection of PDFs based on semantic meaning using Word2Vec embeddings. 

## Features:

- Indexes all PDFs found in a specified directory.
- Converts PDFs to text, cleans the text, and computes Word2Vec embeddings for search.
- Provides a command-line interface for user queries, returning the most semantically similar PDFs.

## Dependencies:

To run the script, install the requirements.txt

`pip install -r requirements.txt`

## Configuration

Copy `config.yaml.template` to `config.yaml` and fill in configuration variables

```yaml
pdf_search_path: path to pdfs
database_path: path to database directory 
```


## Commands:

### 1. Database Initialization and Operations:

``` python cli.py database [--reinit] [--stats] ```

Options:
- `--reinit`: Reinitialize the database.
- `--stats`: Print database statistics such as number of documents, unique hashes, unique paths, and duplicates.

### 2. Search:

Search for the top N closest articles based on a given string:

``` python cli.py search <QUERY> [--num N] [--skip] [--reinit] ```

Arguments:
- `QUERY`: The search query string.

Options:
- `--num N`: Number of results to return (default is 3).
- `--skip`: If specified, won't search for new PDFs.
- `--reinit`: Reinitialize the database before searching.

## Code Overview:

1. **Database Initialization (`init` function)**:
    - Loads previous database if it exists.
    - Searches for new PDF files.
    - Hashes files to track duplicates and changes.
    - Extracts text from new PDFs.
    - Cleans the extracted text.
    - Trains a Word2Vec model on the cleaned text.
    - Computes Word2Vec embeddings for each document.

2. **Search (`search` function)**:
    - Cleans and embeds the user's query using the trained Word2Vec model.
    - Computes cosine similarity between the query and every document in the database.
    - Returns the top N most similar documents.

## Getting Started:

1. Ensure you have all the required dependencies installed.
2. Place the script and its associated modules in the directory containing your PDFs or modify the `config` module to point to your PDF directory.
3. Initialize the database:
    ``` python cli.py database --reinit ```
4. Run a search query:
    ``` python cli.py search "Your search query here" ```

This will return the top 3 (default) most semantically similar PDFs. Adjust with `--num N` to return a different number of results.

---

Happy searching! 