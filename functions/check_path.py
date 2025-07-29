import os
def in_working_dir(working_dir: str, full_path: str) -> bool:
    working_dir_abs = os.path.abspath(working_dir)
    full_path_abs = os.path.abspath(full_path)
    return full_path_abs.startswith(working_dir_abs)
