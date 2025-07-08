import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sys import argv



def main():

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    user_prompt = argv[1]
    if user_prompt == "":
        print("No prompt")
        os._exit(1)



    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    content_response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages
    )

    meta_data = content_response.usage_metadata
    print(content_response.text)
    if "--verbose" in argv:
        if meta_data == None:
            print("no response")
        else:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {meta_data.prompt_token_count}")
            print(f"Response tokens: {meta_data.candidates_token_count}")


if __name__ == "__main__":
    main()
