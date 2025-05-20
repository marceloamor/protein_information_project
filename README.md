# Protein Information Project

A data science application for exploring protein information, including protein-protein interactions and Gene Ontology (GO) term annotations.

## Overview

This project provides a framework for loading, querying, and visualizing protein data from parquet files. It allows users to:

- Search for proteins by identifier
- Retrieve detailed information about proteins
- Explore protein-protein interactions
- Search for proteins by GO term annotation
- View functional annotations for proteins
- Visualize protein interaction networks

## Project Structure

```
protein_information_project/
│
├── data/                      # Data directory containing parquet files
│   ├── protein_nodes.parquet
│   ├── go_term_nodes.parquet
│   ├── edges.parquet
│   └── protein_id_records.parquet
│
├── src/                       # Source code
│   ├── data/                  # Data loading and processing
│   │   └── loader.py          # DataLoader class implementation
│   │
│   ├── components/            # UI components
│   │   ├── layout.py          # Layout components
│   │   ├── search.py          # Search form component
│   │   ├── protein_card.py    # Protein card display
│   │   └── go_term_card.py    # GO term card display
│   │
│   ├── pages/                 # Application pages
│   │   ├── home.py            # Home page
│   │   ├── protein_detail.py  # Protein detail page
│   │   └── about.py           # About page
│   │
│   ├── utils/                 # Utility modules
│   │   └── logging.py         # Logging configuration
│   │
│   └── app.py                 # Main Dash application
│
├── project_notes/             # Project documentation
│   ├── project_summary.txt    # Overview of the project
│   ├── data_structure.md      # Detailed description of the data model
│   ├── execution_flow.md      # Description of code execution flow
│   └── installation_guide.md  # Installation instructions
│
├── assets/                    # Static assets for Dash
├── logs/                      # Application logs
├── pyproject.toml             # Poetry dependency configuration
├── requirements.txt           # pip dependencies
├── install_dependencies.sh    # Dependency installation script
├── test_data_loader.py        # Test script for the DataLoader class
├── run_test.py                # Script to run the test
├── run.py                     # Script to run the Dash application
└── README.md                  # This file
```

## Installation

See [Installation Guide](project_notes/installation_guide.md) for detailed installation instructions.

Quick start with Poetry:

```bash
# Clone the repository
git clone <repository-url>
cd protein_information_project

# Install dependencies
chmod +x install_dependencies.sh
./install_dependencies.sh

# Activate the virtual environment
poetry shell
```

## Running the Application

Once you have installed the dependencies, you can run the application:

```bash
# Start the Dash web application
./run.py

# With custom settings
./run.py --port 8080 --debug --log-level DEBUG
```

Then open your browser and navigate to `http://localhost:8050` (or the port you specified).

## Testing

To test the DataLoader functionality:

```bash
# Run the test script
python run_test.py
```

## Data Model

The application uses four parquet files to represent a graph of proteins and GO terms:

1. **protein_nodes.parquet**: Contains protein information (27,768 rows)
2. **go_term_nodes.parquet**: Contains GO term information (9,594 rows)
3. **edges.parquet**: Contains relationships between entities (498,731 rows)
4. **protein_id_records.parquet**: Maps UUIDs to external identifiers (27,768 rows)

See [Data Structure](project_notes/data_structure.md) for more details on the data model.

## Usage Example

```python
from src.data.loader import DataLoader

# Create an instance of the DataLoader
loader = DataLoader(data_path="data")

# Search for a protein by ID
results = loader.search_protein("Protein::edb7a0a0-b7d6-5f2d-b2eb-8f91f17aa5ca")

# Get details for a protein
if results:
    protein_details = loader.get_protein_details(results[0])
    print(protein_details)

# Search for proteins by GO term
go_results = loader.search_by_go_term("GO:0005634")
```

## Features

- **Protein Search**: Search for proteins by ID, name, or other identifiers
- **GO Term Search**: Find proteins associated with specific GO terms
- **Protein Details**: View comprehensive protein information including:
  - Basic information (ID, name, etc.)
  - Functional annotations (GO terms)
  - Protein-protein interactions
- **Network Visualization**: Interactive visualization of protein-protein interaction networks
- **Responsive UI**: Bootstrap-powered responsive design for all device sizes

## License

[License information to be added] 