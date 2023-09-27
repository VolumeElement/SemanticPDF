from hashing import hash_files
from search import search_pdf_files

file_list = search_pdf_files()
file_hashes = hash_files(file_list)
print(file_hashes)
