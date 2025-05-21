#!/usr/bin/env python
"""
Script to debug the search_protein method in the DataLoader class.
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
    """Main function to debug the search_protein method."""
    # Initialize the DataLoader
    print("Initializing DataLoader...")
    loader = DataLoader(data_path="data")
    
    # 1. Check lookup map construction
    print_separator("Lookup Map Sizes")
    print(f"id_to_details: {len(loader.id_to_details)} entries")
    print(f"uuid_to_ids: {len(loader.uuid_to_ids)} entries")
    print(f"identifier_to_ids: {len(loader.identifier_to_ids)} entries")
    
    # 2. Sample entries from the lookup maps
    print_separator("Sample Entries from Lookup Maps")
    
    # Sample id_to_details
    print("id_to_details samples:")
    count = 0
    for id, details in loader.id_to_details.items():
        print(f"  {id}: {details.get('name', 'No name')}")
        count += 1
        if count >= 3:
            break
    print()
    
    # Sample uuid_to_ids
    print("uuid_to_ids samples:")
    count = 0
    for uuid, ids in loader.uuid_to_ids.items():
        print(f"  {uuid}: {ids}")
        count += 1
        if count >= 3:
            break
    print()
    
    # Sample identifier_to_ids
    print("identifier_to_ids samples:")
    count = 0
    for identifier, ids in loader.identifier_to_ids.items():
        print(f"  {identifier}: {ids}")
        count += 1
        if count >= 3:
            break
    print()
    
    # 3. Check protein_ids content
    print_separator("Sample Protein IDs Content")
    print(f"protein_ids columns: {loader.protein_ids.columns.tolist()}")
    print("\nSample rows:")
    print(loader.protein_ids.head(3).to_string())
    
    # 4. Test specific searches
    print_separator("Testing Protein ID Search")
    
    # Get a few protein IDs from different sources
    test_ids = []
    
    # From protein_nodes
    if not loader.protein_nodes.empty and 'id' in loader.protein_nodes.columns:
        test_ids.extend(loader.protein_nodes['id'].head(2).tolist())
    
    # From protein_ids
    if not loader.protein_ids.empty and 'external_id' in loader.protein_ids.columns:
        test_ids.extend(loader.protein_ids['external_id'].head(2).tolist())
    
    # From UUIDs
    if not loader.protein_ids.empty and 'uuid' in loader.protein_ids.columns:
        test_ids.extend(loader.protein_ids['uuid'].head(2).tolist())
    
    # From secondary IDs if available
    secondary_ids = []
    for _, row in loader.protein_ids.iterrows():
        if 'secondary_ids' in row and isinstance(row['secondary_ids'], list) and row['secondary_ids']:
            secondary_ids.append(row['secondary_ids'][0])
            if len(secondary_ids) >= 2:
                break
    test_ids.extend(secondary_ids)
    
    # Test each ID
    for id in test_ids:
        if id is None:
            continue
        
        print(f"Searching for: {id}")
        results = loader.search_protein(id)
        print(f"  Results: {results}")
        
        # Check if this ID is in the identifier_to_ids map
        print(f"  In identifier_to_ids: {id in loader.identifier_to_ids}")
        
        # If not found, try to find where it should be
        if id not in loader.identifier_to_ids:
            # Check if it's in protein_nodes
            found_in_nodes = id in loader.protein_nodes['id'].values
            print(f"  Found in protein_nodes: {found_in_nodes}")
            
            # Check if it's in protein_ids
            found_in_ids = False
            if 'external_id' in loader.protein_ids.columns:
                found_in_ids = id in loader.protein_ids['external_id'].values
            print(f"  Found in protein_ids external_id: {found_in_ids}")
            
            # Check if it's a UUID
            found_in_uuids = False
            if 'uuid' in loader.protein_ids.columns:
                found_in_uuids = id in loader.protein_ids['uuid'].values
            print(f"  Found in protein_ids uuid: {found_in_uuids}")
        
        print()
    
    # 5. Fix the identifier_to_ids map (temporary fix for testing)
    print_separator("Trying to Fix identifier_to_ids Map")
    
    # Clear and rebuild the identifier_to_ids map
    original_map_size = len(loader.identifier_to_ids)
    loader.identifier_to_ids = {}
    
    # Add entries from protein_nodes
    for _, row in loader.protein_nodes.iterrows():
        protein_id = row['id']
        if protein_id not in loader.identifier_to_ids:
            loader.identifier_to_ids[protein_id] = [protein_id]
    
    # Add entries from protein_ids
    for _, row in loader.protein_ids.iterrows():
        uuid = row.get('uuid')
        external_id = row.get('external_id')
        
        # Map external_id to itself
        if external_id:
            if external_id not in loader.identifier_to_ids:
                loader.identifier_to_ids[external_id] = []
            if external_id not in loader.identifier_to_ids[external_id]:
                loader.identifier_to_ids[external_id].append(external_id)
        
        # Map UUID to external_id
        if uuid and external_id:
            if uuid not in loader.identifier_to_ids:
                loader.identifier_to_ids[uuid] = []
            if external_id not in loader.identifier_to_ids[uuid]:
                loader.identifier_to_ids[uuid].append(external_id)
        
        # Add secondary identifiers
        if 'secondary_ids' in row and isinstance(row.get('secondary_ids'), list):
            for identifier in row['secondary_ids']:
                if identifier not in loader.identifier_to_ids:
                    loader.identifier_to_ids[identifier] = []
                if external_id and external_id not in loader.identifier_to_ids[identifier]:
                    loader.identifier_to_ids[identifier].append(external_id)
    
    print(f"Original map size: {original_map_size}")
    print(f"New map size: {len(loader.identifier_to_ids)}")
    
    # 6. Test searches again
    print_separator("Testing Protein ID Search After Fix")
    
    for id in test_ids:
        if id is None:
            continue
        
        print(f"Searching for: {id}")
        results = loader.search_protein(id)
        print(f"  Results: {results}")
        print(f"  In identifier_to_ids: {id in loader.identifier_to_ids}")
        print()
    
    # 7. Sample specific protein details before concluding
    print_separator("Sample Protein Details")
    
    # Get a protein ID that works
    working_protein_id = None
    for id in test_ids:
        if id and id in loader.identifier_to_ids and loader.identifier_to_ids[id]:
            working_protein_id = loader.identifier_to_ids[id][0]
            break
    
    if working_protein_id:
        print(f"Details for protein: {working_protein_id}")
        details = loader.get_protein_details(working_protein_id)
        print(f"Name: {details.get('name', 'Unknown')}")
        print(f"UUID: {details.get('uuid', 'Unknown')}")
        print(f"Functional annotations: {len(details.get('functional_annotations', []))}")
        print(f"Protein interactions: {len(details.get('protein_interactions', []))}")

if __name__ == "__main__":
    main() 