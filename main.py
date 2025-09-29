import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"

def main():
    # If the prompt is not provided via command line arguments, print an error message and exit
    if not sys.argv[1:]:
        raise Exception("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1:],
        config=types.GenerateContentConfig(system_instruction=system_prompt),
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
        print(response.text)
    
        # if response.usage_metadata:
        #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        # else:
        #     print("Usage metadata not available")

if __name__ == "__main__":
    main()
