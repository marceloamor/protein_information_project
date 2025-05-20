import pandas as pd
import duckdb
from pathlib import Path

def inspect_parquet(file_path: str) -> dict:
    """
    Inspect a parquet file and return its schema and sample data.
    
    Args:
        file_path: Path to the parquet file.
        
    Returns:
        A dictionary containing the schema and sample data.
    """
    # Read the parquet file
    df = pd.read_parquet(file_path)
    
    # Get schema information
    schema = {
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'shape': df.shape
    }
    
    # Get sample data (first 5 rows)
    sample = df.head(5).to_dict('records')
    
    return {
        'schema': schema,
        'sample': sample
    }

def inspect_all_parquet_files(directory: str = "."):
    """
    Inspect all parquet files in a directory.
    
    Args:
        directory: Path to the directory containing the parquet files.
    """
    # Find all parquet files in the directory
    parquet_files = list(Path(directory).glob("*.parquet"))
    
    results = {}
    for file_path in parquet_files:
        print(f"Inspecting {file_path.name}...")
        results[file_path.name] = inspect_parquet(file_path)
        
        # Print schema
        schema = results[file_path.name]['schema']
        print(f"  Shape: {schema['shape'][0]} rows, {schema['shape'][1]} columns")
        print(f"  Columns: {', '.join(schema['columns'])}")
        print()
        
    return results

if __name__ == "__main__":
    # Inspect all parquet files in the current directory
    inspect_all_parquet_files() 