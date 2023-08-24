import os


def get_filename_and_extension(filename: str) -> tuple[str, str]:
    filename, file_ext = os.path.splitext(filename)
    return filename, file_ext