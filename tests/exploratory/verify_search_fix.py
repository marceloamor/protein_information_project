#!/usr/bin/env python
"""
Script to verify the search functionality fix in the DataLoader class.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.data.loader import DataLoader

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def main():
    """Main function to verify the search fix."""
    # Initialize the DataLoader
    print("Initializing DataLoader...")
    loader = DataLoader(data_path="data")
    
    # Test cases - try different types of identifiers
    test_cases = [
        # Protein IDs from protein_nodes
        "Protein::abb25e3e-02ba-569b-b459-56a70ef884c4",  # Direct protein ID
        "AT1G01010.1",  # Protein name
        
        # External IDs from protein_ids
        "UNIPROT_ACCESSION:A0A5S9Y508", 
        
        # UUIDs from protein_ids
        "Protein::0003eb56-eabe-57d3-b639-65c673c4f6b2", 
        
        # Secondary identifiers
        "TAIR:AT5G17870",  # Example from the debug output
        
        # GO terms (as a bonus)
        "GO:0004725"  # Example GO term from our previous output
    ]
    
    # Test each case
    print_separator("Search Results for Test Cases")
    
    for test_id in test_cases:
        print(f"Searching for: {test_id}")
        
        # Test protein search
        protein_results = loader.search_protein(test_id)
        print(f"Protein search results: {protein_results}")
        
        # If we found proteins, get details for the first one
        if protein_results:
            protein_id = protein_results[0]
            details = loader.get_protein_details(protein_id)
            print(f"  Name: {details.get('name', 'Unknown')}")
            print(f"  Functional annotations: {len(details.get('functional_annotations', []))}")
            print(f"  Protein interactions: {len(details.get('protein_interactions', []))}")
            
            # Show a few functional annotations if available
            if details.get('functional_annotations'):
                print("\n  Sample functional annotations:")
                for i, annot in enumerate(details['functional_annotations'][:3]):
                    print(f"    {i+1}. {annot.get('go_id')}: {annot.get('name')}")
                
                if len(details['functional_annotations']) > 3:
                    print(f"    ... and {len(details['functional_annotations']) - 3} more")
            
            # Show a few protein interactions if available
            if details.get('protein_interactions'):
                print("\n  Sample protein interactions:")
                for i, inter in enumerate(details['protein_interactions'][:3]):
                    print(f"    {i+1}. {inter.get('name', inter.get('protein_id'))} (score: {inter.get('score')})")
                
                if len(details['protein_interactions']) > 3:
                    print(f"    ... and {len(details['protein_interactions']) - 3} more")
        
        # Test GO term search if the input looks like a GO term
        if test_id.startswith("GO:"):
            go_results = loader.search_by_go_term(test_id)
            print(f"\nGO term search results: {len(go_results)} proteins")
            
            # Show a few results
            for i, protein in enumerate(go_results[:3]):
                print(f"  {i+1}. {protein.get('name', protein.get('protein_id'))} (score: {protein.get('score')})")
            
            if len(go_results) > 3:
                print(f"  ... and {len(go_results) - 3} more")
        
        print()

if __name__ == "__main__":
    main() 