"""
    The directory parameter should be treated as a relative path within the working_directory. 
    Use os.path.join(working_directory, directory) to create the full path, then validate 
    it stays within the working directory boundaries.
    
    1. If the absolute path to the directory is outside the working_directory, return a string error message:
        f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    2. If the directory argument is not a directory, again, return an error string:
        f'Error: "{directory}" is not a directory'
        
    3. Build and return a string representing the contents of the directory. It should use this format:
        - README.md: file_size=1032 bytes, is_dir=False
        - src: file_size=128 bytes, is_dir=True
        - package.json: file_size=1234 bytes, is_dir=False
    
    **The exact file sizes and even the order of files may vary depending on your operating system and**
    **file system. Your output doesn't need to match the example byte-for-byte, just the overall format**

    4. If any errors are raised by the standard library functions, catch them and instead return 
    a string describing the error. Always prefix error strings with "Error:".
    
        To import from a subdirectory, use this syntax: from DIRNAME.FILENAME import FUNCTION_NAME

        Where DIRNAME is the name of the subdirectory, FILENAME is the name of the file without 
        the .py extension, and FUNCTION_NAME is the name of the function you want to import.
        
    5. We need a way to manually debug our new get_files_info function! Create a new tests.py file in the root 
    of your project. When executed directly (uv run tests.py) it should run the following function 
    calls and output the results matching the formatting below (not necessarily the exact numbers).:
    
        get_files_info("calculator", "."):
        
        Example output:
        Result for current directory:
        - main.py: file_size=719 bytes, is_dir=False
        - tests.py: file_size=1331 bytes, is_dir=False
        - pkg: file_size=44 bytes, is_dir=True
        
        get_files_info("calculator", "pkg"):
        
        Example output:
        Result for 'pkg' directory:
        - calculator.py: file_size=1721 bytes, is_dir=False
        - render.py: file_size=376 bytes, is_dir=False
        
        get_files_info("calculator", "../"):
        
        Example output:
        Result for '../' directory:
        Error: Cannot list "../" as it is outside the permitted working directory
        
    6. Run uv run tests.py, and ensure your function works as expected.
    
    **Here are some standard library functions you'll find helpful:**

        os.path.abspath(): Get an absolute path from a relative path
        os.path.join(): Join two paths together safely (handles slashes)
        .startswith(): Check if a string starts with a substring
        os.path.isdir(): Check if a path is a directory
        os.listdir(): List the contents of a directory
        os.path.getsize(): Get the size of a file
        os.path.isfile(): Check if a path is a file
        .join(): Join a list of strings together with a separator
    """
import os
import subprocess

def get_files_info(working_directory, directory="."):
    """Get information about files in a directory.

    Args:
        working_directory (str): The root directory to restrict file access.
        directory (str, optional): The directory to list files from. Defaults to ".".
    """
    try:
        # Create the full path by joining working_directory and directory
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory_abs = os.path.abspath(working_directory)

        # Check if the full path is within the working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the full path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List the contents of the directory
        items = os.listdir(full_path)
        result_lines = [f'Result for "{directory}" directory:']

        for item in items:
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            result_lines.append(f'- {item}: file_size={file_size} bytes, is_dir={is_dir}')

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {e}"


def write_file(working_directory, file_path, content):
    """Write content to a file.

    Args:
        working_directory (str): The root directory to restrict file access.
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Check if the full path is within the working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create directories if they don't exist
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the content to the file
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


def run_python_file(working_directory, file_path, args=None):
    """Run a Python file with security restrictions.

    Args:
        working_directory (str): The root directory to restrict file access.
        file_path (str): The path to the Python file to execute.
        args (list, optional): Additional arguments to pass to the Python file.
    """
    if args is None:
        args = []
        
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Check if the full path is within the working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        # Check if it's a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Prepare the command
        cmd = ['python', full_path] + args

        # Execute the Python file
        completed_process = subprocess.run(
            cmd,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Format the output
        output_lines = []
        
        if completed_process.stdout:
            output_lines.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            output_lines.append(f"STDERR:\n{completed_process.stderr}")
            
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")

        if not output_lines:
            return "No output produced."
            
        return "\n".join(output_lines)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

"""
If the file_path is outside the working_directory, return a string with an error:
f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

If the file_path is not a file, again, return an error string:
f'Error: File not found or is not a regular file: "{file_path}"'

Read the file and return its contents as a string.
I'll list some useful standard library functions in the tips section below.
If the file is longer than 10000 characters, truncate it to 10000 characters and append this message 
to the end [...File "{file_path}" truncated at 10000 characters].
Instead of hard-coding the 10000 character limit, I stored it in a config.py file.

We don't want to accidentally read a gigantic file and send all that data to the LLM... 
that's a good way to burn through our token limits.

If any errors are raised by the standard library functions, catch them and instead return a string describing the error. 
Always prefix errors with "Error:".

Create a new "lorem.txt" file in the calculator directory. Fill it with at least 20,000 characters of lorem ipsum text. 
You can generate some here.

Update your tests.py file. Remove all the calls to get_files_info, and instead test 
get_file_content("calculator", "lorem.txt"). Ensure that it truncates properly.

Remove the lorem ipsum test, and instead test the following cases:
get_file_content("calculator", "main.py")
get_file_content("calculator", "pkg/calculator.py")
get_file_content("calculator", "/bin/cat") (this should return an error string)
get_file_content("calculator", "pkg/does_not_exist.py") (this should return an error string)

TIPS:
os.path.abspath: Get an absolute path from a relative path
os.path.join: Join two paths together safely (handles slashes)
.startswith: Check if a string starts with a specific substring
os.path.isfile: Check if a path is a file
MAX_CHARS = 10000

with open(file_path, "r") as f:
    file_content_string = f.read(MAX_CHARS)
"""
def get_file_content(working_directory, file_path):
    """Get the content of a file.

    Args:
        working_directory (str): The root directory to restrict file access.
        file_path (str): The path to the file to read.
    """
    try:
        # Create the full path by joining working_directory and file_path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory_abs = os.path.abspath(working_directory)

        # Check if the full path is within the working directory
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the full path is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{full_path}"'

        # Read the file and return its contents
        with open(full_path, "r") as f:
            content = f.read()
            # Truncate content if it's too long
            if len(content) > 10000:
                content = content[:10000] + '[...File truncated at 10000 characters]'
            return content

    except Exception as e:
        return f"Error: {e}"
