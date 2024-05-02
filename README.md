## Install
1. git clone http://github.com/tuckertucker/tkr_unit_tests.git
2. cd tkr_unit_tests
3. pip install .
    > update (if required): data/tests_skip.txt

## Setup
1. Create_structure: 
- walks the main directory looking for py files
- Creates empty files with test_ appended to the found files
    > this is where you'll write your tests
- skips empty directories, items listed in .gitignore, items in data/tests_skip.txt
- Creates a _tests directory that includes a _reports subdirectory with an index.html file

2. python tkr_unit_tests.install_allure_cli
    > after the tests are run the index.html will show the Allure and Coverage reports

## Write your Tests
1. Write your tests in the appropriate files

## Start Testing
1. python tkr_unit_tests.run_tests

## Package Structure
```
tkr_unit_tests/
│   ├── tkr_unit_tests/
│   ├── data/
│   │   ├── index.html
│   │   ├── pytest.ini
│   │   └── tests_skip.txt
│   ├── install_allure_cli.py
│   ├── pytest.ini
│   ├── run_tests.py
│   ├── create.py
│   └── create_structure.py
├── README.md <-- you are here
└── setup.py
```


To call the `examples.py` script from the command line, you can use the following command:

```
python -m tkr_unit_tests.examples [arguments]
```

Replace `[arguments]` with the appropriate command-line arguments based on your requirements. Here are some examples:


1. To create the test directory structure:
   ```
   python -m tkr_unit_tests.examples --create-structure
   ```

   You can also specify a custom test directory:
   ```
   python -m tkr_unit_tests.examples --create-structure --test-dir custom_tests
   ```

2. To run the unit tests:
   ```
   python -m tkr_unit_tests.examples --run-tests
   ```

   You can also specify a custom test directory and report directory:
   ```
   python -m tkr_unit_tests.examples --run-tests --test-dir custom_tests --report-dir custom_reports
   ```
3. To install Allure commandline:
   ```
   python -m tkr_unit_tests.examples --install-allure
   ```

4. To combine multiple actions:
   ```
   python -m tkr_unit_tests.examples --install-allure --create-structure 
   ```

   This command will install Allure commandline, create the test directory structure. 

Note: The `-m` flag tells Python to run the specified module as a script. In this case, it runs the `examples.py` script located in the `tkr_unit_tests` package.