# IS 601 - Module 3: Assignment-Interactive Calculator Command-Line
References https://github.com/kaw393939/module3_is601 for portions of logic and attempts to adhere to the same formatting, with some personal tweaks.

This assignment was to create an interactive calculator for the IS-601 class that creates a calculator that is interactable through a Read-Eval-Print Loop (REPL) interface. Considerations were made towards input validation and error handling.  
Additionally, I added the ability to have a running sum to be more in line with how a traditional handheld calculator functions.  
The instructor repository contained folders such as the .vscode and .coveragerc files; these were ommitted through the .gitignore for my submission, as I felt that these were personal files and wouldn't be commited to a repository under normal circumstances.  

For testing, code coverage and unit testing was done through the pytest and coverage modules. Github Actions was configured to test merges to main, and to fail if 100% code coverage is not achieved.  

## To Run
```bash
python main.py
```

## To Test
```bash
coverage run -m pytest && coverage report
```
or
```bash
pytest
```

If you are coding on a remote server like I do, a `.coveragrc` file may be needed to allow for the data file to be generated correctly.  
Example .coveragrc file:
```
[run]
data_file = /tmp/.coverage
```