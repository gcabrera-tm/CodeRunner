import os
import subprocess
from tqdm import tqdm
import pandas as pd
import re
import time

# Output directories and file constants
PYLINT_OUTPUT_DIR = "Pylint Output"
PYREVERSE_OUTPUT_DIR = "Pyreverse Output"
PYLINT_OUTPUT_FILE = "pylint_output.xlsx"


def ensure_output_directory():
    """Ensure the necessary output directories exist."""
    os.makedirs(PYLINT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(PYREVERSE_OUTPUT_DIR, exist_ok=True)


def gather_python_files(directory):
    """Recursively gather Python files in the given directory."""
    files_by_folder = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                relative_folder = os.path.relpath(root, directory)
                files_by_folder.setdefault(relative_folder, []).append(file)
    return files_by_folder


def run_pylint_and_generate_report(file_list):
    """Run pylint on the provided files and generate a summary."""
    analysis_results = []
    file_messages = {}
    statements_analyzed = []

    for file_path in tqdm(file_list, desc="Running Pylint", unit="file"):
        try:
            # Run pylint analysis
            result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
            stdout_lines = result.stdout.splitlines()
            score_line = next((line for line in stdout_lines if "Your code has been rated" in line), None)
            score = float(re.search(r'at (\d+\.\d+)/10', score_line).group(1)) if score_line else None
            messages = [
                line.strip()
                for line in stdout_lines
                if line.strip() and not line.startswith(('Your code has been rated', 'Module'))
            ]
            final_folder = os.path.basename(os.path.dirname(file_path))
            analysis_results.append({
                'File': os.path.basename(file_path),
                'Path': final_folder,
                'Flags': len(messages),
                'Score': score,
            })
            file_messages[file_path] = messages

            # Generate pylint report for statements analyzed
            result = subprocess.run(['pylint', '--disable=all', '-ry', '-d RP0401', file_path], capture_output=True, text=True)
            report_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            statement_line = next((line for line in report_lines if "statements analysed" in line), None)
            if statement_line:
                statements_analyzed.append({'File': os.path.basename(file_path), 'Statement': statement_line})
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return analysis_results, file_messages, statements_analyzed


def run_pyreverse(directory):
    """Run Pyreverse on the directory to generate UML diagrams."""
    try:
        output_log = os.path.join(PYREVERSE_OUTPUT_DIR, "pyreverse_output.log")

        with open(output_log, "w") as log_file:
            with tqdm(total=1, desc="Running Pyreverse", unit="task") as pbar:
                subprocess.run(
                    ["pyreverse", "--all-ancestors", "-o", "dot", "-d", PYREVERSE_OUTPUT_DIR, "-p", os.path.basename(directory), "."],
                    cwd=directory, check=True,
                    stdout=log_file, stderr=log_file
                )
                pbar.update(1)

    except Exception as e:
        print(f"Error running Pyreverse: {e}")


def save_analysis_to_excel(analysis_results, file_messages, statements_analyzed):
    """Save Pylint analysis results to an Excel file."""
    summary_df = pd.DataFrame(analysis_results)
    summary_df = summary_df[['File', 'Path', 'Flags', 'Score']]
    output_path = os.path.join(PYLINT_OUTPUT_DIR, PYLINT_OUTPUT_FILE)

    all_messages = []
    for file_path, messages in file_messages.items():
        for message in messages:
            all_messages.append({'File': os.path.basename(file_path), 'Message': message})
    all_messages_df = pd.DataFrame(all_messages)
    statements_df = pd.DataFrame(statements_analyzed)

    with pd.ExcelWriter(output_path) as writer:
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        all_messages_df.to_excel(writer, sheet_name='All Messages', index=False)
        statements_df.to_excel(writer, sheet_name='Statements Analyzed', index=False)


def main():
    """
    Main function that drives the analysis pipeline:
    - Ensures directories exist
    - Gathers Python files
    - Runs Pylint and saves report
    - Runs Pyreverse and saves UML files
    - Saves everything to Excel
    """
    start_time = time.time()
    ensure_output_directory()

    directory = os.getcwd()
    files_by_folder = gather_python_files(directory)
    file_list = [os.path.join(directory, folder, file) for folder, files in files_by_folder.items() for file in files]

    pylint_results, pylint_messages, statements_analyzed = run_pylint_and_generate_report(file_list)
    save_analysis_to_excel(pylint_results, pylint_messages, statements_analyzed)
    run_pyreverse(directory)

    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Process completed in {int(minutes)} minutes and {seconds:.2f} seconds.")
    print(f"Use this link to generate UML: https://dreampuf.github.io/GraphvizOnline/")


if __name__ == "__main__":
    main()

