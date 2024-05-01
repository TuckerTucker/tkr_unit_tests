import argparse
from tkr_unit_tests.create_structure import create_structure
from tkr_unit_tests.run_tests import main as run_tests
from tkr_unit_tests.install_allure_cli import install_allure_cli

def main():
    parser = argparse.ArgumentParser(description="TKR Unit Tests Examples")
    parser.add_argument("--run-tests", action="store_true", help="Run the unit tests")
    parser.add_argument("--test-dir", default="_tests", help="Specify the test directory (default: _tests)")
    parser.add_argument("--report-dir", default="_tests/_reports", help="Specify the report directory (default: _tests/_reports)")
    parser.add_argument("--install-allure", action="store_true", help="Install Allure commandline")
    parser.add_argument("--create-structure", action="store_true", help="Create the directory structure")
    args = parser.parse_args()

    if args.install_allure:
        install_allure_cli()

    if args.create_structure:
        create_structure(args.test_dir)

    if args.run_tests:
        run_tests()

if __name__ == "__main__":
    main()