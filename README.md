# tkr_unit_tests

## Install
1. git clone http://github.com/tuckertucker/tkr_unit_tests.git
2. cd tkr_unit_tests
3. pip install .
    > update (if required): data/tests_skip.txt

## Setup
1. Create the test structure:
   ```
   python -m tkr_unit_tests.create --project-dir /path/to/your/project
   ```
   This command will:
   - Walk the main directory looking for .py files
   - Create empty test files with `test_` appended to the found files
     > This is where you'll write your tests
   - Skip empty directories, items listed in .gitignore, items in data/tests_skip.txt
   - Create a `_tests` directory that includes a `_reports` subdirectory with an index.html file

2. Install Allure commandline:
   ```
   python -m tkr_unit_tests.install_allure_cli
   ```
   > After the tests are run, the index.html will show the Allure and Coverage reports

## Write your Tests
1. Write your tests in the appropriate files created in the `_tests` directory

## Start Testing
1. Run the tests:
   ```
   python -m tkr_unit_tests.run_tests
   ```

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

## Command Line Usage

To call the `create.py` and `run_tests.py` scripts from the command line, you can use the following commands:

1. To create the test directory structure:
   ```
   python -m tkr_unit_tests.create --project-dir /path/to/your/project
   ```

   You can also specify a custom test directory:
   ```
   python -m tkr_unit_tests.create --project-dir /path/to/your/project --test-dir custom_tests
   ```

2. To run the unit tests:
   ```
   python -m tkr_unit_tests.run_tests
   ```

   You can also specify a custom test directory and report directory:
   ```
   python -m tkr_unit_tests.run_tests --test-dir custom_tests --report-dir custom_reports
   ```

3. To install Allure commandline:
   ```
   python -m tkr_unit_tests.install_allure_cli
   ```

Note: The `-m` flag tells Python to run the specified module as a script. In this case, it runs the `create.py` and `run_tests.py` scripts located in the `tkr_unit_tests` package.
