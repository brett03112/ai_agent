# Building an AI Agent with Python and Google

These are my notes on building an AI agent using Python and Google services from the course "Building an AI Agent" 
on boot.dev.

## Gemini

Large Language Models (LLMs) are the fancy-schmancy AI technology that have been making all the waves in the AI world recently. Products like:

- ChatGPT
- Claude
- Cursor
- Google Gemini
  
... are all powered by LLMs. For the purposes of this course, you can think of an LLM as a smart text generator. It works just like ChatGPT: you give it a prompt, and it gives you back some text that it believes answers your prompt. We're going to use Google's Gemini API to power our agent in this course. It's reasonably smart, but more importantly for us, it has a free tier.

### Tokens

You can think of tokens as the currency of LLMs. They are the way that LLMs measure how much text they have to process. Tokens are roughly 4 characters for most models. It's important when working with LLM APIs to understand how many tokens you're using.

We'll be staying well within the free tier limits of the Gemini API, but we'll still monitor our token usage!

**Be aware that all API calls, including those made during local testing, consume tokens from your free tier quota. If you exhaust your quota, you may need to wait for it to reset (typically 24 hours) to continue the lesson. Regenerating your API key will not reset your quota.**

### Assignment

1. [ ] Create an account on Google AI Studio.
2. [ ] Create an API key.
3. [ ] Store your API key in an environment variable named `GEMINI_API_KEY`.
4. [ ] Add the `.env` file to your `.gitignore` file.
5. [ ] Update the `main.py` file. When the program starts, load the environment variables from the `.env` file
    using the `dotenv` library.

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    ```
6. [ ] Import `genai` library and use the API key to create a new instance of the Gemini client.

    ```python
    from google import genai

    client = genai.Client(api_key=api_key)
    ```
7. [ ] Use the `client.models.generate_content()` method to get a response from the `gemini-2.0-flash-001` model! You'll need to use two named parameters:

   - model: The model name: gemini-2.0-flash-001 (this one has a generous free tier)
   - contents: The prompt to send to the model (a string). For now, hardcode this prompt:
  
    "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    **The generate_content method returns a GenerateContentResponse object. Print the .text property of the response to see the model's answer.**

    **If everything is working as intended, you should be able to run your code and see the model's response in your terminal!**
8. [ ] In addition to printing the text response, print the number of tokens consumed by the interaction in this format:
   
   ```text
   Prompt tokens: X
   Response tokens: Y
   ```

   The response has a `.usage_metadata` property that has both:

   - a prompt_token_count property (tokens in the prompt)
   - a candidates_token_count property (tokens in the response)
   - Run and submit the CLI tests.