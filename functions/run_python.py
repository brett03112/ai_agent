import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    """Executes a Python file within the working directory and returns the output from the interpreter.

    Args:
        working_directory (str): The path to the working directory.
        file_path (str): The path to the Python file to execute, relative to the working directory.
        args (list, optional): A list of arguments to pass to the Python file. Defaults to None.

    Returns:
        str: The output from the Python interpreter or an error message.
    """
    # Ensure the file is within the working directory
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        # Execute the Python file using subprocess
        commands = ["python", abs_file_path]
        
        # Append any additional arguments
        if args:
            commands.extend(args)
        # Run the command and capture output
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )
        output = []
        # Collect stdout and stderr
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        # Include return code if non-zero
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        # Return the combined output
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

# Define the function schema for integration with Google GenAI
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
