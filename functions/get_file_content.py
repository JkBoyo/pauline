import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    target_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(target_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_path, "r") as file:
            file_content_str = file.read(MAX_CHARS)
            if len(file_content_str) == MAX_CHARS:
                file_content_str += f'...File "{file_path}" truncated at 10000 characters'
        return file_content_str
    except Exception as e:
        return f"Error getting file content: {e}"
