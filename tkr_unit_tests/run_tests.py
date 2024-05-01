import os
import subprocess
import http.server
import socketserver
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command: str) -> None:
    """
    Run a command using subprocess.
    
    :param command: Command to run
    """
    logging.info(f"Running command: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
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

def main(port: int) -> None:
    """
    Main function to run the script.
    
    :param port: Port number for the server
    """
    commands = [
        "pytest",
        "allure generate _tests/_reports/allure-results --clean -o _tests/_reports/allure-report",
    ]
    
    for command in commands:
        run_command(command)
    
    start_server(port, "_tests/_reports/")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests and start a server to view reports.")
    parser.add_argument("--port", type=int, default=8000, help="Port number for the server (default: 8000)")
    args = parser.parse_args()
    
    main(args.port)