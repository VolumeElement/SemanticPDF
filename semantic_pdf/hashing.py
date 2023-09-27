import hashlib


def hash_file(file_path):
    BUF_SIZE = 65536
    md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def hash_files(file_paths):
    file_hashes = []
    for file_path in file_paths:
        file_hashes.append([file_path, hash_file(file_path)])
    return file_hashes
