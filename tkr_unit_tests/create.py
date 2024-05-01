import os
from tkr_unit_tests.create_structure import create_test_structure

# Set the path to the test directory
test_dir = "_tests"

# Set the path to the .gitignore file (optional)
gitignore_path = ".gitignore"

# Set the path to the tests_skip.txt file (optional)
tests_skip_path = "data/tests_skip.txt"

# Create the test structure
create_test_structure(test_dir, gitignore_path, tests_skip_path)
