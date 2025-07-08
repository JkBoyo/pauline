import os

def get_files_info(working_directory: str, directory: str= "") -> str:
    rel_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(rel_path)
    if working_directory not in abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    try:
        items_in_dir = os.listdir(abs_path)
        if directory == ".":
            dir_name = "Current"
        else:
            dir_name = directory
        files_info = f"Result for {dir_name} directory:\n"
        for item in items_in_dir:
            item_path = (os.path.join(abs_path,item))
            files_info += f"  - {item}: file size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"
        return files_info
    except Exception as e:
        return f'Error getting files info: {e}'
