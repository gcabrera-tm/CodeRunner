# CodeRunner

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Configuration](#configuration)  
6. [Usage](#usage)  
7. [Output](#output)  
8. [UML Diagram Generation](#uml-diagram-generation)
9. [License](#license)  

---

### Overview
CodeRunner is an internal automation tool designed to streamline Python code quality checks and architecture visualization. It leverages **Pylint** to analyse code health, summarise linting issues, and exports detailed reports into an Excel workbook. For object-oriented designs, CodeRunner uses **Pyreverse** to generate UML class diagrams in DOT format, which can be visualised via Graphviz.

---

### Features
- **Recursive File Discovery**: Automatically finds all `.py` files within a project directory.  
- **Pylint Integration**: Runs full linting pass, extracts overall scores, flag counts, and detailed messages.  
- **Statement Analysis**: Captures per-file "statements analysed" metrics.  
- **Excel Reporting**: Generates a multi-sheet Excel report (`.xlsx`) with summary, messages, and statement counts.  
- **UML Diagram Export**: Produces DOT files representing class hierarchies and relationships.  
- **Progress Indicators**: Uses `tqdm` for progress bars during long-running operations.  

---

### Prerequisites
- **Python** 3.7 or later  
- **pip** package manager
- **pylint**
- **pyreverse** is included with pylint
- **tqdm**
- **pandas**
- **openpyxl**

---

### Installation
1. Clone or copy the CodeRunner repository into your local environment.
2. Navigate to the root of the project directory:
```bash
cd path/to/CodeRunner
```
3. Ensure all prerequisites are installed (see Prerequisites).

---

### Configuration
You can customise output directories and filenames by editing the constants at the top of the script:
| Constant              | Default Value                    | Description                              |
|-----------------------|---------------------------------|------------------------------------------|
| `OUTPUT_DIR`           | `"Pylint Output"`                | Directory where Excel reports are stored.|
| `PYREVERSE_OUTPUT_DIR` | `"Pyreverse Output"`             | Directory for DOT UML files.             |
| `OUTPUT_FILE`          | `"pylint_analysis_summary.xlsx"`| Name of the Excel summary report.       |
> **Tip:** Ensure you have write permissions in the target directories.

---
### Usage
Run the CodeRunner script from the project root:

```bash
python code_runner.py
```
The script performs the following steps:

- Creates (or ensures) output directories exist.
- Discovers all Python files in the current directory tree.
- Executes Pylint on each file, capturing scores and messages.
- Collects "statements analysed" data via a secondary Pylint pass.
- Writes a consolidated Excel report with three sheets:
  - **Summary:** File-level scores and flag counts.
  - **All Messages:** Detailed lint warning/error messages.
  - **Statements Analyzed:** Per-file statement metrics.
- Generates UML diagrams in DOT format using Pyreverse.
- Prints execution time and a reminder link for visualising DOT files.

---
### Output
After execution, you will find:

```matlab
Pylint Output/
├── pylint_analysis_summary.xlsx > generated output from code_runner.py
└── analysis_code_review.xlsx > already existing file for analysis of the result above. Need to refresh the path file in PowerQuery to connect with pylint_analysis_summary.xlsx

Pyreverse Output/
├── classes_ProjectName.dot > generated UML diagram as a .dot file
├── packages_ProjectName.dot
└── pyreverse_output.log
```

Open the .xlsx file with Excel to explore lint results. Use an online Graphviz viewer (e.g., GraphvizOnline) to visualise .dot UML diagrams.

---

### UML Diagram Generation

CodeRunner runs:
```bash
pyreverse --all-ancestors -o dot -d "Pyreverse Output" -p <ProjectName> .
```
- --all-ancestors: Includes inherited classes beyond immediate parents.
- -o dot: Outputs in DOT graph description language.
- -d: Specifies the output directory.
- -p: Names the project in the diagram files.

---

### License

This project is licensed under the MIT License. See the LICENSE file for details.

---

#### Happy linting & diagramming!


