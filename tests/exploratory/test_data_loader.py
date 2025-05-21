"""
Test script for the DataLoader class to ensure it can properly load and query the data.
"""
from src.data.loader import DataLoader

def test_data_loader():
    """Test DataLoader functionality."""
    print("Creating DataLoader...")
    loader = DataLoader(data_path="data")
    
    print("\nSummary of loaded data:")
    print(f"Proteins: {len(loader.protein_nodes)} rows")
    print(f"GO Terms: {len(loader.go_terms)} rows")
    print(f"Edges: {len(loader.edges)} rows")
    print(f"Protein IDs: {len(loader.protein_ids)} rows")
    
    # Test searching for a protein - use a protein known to have connections
    print("\nTesting protein search using a protein ID...")
    test_id = "Protein::edb7a0a0-b7d6-5f2d-b2eb-8f91f17aa5ca"  # Protein with most connections
    print(f"Searching for protein ID: {test_id}")
    results = loader.search_protein(test_id)
    print(f"Found {len(results)} matches")
    
    if results:
        # Get details for the first result
        print("\nGetting protein details...")
        protein_id = results[0]
        protein_details = loader.get_protein_details(protein_id)
        print(f"Protein ID: {protein_details.get('id', 'N/A')}")
        print(f"Protein name: {protein_details.get('name', 'N/A')}")
        print(f"Number of functional annotations: {len(protein_details.get('functional_annotations', []))}")
        print(f"Number of protein interactions: {len(protein_details.get('protein_interactions', []))}")
        
        # Print a sample functional annotation if available
        annotations = protein_details.get('functional_annotations', [])
        if annotations:
            print("\nSample functional annotations:")
            for i, annotation in enumerate(annotations[:3]):  # Show up to 3 annotations
                print(f"\nAnnotation {i+1}:")
                print(f"GO ID: {annotation.get('go_id', 'N/A')}")
                print(f"Name: {annotation.get('name', 'N/A')}")
                print(f"Namespace: {annotation.get('namespace', 'N/A')}")
                print(f"Score: {annotation.get('score', 'N/A')}")
        
        # Print a sample protein-protein interaction if available
        interactions = protein_details.get('protein_interactions', [])
        if interactions:
            print("\nSample protein interactions:")
            for i, interaction in enumerate(interactions[:3]):  # Show up to 3 interactions
                print(f"\nInteraction {i+1}:")
                print(f"Protein ID: {interaction.get('protein_id', 'N/A')}")
                print(f"Name: {interaction.get('name', 'N/A')}")
                print(f"Direction: {interaction.get('direction', 'N/A')}")
                print(f"Score: {interaction.get('score', 'N/A')}")
    
    # Test GO term search
    print("\nTesting GO term search...")
    if len(loader.go_terms) > 0:
        # Find a GO term that has associations
        go_term_row = loader.go_terms.iloc[0]
        test_go_id = go_term_row['external_id']  # GO:00... identifier
        print(f"Searching for GO term: {test_go_id}")
        go_results = loader.search_by_go_term(test_go_id)
        print(f"Found {len(go_results)} associated proteins")
        
        # If no results, try a different GO term
        if not go_results and len(loader.go_terms) > 10:
            test_go_id = loader.go_terms.iloc[10]['external_id']
            print(f"Trying another GO term: {test_go_id}")
            go_results = loader.search_by_go_term(test_go_id)
            print(f"Found {len(go_results)} associated proteins")
        
        # Display sample results
        if go_results:
            print("\nSample proteins associated with this GO term:")
            for i, protein in enumerate(go_results[:3]):  # Show up to 3 proteins
                print(f"\nProtein {i+1}:")
                print(f"Protein ID: {protein.get('protein_id', 'N/A')}")
                print(f"Name: {protein.get('name', 'N/A')}")
                print(f"UUID: {protein.get('uuid', 'N/A')}")
                print(f"Score: {protein.get('score', 'N/A')}")

if __name__ == "__main__":
    test_data_loader() 