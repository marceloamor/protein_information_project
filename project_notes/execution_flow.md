# Protein Information Explorer - Execution Flow

## Core Components and Flow

### Application Startup Flow
1. User runs `run.py` with optional command-line arguments
2. Command-line arguments are parsed (port, debug mode, log level)
3. Environment variables are set based on these arguments
4. The Dash application is imported from `src/app.py`
5. The application is started with the specified settings

### Dash Application Initialization
1. `app.py` initializes the Dash application with Bootstrap styling
2. The DataLoader is initialized to load data from parquet files
3. The application layout is created with routing components
4. Callbacks are registered for handling user interactions
5. The server starts and listens for requests

### DataLoader Initialization Flow
1. `DataLoader.__init__(data_path)` is called
2. Initialize internal state variables
3. Call `load_data()` to load all parquet files
4. Create lookup maps with `_create_lookup_maps()`
   - `id_to_details`: Maps protein IDs to their details
   - `uuid_to_ids`: Maps UUIDs to protein IDs
   - `identifier_to_ids`: Maps all identifiers to protein IDs
   - `name_to_ids`: Maps protein names to protein IDs
   - Special handling for protein IDs found in edges but missing from protein_id_records

### Navigation Flow
1. User navigates to a URL in the application
2. The `display_page` callback is triggered
3. Based on the URL pathname, the appropriate page is rendered:
   - `/`: Home page with search functionality
   - `/protein`: Protein detail page (if protein data is available)
   - `/about`: About page with application information
4. The page content is rendered within the main layout

## Search Operations

### Search Interface Flow
1. User enters a search term and selects a search type (protein or GO term)
2. User clicks the search button
3. The `perform_search` callback is triggered
4. Based on the search type, the appropriate search method is called
5. Search results are displayed as cards with "View Details" buttons

### Protein Search Flow
1. User enters a protein identifier
2. `search_protein(identifier)` is called
3. The identifier is looked up in the `identifier_to_ids` map
4. If not found, it's looked up in the `name_to_ids` map
5. If still not found and the identifier is at least 3 characters, fuzzy matching is attempted on protein names
6. A list of matching protein IDs is returned
7. For each match, a card is created with basic protein information and a "View Details" button

### GO Term Search Flow
1. User enters a GO term ID (e.g., "GO:0005624")
2. `search_by_go_term(go_term_id)` is called
3. Find the GO term in `go_terms` DataFrame using `external_id`
4. Look up the internal ID in the `edges` DataFrame to find proteins connected to this GO term
5. Return list of protein information dictionaries
6. For each match, a card is created with basic protein information and a "View Details" button

## Detail Retrieval Flow

### Protein Details View Flow
1. User clicks "View Details" on a search result
2. The `view_protein_details` callback is triggered
3. The protein ID is extracted from the clicked button
4. `get_protein_details(protein_id)` is called to retrieve comprehensive information
5. The protein data is stored in the session store
6. The user is redirected to the protein detail page
7. The protein detail page displays:
   - Basic protein information
   - Functional annotations (GO terms)
   - Protein-protein interactions

### Protein Details Retrieval Flow
1. `get_protein_details(protein_id)` is called
2. Retrieve basic details from `id_to_details` map
3. Add UUID if available in `uuid_to_ids` map
4. Add functional annotations with `_get_functional_annotations(protein_id)`
   - Find edges connecting this protein to GO terms
   - Retrieve GO term details and scores
5. Add protein interactions with `_get_protein_interactions(protein_id)`
   - Find edges connecting this protein to other proteins
   - Include interaction scores and directions
6. Return complete protein details dictionary

### Functional Annotations Flow
1. `_get_functional_annotations(protein_id)` is called
2. Filter edges with source matching protein_id and relationship type is one of the functional annotation types
3. For each matching edge:
   - Retrieve GO term details from `go_terms` DataFrame
   - Extract namespace from relationship type
   - Create annotation dictionary with GO term information and score
4. Return list of annotation dictionaries

### Protein Interactions Flow
1. `_get_protein_interactions(protein_id)` is called
2. Find edges where:
   - The protein is either the source or target
   - The relationship type is a protein-protein interaction
3. For each found edge:
   - Create interaction dictionary with the other protein's details
   - Set direction as "source" or "target"
   - Include interaction score
4. Return list of interaction dictionaries

## UI Component Flow

### Layout Component Flow
1. `create_layout(content)` is called with the page content
2. The layout is created with:
   - Navbar from `create_navbar()`
   - Container with the provided content
   - Footer from `create_footer()`
3. The complete layout is returned

### Search Component Flow
1. `create_search_form()` creates the search form with:
   - Input field for the search term
   - Radio buttons for the search type
   - Search button
2. `create_search_results()` creates a container for search results
3. When the search button is clicked, the `perform_search` callback is triggered
4. Search results are displayed in the results container

### Protein Card Component Flow
1. `create_protein_card(protein_details)` is called with protein details
2. The card is created with:
   - Basic information section
   - Functional annotations section
   - Protein interactions section
3. The complete card is returned and displayed on the protein detail page

## Testing Flow

### Verification Script Flow
1. Create a DataLoader instance with path to data
2. Test search functionality with various identifiers:
   - Protein IDs
   - Protein names
   - External IDs
   - Secondary identifiers
   - GO terms
3. For each successful search, retrieve and display:
   - Basic protein information
   - Sample functional annotations
   - Sample protein-protein interactions
4. For GO term searches, display associated proteins 