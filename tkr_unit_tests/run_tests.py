import os
import subprocess
import http.server
import socketserver
import logging
from typing import List
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command: str, cwd: str) -> None:
    """
    Run a command using subprocess.
    
    :param command: Command to run
    :param cwd: Current working directory for the command
    """
    logging.info(f"Running command: {command}")
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")

def start_server(port: int, root_dir: str) -> None:
    """
    Start a simple HTTP server to host view_reports.html.
    
    :param port: Port number for the server
    :param root_dir: Root directory for the server
    """
    logging.info(f"Starting HTTP server on port {port} with root directory {root_dir}...")
    os.chdir(root_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logging.info(f"Server started at http://localhost:{port}")
        httpd.serve_forever()

def main(port: int, project_dir: str, test_dir: str) -> None:
    """
    Main function to run the script.
    
    :param port: Port number for the server
    :param project_dir: Root directory of the project
    :param test_dir: Name of the test directory
    """
    project_path = Path(project_dir).resolve()
    test_path = project_path / test_dir
    reports_path = test_path / "_reports"
    allure_results_path = reports_path / "allure-results"
    allure_report_path = reports_path / "allure-report"
    coverage_report_path = reports_path / "coverage"
    
    # Create the necessary directories if they don't exist
    os.makedirs(allure_results_path, exist_ok=True)
    os.makedirs(coverage_report_path, exist_ok=True)
    
    commands = [
        f"pytest {test_path} --alluredir={allure_results_path} --cov={project_path} --cov-report=html:{coverage_report_path}",
        f"allure generate {allure_results_path} --clean -o {allure_report_path}",
    ]
    
    for command in commands:
        run_command(command, str(project_path))
    
    start_server(port, str(reports_path))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests and start a server to view reports.")
    parser.add_argument("--port", type=int, default=8000, help="Port number for the server (default: 8000)")
    parser.add_argument("--project-dir", required=True, help="Root directory of the project")
    parser.add_argument("--test-dir", default="_tests", help="Name of the test directory (default: _tests)")
    args = parser.parse_args()
    
    main(args.port, args.project_dir, args.test_dir)

# python run_tests.py --project-dir /Users/tucker/tkrSearxngRoot/tkr_searxng --test-dir _tests --port 9000