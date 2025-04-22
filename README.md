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
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Overview
CodeRunner is an internal automation tool designed to streamline Python code quality checks and architecture visualization. It leverages **Pylint** to analyse code health, summarise linting issues, and exports detailed reports into an Excel workbook. For object-oriented designs, CodeRunner uses **Pyreverse** to generate UML class diagrams in DOT format, which can be visualised via Graphviz.

---

## Features
- **Recursive File Discovery**: Automatically finds all `.py` files within a project directory.  
- **Pylint Integration**: Runs full linting pass, extracts overall scores, flag counts, and detailed messages.  
- **Statement Analysis**: Captures per-file "statements analysed" metrics.  
- **Excel Reporting**: Generates a multi-sheet Excel report (`.xlsx`) with summary, messages, and statement counts.  
- **UML Diagram Export**: Produces DOT files representing class hierarchies and relationships.  
- **Progress Indicators**: Uses `tqdm` for progress bars during long-running operations.  

---

## Prerequisites
- **Python** 3.7 or later  
- **pip** package manager
- **pylint**
- **pyreverse** is included with pylint
- **tqdm**
- **pandas**
- **openpyxl**

## Installation
1. Clone or copy the CodeRunner repository into your local environment.
2. Navigate to the root of the project directory:
```bash
cd path/to/CodeRunner


