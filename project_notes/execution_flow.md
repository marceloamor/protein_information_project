# Protein Information Project - Execution Flow

## Core Components and Flow

### DataLoader Initialization Flow
1. `DataLoader.__init__(data_path)` is called
2. Initialize internal state variables
3. Call `load_data()` to load all parquet files
4. Create lookup maps with `_create_lookup_maps()`
   - `id_to_details`: Maps protein IDs to their details
   - `uuid_to_ids`: Maps UUIDs to protein IDs
   - `identifier_to_ids`: Maps all identifiers to protein IDs
   - Special handling for protein IDs found in edges but missing from protein_id_records

### Search Operations

#### Protein Search Flow
1. User enters a protein identifier
2. `search_protein(identifier)` is called
3. Lookup identifier in `identifier_to_ids` map
4. Return list of matching protein IDs

#### GO Term Search Flow
1. User enters a GO term ID (e.g., "GO:0005624")
2. `search_by_go_term(go_term_id)` is called
3. Find the GO term in `go_terms` DataFrame using `external_id`
4. Look up the internal ID in the `edges` DataFrame to find proteins connected to this GO term
5. Return list of protein information dictionaries

### Detail Retrieval Flow

#### Protein Details Flow
1. User selects a protein from search results
2. `get_protein_details(protein_id)` is called
3. Retrieve basic details from `id_to_details` map
4. Add UUID if available in `uuid_to_ids` map
5. Add functional annotations with `_get_functional_annotations(protein_id)`
   - Find edges connecting this protein to GO terms
   - Retrieve GO term details and scores
6. Add protein interactions with `_get_protein_interactions(protein_id)`
   - Find edges connecting this protein to other proteins
   - Include interaction scores and directions
7. Return complete protein details dictionary

#### Functional Annotations Flow
1. `_get_functional_annotations(protein_id)` is called
2. Filter edges with source matching protein_id and relationship type is one of the functional annotation types
3. For each matching edge:
   - Retrieve GO term details from `go_terms` DataFrame
   - Extract namespace from relationship type
   - Create annotation dictionary with GO term information and score
4. Return list of annotation dictionaries

#### Protein Interactions Flow
1. `_get_protein_interactions(protein_id)` is called
2. Find edges where:
   - The protein is either the source or target
   - The relationship type is a protein-protein interaction
3. For each found edge:
   - Create interaction dictionary with the other protein's details
   - Set direction as "source" or "target"
   - Include interaction score
4. Return list of interaction dictionaries

## Testing Flow

### Test Script Flow 
1. Create a DataLoader instance with path to data
2. Display summary of loaded data
3. Test protein search with a specific protein ID
4. Retrieve and display protein details for the first match
5. Display sample functional annotations
6. Display sample protein-protein interactions
7. Test GO term search with a GO term from the dataset
8. Display sample proteins associated with the GO term

## Application Integration Flow (Future)

### Web App Flow (Planned)
1. Initialize DataLoader when the application starts
2. User enters search query in the interface
3. Call appropriate search method based on query type
4. Display search results in the UI
5. User selects a result to view details
6. Call appropriate detail retrieval method
7. Render details in the UI with visualizations 