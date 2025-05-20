"""
Minimal test script that uses only DuckDB to load and query the data.
"""
import pandas as pd
import duckdb
import os

def main():
    """Main function to test data loading with DuckDB."""
    print("Testing data loading with DuckDB...")
    
    # Connect to DuckDB
    con = duckdb.connect(':memory:')
    
    # List the parquet files
    data_dir = "data"
    parquet_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    print(f"Found {len(parquet_files)} parquet files: {', '.join(parquet_files)}")
    
    # Load each file
    for file in parquet_files:
        print(f"\nLoading {file}...")
        file_path = os.path.join(data_dir, file)
        
        # Query the file
        df = con.execute(f"SELECT * FROM '{file_path}' LIMIT 5").df()
        
        # Print info
        print(f"  Columns: {', '.join(df.columns)}")
        print(f"  Shape: {df.shape}")
        
        # Show a sample
        print("\nSample data:")
        print(df.head(2).to_string(index=False))
    
    print("\nAll files loaded successfully!")
    
    # Perform a sample join operation
    print("\nPerforming a sample query to join proteins with their GO terms...")
    
    # Path to files
    proteins_path = os.path.join(data_dir, "protein_nodes.parquet")
    go_terms_path = os.path.join(data_dir, "go_term_nodes.parquet")
    edges_path = os.path.join(data_dir, "edges.parquet")
    
    # Execute query
    query = f"""
    SELECT 
        p.id as protein_id, 
        p.name as protein_name,
        g.id as go_term_id,
        g.name as go_term_name,
        g.external_id as go_external_id,
        e.relationship,
        e.ML_prediction_score
    FROM '{proteins_path}' as p
    JOIN '{edges_path}' as e ON p.id = e.source
    JOIN '{go_terms_path}' as g ON g.id = e.target
    WHERE e.relationship = 'FunctionalAnnotation'
    LIMIT 10
    """
    
    result = con.execute(query).df()
    
    # Show results
    print("\nSample joined data:")
    print(result.to_string(index=False))
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main() 