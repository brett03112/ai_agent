import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import schema_write_file
from functions.get_files_info import schema_get_file_content
from functions.get_files_info import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    # If the prompt is not provided via command line arguments, print an error message and exit
    if not sys.argv[1:]:
        raise Exception("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    # Define the available functions for the model to use
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)
    # Make the API call to generate content with the provided prompt and available functions
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1:],
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    # If the --verbose flag is provided, the output should include:
    # 1. The user's prompt ("User prompt: {user_prompt}")
    # 2. The number of prompt tokens on the each iteration ("Prompt tokens: {prompt_tokens}")
    # 3. The number of response tokens on each iteration ("Response tokens: {response_tokens}")
    if "--verbose" in sys.argv:
        user_prompt = " ".join(arg for arg in sys.argv[1:] if arg != "--verbose")
        print(f"User prompt: {user_prompt}\n")
        print(response.text)
        if response.usage_metadata:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print("Usage metadata not available")
            
    else:
        # Check if the response contains function calls
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        print(f"Calling function: {function_call.name}({function_call.args})")
                    elif hasattr(part, 'text') and part.text:
                        print(part.text)
        else:
            # Fallback to the original text output
            print(response.text)
    
        # if response.usage_metadata:
        #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # else:
        #     print("Usage metadata not available")

if __name__ == "__main__":
    main()
