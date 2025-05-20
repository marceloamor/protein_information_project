# Protein Information Project - Installation Guide

## Prerequisites

- Python 3.9 or higher (Python 3.12 recommended)
- pip or Poetry package manager

## Option 1: Installation with Poetry (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd protein_information_project
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install the dependencies using the helper script**:
   ```bash
   chmod +x install_dependencies.sh
   ./install_dependencies.sh
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

5. **Verify installation**:
   ```bash
   python run_test.py
   ```

6. **Run the application**:
   ```bash
   ./run.py
   ```

## Option 2: Installation with pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd protein_information_project
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python run_test.py
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

## Data Files

Ensure the data files are present in the `data/` directory:
- protein_nodes.parquet
- go_term_nodes.parquet
- edges.parquet
- protein_id_records.parquet

## Troubleshooting

### Common Issues:

1. **DuckDB Installation Issues**:
   - If you're having trouble installing DuckDB, try:
     ```bash
     pip install --force-reinstall duckdb
     ```

2. **PyArrow Compatibility**:
   - If you encounter PyArrow compatibility issues, try:
     ```bash
     pip uninstall pyarrow
     pip install pyarrow==14.0.1
     ```

3. **Poetry Environment Issues**:
   - If Poetry cannot resolve dependencies, try:
     ```bash
     poetry update
     ```

4. **WSL-specific Issues**:
   - Some dependencies may require additional system packages on WSL:
     ```bash
     sudo apt-get update
     sudo apt-get install build-essential libssl-dev libbz2-dev libffi-dev
     ```

### Missing Data Files:

If the data files are missing from the `data/` directory, you need to:
1. Download the required parquet files
2. Place them in the `data/` directory
3. Ensure the file names match those expected by the application

## Running the Application

### Basic Usage:

```bash
# With Poetry (recommended)
poetry shell
./run.py

# Without Poetry
python run.py
```

### Advanced Options:

```bash
# Run on a different port
./run.py --port 8080

# Run in debug mode
./run.py --debug

# Set custom log level
./run.py --log-level DEBUG

# Combine options
./run.py --port 8080 --debug --log-level DEBUG
```

### Accessing the Application:

Once the application is running, open your web browser and navigate to:
- `http://localhost:8050` (or the port you specified)

## Testing the DataLoader:

To verify that the DataLoader is working correctly:

```bash
# Run the test script
python run_test.py
```

This will attempt to load the data files and perform some basic queries to ensure everything is working as expected. 