import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    target_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_abs = os.path.abspath(working_directory)
    if not target_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        path = os.path.dirname(target_path_abs)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(target_path_abs, "w") as f:
            _ = f.write(content)
    except Exception as e:
        return f'Error writing file: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes changes that are desired to the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path the file to write content to, relative to the working directory. If not provided, returns an error saying no path for content.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file_path. If not provided, returns an error saying no content to write to file.",
            )
        },
    ),
)
