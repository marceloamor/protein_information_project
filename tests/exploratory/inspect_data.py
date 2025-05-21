"""
This script inspects the parquet files in the data directory and prints out their schema and sample data.
Run this script to get a better understanding of the data before working on the application.
"""
from src.data.inspect import inspect_all_parquet_files
import pandas as pd
import json

def print_sample_data(file_path, n=3):
    """Print sample data from a parquet file in a more readable format."""
    print(f"\n--- Sample data from {file_path} (first {n} rows) ---")
    df = pd.read_parquet(file_path)
    for i, row in df.head(n).iterrows():
        print(f"\nRow {i}:")
        for col, val in row.items():
            if isinstance(val, (list, dict)):
                val_str = json.dumps(val, indent=2)
                print(f"  {col}: {val_str}")
            else:
                print(f"  {col}: {val}")
    print("\n" + "-" * 50)

if __name__ == "__main__":
    print("Inspecting parquet files...\n")
    results = inspect_all_parquet_files("data")
    
    # Print sample data for each file
    print("\nPrinting sample data from each file:")
    print_sample_data("data/protein_nodes.parquet")
    print_sample_data("data/go_term_nodes.parquet")
    print_sample_data("data/edges.parquet")
    print_sample_data("data/protein_id_records.parquet") 