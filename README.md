## Install
1. git clone http://github.com/tuckertucker/tkr_unit_tests.git
2. cd tkr_unit_tests
    > update (if required): data/tests_skip.txt

## Setup
1. python tkr_unit_tests.create_structure: 
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