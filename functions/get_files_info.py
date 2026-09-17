import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}





def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            ltdr = os.listdir(target_dir)
            for ld in ltdr:
                branch_path = os.path.join(target_dir, ld)
                file_size = os.path.getsize(branch_path)
                file_name = os.path.basename(branch_path)
                if_dir = os.path.isdir(branch_path)
                print(f"- {file_name}: file_size={file_size}, is_dir={if_dir}")

        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error {e}"
    
