import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read file contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}



def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        MAX_CHARS = 10000
        if valid_target_file is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file, "r") as openfile:
                cut_text = openfile.read(10000)
                if openfile.read(1):
                    cut_text += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return cut_text
    except Exception as e:
        return f"Error: {e}"
    
    
    
    
    

