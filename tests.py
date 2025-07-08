from functions.get_file_content import get_file_content

def test_get_file_info():
    cases = [
        get_file_content("calculator", "main.py"),
        get_file_content("calculator", "pkg/calculator.py"),
        get_file_content("calculator", "/bin/cat")
    ]
    for case in cases:
        print(case)


test_get_file_info()
