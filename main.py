import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import schema_write_file
from functions.get_files_info import schema_get_file_content
from functions.get_files_info import schema_run_python_file
from functions.get_files_info import call_function

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
    # Check if --verbose flag is provided
    verbose = "--verbose" in sys.argv
    user_prompt = " ".join(arg for arg in sys.argv[1:] if arg != "--verbose")
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    
    # Make the initial API call to generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[user_prompt],
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    # Check if the response contains function calls
    if (response.candidates and response.candidates[0].content and 
        response.candidates[0].content.parts):
        
        has_function_calls = False
        function_results = []
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call:
                has_function_calls = True
                # Call the function and get result
                function_result = call_function(part.function_call, verbose)
                function_results.append(function_result)
        
        if has_function_calls:
            # Create a new conversation with the function results
            conversation = [
                user_prompt,
                response.candidates[0].content
            ] + function_results
            
            # Get the final response after function calls
            final_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=conversation,
                config=types.GenerateContentConfig(system_instruction=system_prompt),
            )
            response = final_response
    
    # Print final response and usage metadata
    if verbose:
        print(response.text)
        if response.usage_metadata:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print("Usage metadata not available")
    else:
        print(response.text)
    
        # if response.usage_metadata:
        #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # else:
        #     print("Usage metadata not available")

if __name__ == "__main__":
    main()
