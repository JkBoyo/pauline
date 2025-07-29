import os
import subprocess
from functions.check_path import in_working_dir
from google.genai import types

def run_python_file(working_directory: str, file_path: str) -> str:
    full_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    if not in_working_dir(working_directory, full_path_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path_abs):
        return f'Error: File "{file_path}" not found.'
    if not full_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = subprocess.run(args=['uv', 'run', full_path_abs],
                                 timeout= 30.0,
                                 text= True,
                                 capture_output= True,
                                 cwd= working_directory)
        stdout = command.stdout
        stderr = command.stderr
        ret_code = command.returncode
        
        result_string = f'STDOUT: {stdout}, STDERR: {stderr}'
        if ret_code != 0:
            result_string += f'\nProcess exited with code {stderr}'

        print(stdout)
        if stdout == "None":
            return 'No output produced.'
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file returning output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run. If not provided, return a string saying no file provided.",
            ),
        },
    ),
)
