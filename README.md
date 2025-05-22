# Protein Information Explorer

A web application for exploring protein information, including protein-protein interactions and Gene Ontology (GO) term annotations.

![Protein Information Explorer](assets/favicon.ico)

## Overview

The Protein Information Explorer allows researchers and biologists to:
- Search for proteins by various identifiers
- View detailed protein information
- Explore protein-protein interactions
- View functional annotations (GO terms)
- Search for proteins by GO term
- Visualize protein interaction networks

## Project Structure

```
protein_information_project/
├── assets/                 # Static assets (images, favicon)
├── data/                   # Data files (parquet format)
├── logs/                   # Application logs
├── project_notes/          # Project documentation
│   ├── data_structure.md   # Data structure documentation
│   ├── execution_flow.md   # Application flow documentation
│   └── installation_guide.md # Detailed installation guide
├── src/                    # Source code
│   ├── components/         # UI components
│   ├── data/               # Data handling
│   ├── pages/              # Application pages
│   └── utils/              # Utility functions
├── tests/                  # Tests
│   └── exploratory/        # Exploratory test scripts
├── install_dependencies.sh # Helper script for installation
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # Pip requirements
└── run.py                  # Main entry point
```

## Installation

### Prerequisites

- Python 3.9 or higher (Python 3.12/3.13 recommended)
- Poetry package manager (recommended) or pip

### Option 1: Using Poetry (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd protein_information_project
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

### Option 2: Using pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd protein_information_project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Ensure your environment is activated** (if using Poetry):
   ```bash
   poetry shell
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

3. **Access the application** in your web browser at:
   ```
   http://localhost:8050
   ```

### Command-line Options

```bash
python run.py --port 8080 --debug --log-level DEBUG
```

Available options:
- `--port`: Set the port number (default: 8050)
- `--debug`: Enable debug mode
- `--log-level`: Set log level (DEBUG, INFO, WARNING, ERROR)

## Data Model

The application uses four parquet files to store and retrieve protein information:

1. **protein_nodes.parquet**: Contains basic protein information
2. **go_term_nodes.parquet**: Contains Gene Ontology terms
3. **edges.parquet**: Represents relationships between entities
4. **protein_id_records.parquet**: Maps between different protein identifiers

For detailed information about the data model, see [data_structure.md](project_notes/data_structure.md).

## Features

### Search Functionality
- Search for proteins by various identifiers:
  - Protein IDs (e.g., "Protein::abb25e3e-02ba-569b-b459-56a70ef884c4")
  - Protein names (e.g., "AT1G01010.1")
  - External IDs (e.g., "UNIPROT_ACCESSION:A0A5S9Y508")
  - Secondary identifiers
- Search for proteins by GO term (e.g., "GO:0004725")

### Protein Details
- View comprehensive protein information
- Explore functional annotations (GO terms)
- Visualize protein-protein interactions

### User Interface
- Clean, responsive design using Dash and Bootstrap
- Interactive components for exploring protein data
- Visualization of protein interaction networks

## Testing

To run the exploratory tests:

```bash
python tests/exploratory/verify_search_fix.py
```

For detailed exploration of the data:

```bash
python tests/exploratory/find_search_terms.py
```

## Application Flow

For detailed information about how the application works, see [execution_flow.md](project_notes/execution_flow.md).

## Key Decisions and Future Improvements

### Key Design Decisions

1. **Data Loading Architecture**
   - **In-Memory Approach**: We load all data into memory using dictionaries and DataFrames
   - **Benefits**: Extremely fast lookups once loaded, ideal for interactive applications
   - **Trade-offs**: 
     - Memory Usage: Requires significant RAM (hundreds of MB for current dataset)
     - Startup Time: Initial loading increases with data size
     - Scalability: Limited by available RAM on a single machine
     - Static Data: Assumes data doesn't change during runtime

2. **Technology Stack**
   - Used Dash for the web framework due to its Python integration and interactive capabilities
   - Leveraged DuckDB for efficient parquet file handling, a full deployed application would replace this with a cloud hosted data lake and perform searches in real time 
   - Implemented Bootstrap components for responsive UI design

3. **Code Organization**
   - Separated sections with a clear module structure (data, components, pages)
   - Created reusable UI components to maintain consistency
   - Implemented a clean routing system for navigation between pages

4. **Search Implementation**
   - Dictionary-based lookups for exact matches (O(1) performance)
   - Simple fuzzy matching for partial name searches
   - **Trade-offs**: Fast for exact matches, but fuzzy search scales linearly with data size

### Scalability Considerations

1. **Cloud Data Lake Alternative**
   - For large/dynamic datasets, we could use:
     - Lazy loading patterns to load data on demand
     - Caching frequently accessed data while keeping most in external storage
     - Change data capture for real-time updates

2. **Database Considerations**
   - DuckDB could be replaced with cloud databases for larger workloads
   - Would require handling connection management, authentication, and query optimization
   - Network latency and cost models would need consideration
   - Different SQL dialects might require code changes

### Future Deployments and Cloud Integration

1. **Containerization and Cloud Deployment Options**
   - Dockerize the application for consistent deployment across environments
   - Create docker-compose setup for development environments
   - Implement proper logging and monitoring for production use

2. **Data Integration**
   - Connect to cloud data lakes or warehouses for larger datasets
   - Implement proper authentication and access controls
   - Consider data partitioning strategies for performance

### Improvements with More Time

1. **Performance Optimizations**
   - Implement pagination for large result sets
   - Add caching for frequently accessed data
   - Optimize the initial data loading process
   - Replace iterative search with indexed approaches for better scaling

2. **Enhanced Search Capabilities**
   - Implement more sophisticated fuzzy matching algorithms
   - Add support for dynamic searching, allowing the program to determine if a search term contains protein information or GO terms without user input
   - Due to limited time, I needed to create scripts to query the data files for structure, and therefore can't guarantee the search algorithms have been able to capture all data. Given more time to manually understand the data schema, or access to the data scientists that created the files, I would have more confidence the search results are comprehensive. 

3. **Testing and Validation**
   - Develop comprehensive unit tests for all components
   - Add integration tests for end-to-end workflows
   - Implement automated UI testing

### Nice-to-Have Features

1. **Enhanced Visualizations**
   - Interactive network graphs for protein interactions using Cytoscape
   - Enable clicking on graph nodes to access protein or GO term information cards
   - Hierarchical visualization of GO term relationships

2. **User Experience Improvements**
   - User accounts and saved searches
   - Export functionality for search results
   - Fix icon display issues in the UI

3. **Data Integration**
   - Real-time data updates
   - Support for user-uploaded datasets and cloud based data lakes 

4. **Documentation and Maintenance**
   - Add a CHANGELOG.md to track versions and feature requests
   - Create data/README.md to document data structure for developers
   - Clean up unused imports and optimize code
   - In-app tutorials and tooltips
   - Comprehensive API documentation
   - Example workflows for common research tasks

## License

Internal Biographica use only