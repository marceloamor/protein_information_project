# Protein Information Explorer - Data Structure

## Overview
This document describes the data structure of the parquet files used in the Protein Information Explorer. The data is organized into four main parquet files that represent a graph-like structure of proteins, GO terms, and their relationships.

## Data Files

### 1. protein_nodes.parquet
Contains information about proteins.

**Schema:**
- `id` (string): Unique identifier for the protein in the format "Protein::UUID"
- `name` (string): Display name of the protein
- `sequence` (string): Amino acid sequence of the protein
- Additional metadata fields may be present

**Notes:**
- Contains 27,768 rows
- Primary source for protein details

### 2. go_term_nodes.parquet
Contains information about Gene Ontology (GO) terms.

**Schema:**
- `id` (string): Internal identifier in the format "GeneOntologyTerm::UUID"
- `external_id` (string): Standard GO term identifier (e.g., "GO:0005624")
- `name` (string): Name of the GO term
- `namespace` (string): GO namespace (possibly embedded in other fields)
- Additional metadata fields likely present

**Notes:**
- Contains 9,594 rows
- GO terms are categorized into three namespaces: BiologicalProcess, MolecularFunction, and CellularComponent

### 3. edges.parquet
Contains relationships between entities (proteins and GO terms).

**Schema:**
- `source` (string): Source node ID (usually a protein ID)
- `target` (string): Target node ID (protein ID or GO term ID)
- `relationship` (string): Type of relationship
  - `BiologicalProcess-Protein-FunctionalAnnotation`
  - `MolecularFunction-Protein-FunctionalAnnotation`
  - `CellularComponent-Protein-FunctionalAnnotation`
  - `Protein-Protein-ProteinProteinInteraction`
- `ML_prediction_score` (float): Score for functional annotations (GO terms)
- `string_combined_score` (float): Score for protein-protein interactions

**Notes:**
- Contains 498,731 rows
- Two main types of relationships:
  1. Functional annotations (between proteins and GO terms)
  2. Protein-protein interactions (between proteins)
- Relationships are directed (source → target)
- Includes proteins that may not have entries in protein_id_records.parquet

### 4. protein_id_records.parquet
Maps UUIDs to external protein identifiers.

**Schema:**
- `uuid` (string): UUID portion of the protein ID 
- `external_id` (string): Primary external identifier (same as the protein ID in protein_nodes)
- `secondary_ids` (list of strings): Alternative identifiers for the protein
- `ambiguous_secondary_ids` (list of strings): Ambiguous identifiers (may map to multiple proteins)

**Notes:**
- Contains 27,768 rows
- Important for mapping between different protein identifier systems
- **Data Model Issue**: Some protein IDs found in edges.parquet do not have corresponding entries in this file

## Data Model Relationships

```
protein_nodes.parquet
    |
    |-- id = edges.parquet.source/target (for proteins)
    |
    v
edges.parquet
    |
    |-- target = go_term_nodes.parquet.id (for GO terms)
    |
    v
go_term_nodes.parquet

protein_id_records.parquet
    |
    |-- uuid = part of protein_nodes.parquet.id (format: "Protein::{uuid}")
    |
    v
protein_nodes.parquet
```

## Lookup Maps

The DataLoader creates several lookup maps for efficient data access:

1. **id_to_details**: Maps protein IDs to their details
   - Key: Protein ID (e.g., "Protein::abb25e3e-02ba-569b-b459-56a70ef884c4")
   - Value: Dictionary of protein details

2. **uuid_to_ids**: Maps UUIDs to protein IDs
   - Key: UUID (e.g., "Protein::0003eb56-eabe-57d3-b639-65c673c4f6b2")
   - Value: List of protein IDs

3. **identifier_to_ids**: Maps all identifiers to protein IDs
   - Key: Any identifier (Protein ID, external ID, secondary ID)
   - Value: List of protein IDs

4. **name_to_ids**: Maps protein names to protein IDs
   - Key: Protein name (e.g., "AT1G01010.1")
   - Value: List of protein IDs

## Known Issues and Solutions

1. **Data Model Inconsistency**: Some protein IDs found in edges.parquet don't have corresponding records in protein_id_records.parquet. Example:
   ```
   Protein::edb7a0a0-b7d6-5f2d-b2eb-8f91f17aa5ca
   ```
   
2. **Resolution Strategy**: The DataLoader has been modified to:
   - Create a lookup map directly from protein IDs in edges.parquet
   - Provide default minimal entries for proteins missing from protein_nodes
   - Allow searching and retrieving interactions for all proteins, even if they lack complete records

3. **Search Functionality Fix**: We've implemented a robust search mechanism that:
   - Handles different types of identifiers (IDs, names, external IDs)
   - Provides fuzzy matching for partial name searches
   - Properly maps protein IDs to their details

## Usage in the Application

1. **Search Operations**:
   - By protein ID: Uses the identifier_to_ids map
   - By protein name: Uses the name_to_ids map with fallback to fuzzy matching
   - By GO term: Searches go_term_nodes and follows edges to proteins

2. **Detail Retrieval**:
   - Protein details: Combines data from protein_nodes with functional annotations and interactions from edges
   - GO term details: Retrieves GO term information and associated proteins

3. **Data Relationships**:
   - Functional annotations: Connect proteins to GO terms
   - Protein-protein interactions: Connect proteins to other proteins 