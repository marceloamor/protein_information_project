# Protein Information Project - Data Structure

## Overview
This document describes the data structure of the parquet files used in the Protein Information Project. The data is organized into four main parquet files that represent a graph-like structure of proteins, GO terms, and their relationships.

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

## Known Issues

1. **Data Model Inconsistency**: Some protein IDs found in edges.parquet don't have corresponding records in protein_id_records.parquet. Example:
   ```
   Protein::edb7a0a0-b7d6-5f2d-b2eb-8f91f17aa5ca
   ```
   
2. **Resolution Strategy**: The DataLoader has been modified to:
   - Create a lookup map directly from protein IDs in edges.parquet
   - Provide default minimal entries for proteins missing from protein_nodes
   - Allow searching and retrieving interactions for all proteins, even if they lack complete records

## Usage in the Application

1. **Search Operations**:
   - By protein ID/name: Uses the identifier_to_ids map
   - By GO term: Searches go_term_nodes and follows edges to proteins

2. **Detail Retrieval**:
   - Protein details: Combines data from protein_nodes with functional annotations and interactions from edges
   - GO term details: Retrieves GO term information and associated proteins

3. **Data Relationships**:
   - Functional annotations: Connect proteins to GO terms
   - Protein-protein interactions: Connect proteins to other proteins 