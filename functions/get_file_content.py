import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """Reads the content of a file within the working directory.

    Args:
        working_directory (str): The path to the working directory.
        file_path (str): The path to the file whose content should be read, relative to the working directory.

    Returns:
        str: The content of the file or an error message.
    """
    # Ensure the file path is within the working directory
    abs_working_dir = os.path.abspath(working_directory)
    # Get the absolute file path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Check if the absolute file path starts with the absolute working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        # Read and return the file content, truncated to MAX_CHARS
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

# Define the function schema for integration with Google GenAI
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)