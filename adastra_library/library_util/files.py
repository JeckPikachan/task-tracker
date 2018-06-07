import os


def create_file_if_not_exists(path, filename):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(os.path.dirname(path) + '/' + filename, 'a').close()
