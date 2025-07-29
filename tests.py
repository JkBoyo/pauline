from functions.run_python import run_python_file

def test_get_file_info():
    cases = [
        run_python_file("calculator", "main.py"),
        run_python_file("calculator", "tests.py"),
        run_python_file("calculator", "../main.py"), # (this should return an error)
        run_python_file("calculator", "nonexistent.py"), # (this should return an error)
    ]
    for case in cases:
        print(case)


test_get_file_info()
