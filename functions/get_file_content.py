import os
from config import MAX_CHARS
from functions.check_path import in_working_dir
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    target_path = os.path.join(working_directory, file_path)
    target_path_abs = os.path.abspath(target_path)
    if not in_working_dir(working_directory, target_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.isfile(target_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path_abs, "r") as file:
            file_content_str = file.read(MAX_CHARS)
            if len(file_content_str) == MAX_CHARS:
                file_content_str += f'...File "{file_path}" truncated at 10000 characters'
        return file_content_str
    except Exception as e:
        return f"Error getting file content: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content of the specified file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to pull content from, relative to working directory. The files are truncated at 10000 characters. Returns an error if it's not a file.",
            ),
        },
    ),
)
