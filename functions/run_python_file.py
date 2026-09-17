import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory and returns its output.",
        "parameters": {
            "type": "object",
                        "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}




def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        sub = subprocess.run(command, cwd=working_directory ,text=True, capture_output=True, timeout=30)
        output = []
        if sub.returncode != 0:
            output.append(f"Process exited with code {sub.returncode}")
        if sub.stdout == "" and sub.stderr == "":
            output.append("No output produced")
        else:
            if sub.stdout != "":
                output.append(f"STDOUT: {sub.stdout}")
            if sub.stderr != "":
                output.append(f"STDERR: {sub.stderr}")
        put = "\n".join(output)
        return put
    except Exception as e:
        return f"Error: {e}"
    
