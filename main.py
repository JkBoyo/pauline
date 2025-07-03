import os
from dotenv import load_dotenv
from google import genai
from sys import argv



def main():
    print("Hello from pauline!")

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    prompt = argv[1:]
    if prompt == []:
        print("No prompt")
        os._exit(1)

    content_response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=prompt
    )

    meta_data = content_response.usage_metadata
    print(content_response.text)
    if meta_data == None:
        print("no response")
    else:
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")


if __name__ == "__main__":
    main()
