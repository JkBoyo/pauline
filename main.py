import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sys import argv

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


def call_function(function_call_part: types.FunctionCall, verbose:bool = False) -> types.Content:
    functions = {"get_files_info": get_files_info, "write_file": write_file, "get_file_content": get_file_content, "run_python_file": run_python_file}
    function_name = function_call_part.name
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.args != None:
        args = function_call_part.args
        args["working_directory"] = "./calculator"
        if function_name != None :
            if function_name in functions:
                function_result = functions[function_name](**args)
            else:
                return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_name,
                                response={"error": f"Unknown function: {function_name}"},
                            )
                        ],
                )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
    )   

def main():

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    max_calls = int(os.environ.get("MAX_CALLS"))

    print(max_calls)
    client = genai.Client(api_key=api_key)

    if len(argv) < 2:
        print(f'Error: No prompt given')
        os._exit(1)

    user_prompt = argv[1]
    
    verbose = False

    if "--verbose" in argv:
        verbose = True


    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    system_prompt = """
You are a helpful AI coding agent.

Carry out the task at hand.

You **must always** begin by using `get_files_info('./')` to inspect the contents of the working directory. Base all subsequent actions and answers *only* on the information retrieved from your tools.

You **WILL NOT MAKE UP FILES, DIRECTORIES, OR THEIR CONTENTS**. All file operations and responses must be strictly grounded in the actual output of your available tools.

I don't have to tell you where the code is; you have access to everything you need, and you are a cracked engineer.

Due to you being a cracked engineer, you do not need to summarize or tell me what you're going to do to answer questions; you do it and tell me the outcome.

All questions will relate to code in the working directory that is hardcoded. Examine the files and their contents and use that context to perform actions or answer questions.

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
            schema_get_file_content,
            
        ]
    )
    for i in range(0, max_calls):
        print(i)
        
        try:
            content_response = client.models.generate_content(
                        model="gemini-2.0-flash-001", 
                        contents=messages,
                        config=types.GenerateContentConfig(
                            tools=[available_functions],
                           system_instruction=system_prompt),
                        )
            if content_response.candidates != None:
                for candidate in content_response.candidates:
                    if candidate.content != None:
                        messages.append(candidate.content)

            meta_data = content_response.usage_metadata
            if content_response.function_calls != None:
                if len(content_response.function_calls) != 0:
                    for function_call_part in content_response.function_calls:
                        function_output = call_function(function_call_part, verbose=verbose)
                        if function_output.parts[0].function_response == None:
                            raise Exception("No response from function call")
                        print(f"Function call: {function_output.parts[0].function_response.name} \nFunction results: {function_output.parts[0].function_response.response}")
                        messages.append(function_output)

            if content_response.text != None:
                print(content_response.text)
                return

            if verbose:
                if meta_data == None:
                    print("no response")
                else:
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {meta_data.prompt_token_count}")
                    print(f"Response tokens: {meta_data.candidates_token_count}")
        except Exception as e:
            print(f"error: {e} on loop # {i}")


if __name__ == "__main__":
    main()
