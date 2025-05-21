#!/usr/bin/env python
"""
Script to probe the parquet files and find suitable search terms for testing.
"""
import os
import sys
import pandas as pd
import duckdb
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
    """Main function to probe the parquet files."""
    # Initialize the DataLoader
    print("Initializing DataLoader...")
    loader = DataLoader(data_path="data")
    
    # 1. Show basic statistics
    print_separator("Basic Statistics")
    print(f"Number of proteins: {len(loader.protein_nodes)}")
    print(f"Number of GO terms: {len(loader.go_terms)}")
    print(f"Number of edges: {len(loader.edges)}")
    print(f"Number of protein IDs: {len(loader.protein_ids)}")
    
    # 2. Sample protein IDs and names for search testing
    print_separator("Sample Protein IDs and Names")
    
    # Get 5 random protein samples
    protein_samples = loader.protein_nodes.sample(5)
    for i, (idx, protein) in enumerate(protein_samples.iterrows(), 1):
        print(f"Sample {i}:")
        print(f"  ID: {protein.get('id')}")
        print(f"  Name: {protein.get('name')}")
        print(f"  Type: {protein.get('type')}")
        
        # Try to find the UUID for this protein
        uuid = None
        for u, ids in loader.uuid_to_ids.items():
            if protein.get('id') in ids:
                uuid = u
                break
        
        print(f"  UUID: {uuid}")
        print()
    
    # 3. Sample GO terms for search testing
    print_separator("Sample GO Terms")
    
    # Get 5 random GO term samples
    go_samples = loader.go_terms.sample(5)
    for i, (idx, go_term) in enumerate(go_samples.iterrows(), 1):
        print(f"Sample {i}:")
        print(f"  ID: {go_term.get('id')}")
        print(f"  External ID: {go_term.get('external_id')}")
        print(f"  Name: {go_term.get('name')}")
        print(f"  Type: {go_term.get('type')}")
        print()
    
    # 4. Test searching for a few proteins
    print_separator("Test Protein Search")
    
    # Test with the first protein sample's ID
    for i, (idx, protein) in enumerate(protein_samples.iterrows()):
        protein_id = protein.get('id')
        print(f"Searching for protein with ID: {protein_id}")
        
        results = loader.search_protein(protein_id)
        print(f"Found {len(results)} matches:")
        for j, result_id in enumerate(results[:5], 1):  # Show up to 5 results
            print(f"  {j}. {result_id}")
        
        if len(results) > 5:
            print(f"  ... and {len(results) - 5} more")
        print()
    
    # 5. Test searching for GO terms
    print_separator("Test GO Term Search")
    
    # Test with the first GO term sample's external ID
    for i, (idx, go_term) in enumerate(go_samples.iterrows()):
        go_id = go_term.get('external_id')
        print(f"Searching for proteins associated with GO term: {go_id}")
        
        results = loader.search_by_go_term(go_id)
        print(f"Found {len(results)} protein matches:")
        for j, result in enumerate(results[:5], 1):  # Show up to 5 results
            print(f"  {j}. {result.get('protein_id')} ({result.get('name')})")
        
        if len(results) > 5:
            print(f"  ... and {len(results) - 5} more")
        print()
    
    # 6. Print examples of protein secondary identifiers
    print_separator("Sample Protein Secondary Identifiers")
    
    # Find some proteins with secondary identifiers
    sample_count = 0
    for idx, record in loader.protein_ids.iterrows():
        if 'secondary_ids' in record and isinstance(record['secondary_ids'], list) and record['secondary_ids']:
            print(f"Sample {sample_count + 1}:")
            print(f"  UUID: {record.get('uuid')}")
            print(f"  External ID: {record.get('external_id')}")
            print(f"  Secondary IDs: {', '.join(record['secondary_ids'][:5])}")
            if len(record['secondary_ids']) > 5:
                print(f"  ... and {len(record['secondary_ids']) - 5} more")
            print()
            
            sample_count += 1
            if sample_count >= 5:
                break

if __name__ == "__main__":
    main() 